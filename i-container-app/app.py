import streamlit as st
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from user_management import get_user_manager
from payment_simulation import PaymentSimulation

# Set page configuration
st.set_page_config(
    page_title="i-CONtainer",
    page_icon="🥫",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Load custom CSS
def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "assets", "style.css")
    with open(css_file, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the CSS
load_css()

# Initialize user management and payment simulation
user_manager = get_user_manager()
payment_sim = PaymentSimulation()

# Initialize session state variables if they don't exist
if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = "demo_user"

if 'products' not in st.session_state:
    user = user_manager.get_user(st.session_state.current_user_id)
    if user and "products" in user:
        st.session_state.products = user["products"]
    else:
        st.session_state.products = ['i-CONtainer']

if 'selected_product' not in st.session_state:
    st.session_state.selected_product = 'i-CONtainer'

if 'subscription' not in st.session_state:
    user = user_manager.get_user(st.session_state.current_user_id)
    if user and "subscription" in user:
        st.session_state.subscription = user["subscription"]
    else:
        st.session_state.subscription = '$1/month'

if 'username' not in st.session_state:
    user = user_manager.get_user(st.session_state.current_user_id)
    if user and "username" in user:
        st.session_state.username = user["username"]
    else:
        st.session_state.username = 'Demo User'

if 'payment_status' not in st.session_state:
    st.session_state.payment_status = None

if 'show_payment_form' not in st.session_state:
    st.session_state.show_payment_form = False

# Define thresholds for gas sensors
THRESHOLDS = {
    'meat': {
        'CO2': {'warning': 5000, 'spoiled': 10000},
        'NH3': {'warning': 15, 'spoiled': 30},
        'H2S': {'warning': 5, 'spoiled': 10},
        'VOCs': {'warning': 1000, 'spoiled': 2000}
    },
    'eggs': {
        'CO2': {'warning': 3000, 'spoiled': 7000},
        'NH3': {'warning': 20, 'spoiled': 40},
        'H2S': {'warning': 3, 'spoiled': 8},
        'VOCs': {'warning': 800, 'spoiled': 1500}
    },
    'dairy': {
        'CO2': {'warning': 4000, 'spoiled': 8000},
        'NH3': {'warning': 10, 'spoiled': 25},
        'H2S': {'warning': 2, 'spoiled': 6},
        'VOCs': {'warning': 900, 'spoiled': 1800}
    },
    'fruits': {
        'CO2': {'warning': 2000, 'spoiled': 5000},
        'NH3': {'warning': 5, 'spoiled': 15},
        'H2S': {'warning': 1, 'spoiled': 4},
        'VOCs': {'warning': 700, 'spoiled': 1400}
    },
    'vegetables': {
        'CO2': {'warning': 2500, 'spoiled': 6000},
        'NH3': {'warning': 8, 'spoiled': 20},
        'H2S': {'warning': 2, 'spoiled': 5},
        'VOCs': {'warning': 800, 'spoiled': 1600}
    },
    'rice': {
        'CO2': {'warning': 1500, 'spoiled': 4000},
        'NH3': {'warning': 10, 'spoiled': 25},
        'H2S': {'warning': 1, 'spoiled': 3},
        'VOCs': {'warning': 600, 'spoiled': 1200}
    }
}

# Function to add a new product
def add_product():
    new_product = st.session_state.new_product
    if new_product and new_product not in st.session_state.products:
        st.session_state.products.append(new_product)
        st.session_state.new_product = ""
        
        # Update user's products in the database
        user_manager.add_product(st.session_state.current_user_id, new_product)

# Function to select a product
def select_product(product):
    st.session_state.selected_product = product

# Function to determine spoilage status
def determine_spoilage(food_type, gas_values):
    status = "Fresh"
    gas_statuses = {}
    
    for gas, value in gas_values.items():
        if value >= THRESHOLDS[food_type][gas]['spoiled']:
            gas_statuses[gas] = "Above Limit"
            status = "Spoiled"
        elif value >= THRESHOLDS[food_type][gas]['warning']:
            gas_statuses[gas] = "Warning"
            if status != "Spoiled":
                status = "Warning"
        else:
            gas_statuses[gas] = "Normal"
    
    return status, gas_statuses

# Function to display traffic light
def display_traffic_light(status):
    html = """
    <div class="traffic-light">
    """
    
    if status == "Spoiled":
        html += '<div class="light red active"></div>'
    else:
        html += '<div class="light red"></div>'
        
    if status == "Warning":
        html += '<div class="light yellow active"></div>'
    else:
        html += '<div class="light yellow"></div>'
        
    if status == "Fresh":
        html += '<div class="light green active"></div>'
    else:
        html += '<div class="light green"></div>'
        
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)

# Function to process payment
def process_payment():
    # Show payment form
    st.session_state.show_payment_form = True

# Function to switch user
def switch_user(user_id):
    st.session_state.current_user_id = user_id
    
    # Update session state with user data
    user = user_manager.get_user(user_id)
    if user:
        st.session_state.username = user.get("username", "Demo User")
        st.session_state.subscription = user.get("subscription", "$1/month")
        st.session_state.products = user.get("products", ["i-CONtainer"])
        st.session_state.selected_product = "i-CONtainer"
    
    # Reset payment status
    st.session_state.payment_status = None
    st.session_state.show_payment_form = False

# Sidebar
with st.sidebar:
    # Logo
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    st.image(logo_path, width=200)
    
    # User account selector
    st.subheader("Account")
    
    # Get current user
    current_user = user_manager.get_user(st.session_state.current_user_id)
    
    # User account info
    st.markdown("""
    <div class="account-info">
        <div class="account-avatar">{}</div>
        <div class="account-name">{}</div>
    </div>
    """.format(st.session_state.username[0], st.session_state.username), unsafe_allow_html=True)
    
    # User switcher (for demo purposes)
    user_options = ["demo_user", "premium_user"]
    user_labels = ["Demo User", "Premium User"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Demo User", key="switch_demo", disabled=st.session_state.current_user_id == "demo_user"):
            switch_user("demo_user")
    
    with col2:
        if st.button("Premium User", key="switch_premium", disabled=st.session_state.current_user_id == "premium_user"):
            switch_user("premium_user")
    
    # Subscription section
    st.subheader("Subscription Plan")
    
    # Create subscription cards
    subscription_options = [
        {"name": "Basic", "price": "$1", "period": "month", "value": "$1/month"},
        {"name": "Standard", "price": "$200", "period": "year", "value": "$200/year"},
        {"name": "Premium", "price": "$500", "period": "3-years", "value": "$500/3-years"}
    ]
    
    for option in subscription_options:
        selected = option["value"] == st.session_state.subscription
        selected_class = "selected" if selected else ""
        
        if st.markdown(f"""
        <div class="subscription-card {selected_class}" onclick="this.closest('section').querySelector('button').click()">
            <div class="subscription-name">{option["name"]}</div>
            <div class="subscription-price">{option["price"]}</div>
            <div class="subscription-period">per {option["period"]}</div>
        </div>
        """, unsafe_allow_html=True):
            st.session_state.subscription = option["value"]
            st.session_state.payment_status = None
    
    # Hidden buttons for the subscription cards
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Basic", key="btn_basic", help="$1 per month"):
            st.session_state.subscription = "$1/month"
            st.session_state.payment_status = None
    with col2:
        if st.button("Standard", key="btn_standard", help="$200 per year"):
            st.session_state.subscription = "$200/year"
            st.session_state.payment_status = None
    with col3:
        if st.button("Premium", key="btn_premium", help="$500 for 3 years"):
            st.session_state.subscription = "$500/3-years"
            st.session_state.payment_status = None
    
    # Payment button
    if st.session_state.payment_status != "Success":
        if st.button("Process Payment", key="payment_button"):
            process_payment()
    
    if st.session_state.payment_status == "Processing":
        st.markdown("""
        <div style="display: flex; justify-content: center; margin: 20px 0;">
            <div class="loading"><div></div><div></div></div>
        </div>
        <div style="text-align: center;">Processing payment...</div>
        """, unsafe_allow_html=True)
    elif st.session_state.payment_status == "Success":
        st.success("Payment successful!")
    
    # Show subscription details
    subscription_details = user_manager.get_subscription_details(st.session_state.current_user_id)
    if subscription_details:
        st.markdown(f"""
        <div style="background-color: rgba(138, 43, 226, 0.1); padding: 10px; border-radius: 8px; margin: 10px 0; font-size: 0.8rem;">
            <div>Status: <span style="color: {'#00cc66' if subscription_details['status'] == 'Active' else '#ff4500'}; font-weight: bold;">{subscription_details['status']}</span></div>
            <div>Expires: {subscription_details['end_date']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Products list
    st.subheader("Your Products")
    
    for product in st.session_state.products:
        if product == st.session_state.selected_product:
            st.markdown(f"<div class='selected-product'>{product}</div>", unsafe_allow_html=True)
        else:
            if st.button(product, key=f"btn_{product}"):
                select_product(product)
    
    # Add new product
    st.text_input("Add new product", key="new_product")
    st.button("+ Add Product", on_click=add_product)

# Main content
st.markdown("<div class='logo-container'><h1>i-CONtainer</h1></div>", unsafe_allow_html=True)
st.markdown("<div class='slogan'>taste without waste</div>", unsafe_allow_html=True)

# Check if payment form should be shown
if st.session_state.show_payment_form:
    # Show payment form
    payment_success = payment_sim.display_payment_form(st.session_state.current_user_id, st.session_state.subscription)
    
    if payment_success:
        st.session_state.payment_status = "Success"
        st.session_state.show_payment_form = False
        
        # Add a button to continue
        if st.button("Continue to App"):
            st.session_state.show_payment_form = False
            st.experimental_rerun()
    
    # Add a button to cancel payment
    if st.button("Cancel Payment"):
        st.session_state.show_payment_form = False
        st.experimental_rerun()

# If not showing payment form, show the main app content
elif st.session_state.selected_product == "i-CONtainer":
    # Add a welcome animation
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 1.2rem; margin-bottom: 15px;">Welcome to the Smart Food Storage Solution</div>
        <div style="font-size: 0.9rem; color: #cccccc;">Use the simulator below to test food spoilage detection</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tabs for different features
    tab1, tab2, tab3 = st.tabs(["Food Spoilage Detection", "Device Settings", "Account Details"])
    
    with tab1:
        st.subheader("Food Spoilage Detection")
        
        # Food type selection with icons
        food_icons = {
            "meat": "🥩", 
            "eggs": "🥚", 
            "dairy": "🧀", 
            "fruits": "🍎", 
            "vegetables": "🥦", 
            "rice": "🍚"
        }
        
        # Create food type selection cards
        st.markdown("<div style='margin-bottom: 20px;'>Select food type:</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        food_type = None
        
        with col1:
            if st.button(f"{food_icons['meat']} Meat", key="meat_btn"):
                food_type = "meat"
            if st.button(f"{food_icons['eggs']} Eggs", key="eggs_btn"):
                food_type = "eggs"
        
        with col2:
            if st.button(f"{food_icons['dairy']} Dairy", key="dairy_btn"):
                food_type = "dairy"
            if st.button(f"{food_icons['fruits']} Fruits", key="fruits_btn"):
                food_type = "fruits"
        
        with col3:
            if st.button(f"{food_icons['vegetables']} Vegetables", key="vegetables_btn"):
                food_type = "vegetables"
            if st.button(f"{food_icons['rice']} Rice", key="rice_btn"):
                food_type = "rice"
        
        # Default food type if none selected
        if food_type is None:
            if 'food_type' not in st.session_state:
                st.session_state.food_type = "meat"
            food_type = st.session_state.food_type
        else:
            st.session_state.food_type = food_type
        
        # Display selected food type
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 10px; border-radius: 8px; margin: 15px 0; text-align: center;">
            <div style="font-size: 2rem;">{food_icons[food_type]}</div>
            <div style="font-weight: bold; text-transform: capitalize;">{food_type}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Gas sensor sliders
        st.subheader("Sensor Readings")
        st.markdown("<div style='font-size: 0.9rem; color: #cccccc; margin-bottom: 20px;'>Adjust the sliders to simulate sensor readings</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            co2 = st.slider("CO₂ (ppm)", 0, 15000, 1000, help="Carbon dioxide level in parts per million")
            nh3 = st.slider("NH₃ (ppm)", 0, 50, 5, help="Ammonia level in parts per million")
        
        with col2:
            h2s = st.slider("H₂S (ppm)", 0, 15, 1, help="Hydrogen sulfide level in parts per million")
            vocs = st.slider("VOCs (ppb)", 0, 3000, 500, help="Volatile organic compounds in parts per billion")
        
        # Collect gas values
        gas_values = {
            'CO2': co2,
            'NH3': nh3,
            'H2S': h2s,
            'VOCs': vocs
        }
        
        # Analyze button with animation
        analyze_btn = st.button("Analyze Food Status", key="analyze_btn", help="Click to analyze the food status based on sensor readings")
        
        if analyze_btn:
            # Show loading animation
            with st.spinner("Analyzing sensor data..."):
                # Simulate processing time
                import time
                time.sleep(1)
                
                # Determine spoilage status
                status, gas_statuses = determine_spoilage(food_type, gas_values)
                
                # Display results
                st.markdown("""
                <div class="results-container">
                    <h3>Analysis Results</h3>
                """, unsafe_allow_html=True)
                
                # Display traffic light
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    display_traffic_light(status)
                
                with col2:
                    if status == "Fresh":
                        st.markdown("""
                        <div style="background-color: rgba(0, 204, 102, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #00cc66;">
                            <div style="font-weight: bold; color: #00cc66; font-size: 1.2rem;">Status: Fresh</div>
                            <div>Your food is fresh and safe to consume.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    elif status == "Warning":
                        st.markdown("""
                        <div style="background-color: rgba(255, 165, 0, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #ffa500;">
                            <div style="font-weight: bold; color: #ffa500; font-size: 1.2rem;">Status: Warning</div>
                            <div>Your food is showing early signs of spoilage. Consume soon.</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div style="background-color: rgba(255, 69, 0, 0.1); padding: 15px; border-radius: 8px; border-left: 4px solid #ff4500;">
                            <div style="font-weight: bold; color: #ff4500; font-size: 1.2rem;">Status: Spoiled</div>
                            <div>Your food has spoiled and should not be consumed.</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Display detailed gas readings
                st.subheader("Detailed Gas Readings")
                
                for gas, value in gas_values.items():
                    status_class = ""
                    if gas_statuses[gas] == "Normal":
                        status_class = "status-normal"
                    elif gas_statuses[gas] == "Warning":
                        status_class = "status-warning"
                    else:
                        status_class = "status-danger"
                    
                    st.markdown(f"""
                    <div class="product-card">
                        <div>{gas}: {value} {gas if gas != 'VOCs' else 'ppb'}</div>
                        <div class="status-tag {status_class}">{gas_statuses[gas]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add visualization
                st.subheader("Gas Levels Visualization")
                
                fig, ax = plt.subplots(figsize=(10, 6))
                gases = list(gas_values.keys())
                values = list(gas_values.values())
                
                # Normalize values for comparison
                normalized_values = []
                colors = []
                
                for i, gas in enumerate(gases):
                    warning_threshold = THRESHOLDS[food_type][gas]['warning']
                    spoiled_threshold = THRESHOLDS[food_type][gas]['spoiled']
                    normalized_value = values[i] / spoiled_threshold
                    normalized_values.append(normalized_value)
                    
                    if values[i] >= spoiled_threshold:
                        colors.append('#ff4500')
                    elif values[i] >= warning_threshold:
                        colors.append('#ffa500')
                    else:
                        colors.append('#00cc66')
                
                # Set dark background style for the plot
                plt.style.use('dark_background')
                fig.patch.set_facecolor('#1e1e1e')
                ax.set_facecolor('#1e1e1e')
                
                bars = ax.bar(gases, normalized_values, color=colors)
                ax.set_ylim(0, 1.5)
                ax.set_ylabel('Normalized Gas Level (1.0 = Spoilage Threshold)')
                ax.set_title('Gas Levels Relative to Spoilage Thresholds')
                
                # Add threshold lines
                ax.axhline(y=1.0, color='r', linestyle='-', alpha=0.3, label='Spoilage Threshold')
                ax.axhline(y=0.5, color='orange', linestyle='-', alpha=0.3, label='Warning Threshold')
                
                # Add value labels on top of bars
                for i, bar in enumerate(bars):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                            f'{values[i]}',
                            ha='center', va='bottom', color='white')
                
                ax.legend()
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.spines['bottom'].set_color('#444444')
                ax.spines['left'].set_color('#444444')
                ax.tick_params(colors='white')
                
                plt.tight_layout()
                st.pyplot(fig)
                
                st.markdown("</div>", unsafe_allow_html=True)
    
    with tab3:
        st.subheader("Account Details")
        
        # Get current user
        current_user = user_manager.get_user(st.session_state.current_user_id)
        
        if current_user:
            # User profile
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"""
                <div style="width: 80px; height: 80px; background-color: #8a2be2; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; font-weight: bold;">
                    {current_user['username'][0]}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="padding: 10px;">
                    <div style="font-size: 1.5rem; font-weight: bold;">{current_user['username']}</div>
                    <div style="color: #cccccc;">{current_user['email']}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.divider()
            
            # Subscription details
            st.subheader("Subscription Details")
            
            # Get subscription details
            subscription_details = user_manager.get_subscription_details(st.session_state.current_user_id)
            
            if subscription_details:
                status_color = "#00cc66" if subscription_details['status'] == "Active" else "#ff4500"
                
                st.markdown(f"""
                <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <div>Plan:</div>
                        <div>{subscription_details['plan']}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <div>Start Date:</div>
                        <div>{subscription_details['start_date']}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <div>End Date:</div>
                        <div>{subscription_details['end_date']}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                        <div>Status:</div>
                        <div style="color: {status_color}; font-weight: bold;">{subscription_details['status']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Payment history
            st.subheader("Payment History")
            
            # Get payment history
            payment_history = user_manager.get_payment_history(st.session_state.current_user_id)
            
            if payment_history:
                for payment in payment_history:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="display: flex; justify-content: space-between;">
                            <div>{payment['date']}</div>
                            <div style="font-weight: bold;">{payment['amount']}</div>
                        </div>
                        <div style="color: #cccccc; font-size: 0.9rem;">{payment['description']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No payment history found.")
            
            # Connected products
            st.subheader("Connected Products")
            
            if "products" in current_user and current_user["products"]:
                for product in current_user["products"]:
                    st.markdown(f"""
                    <div class="product-card">
                        <div style="font-weight: bold;">{product}</div>
                        <div style="color: #cccccc; font-size: 0.9rem;">Connected since: {subscription_details['start_date']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No connected products found.")
        else:
            st.error("User not found.")
        
        # Device settings
        st.markdown("""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px; margin: 15px 0;">
            <h4>Device Information</h4>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Device ID:</div>
                <div style="color: #8a2be2;">IC-2025-0001</div>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Firmware Version:</div>
                <div>v2.3.1</div>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Battery Status:</div>
                <div style="color: #00cc66;">87%</div>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Last Calibration:</div>
                <div>2025-05-15</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Notification settings
        st.subheader("Notification Settings")
        
        notify_spoilage = st.checkbox("Notify when food is spoiling", value=True)
        notify_battery = st.checkbox("Notify on low battery", value=True)
        
        # Calibration button
        if st.button("Calibrate Sensors"):
            with st.spinner("Calibrating sensors..."):
                # Simulate calibration
                import time
                time.sleep(2)
                st.success("Sensors calibrated successfully!")

else:
    # Display coming soon for other products with enhanced styling
    st.markdown("""
    <div style="text-align: center; padding: 50px 0; background-color: #1e1e1e; border-radius: 8px; margin: 20px 0;">
        <h2 style="background: linear-gradient(90deg, #8a2be2, #9370db); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Coming Soon!</h2>
        <p style="color: #cccccc; margin: 20px 0;">This smart product is currently in development.</p>
        <div style="margin: 30px 0;">
            <button disabled style="background-color: #333; color: #888; padding: 10px 20px; border: none; border-radius: 4px; cursor: not-allowed;">Setup Device</button>
        </div>
        <div style="margin-top: 40px; font-size: 0.9rem; color: #888;">
            Expected release: Q3 2025
        </div>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    <div>© 2025 i-CONtainer. All rights reserved.</div>
    <div style="margin-top: 10px; font-size: 0.8rem;">
        <a href="#" style="color: #8a2be2; text-decoration: none; margin: 0 10px;">Privacy Policy</a>
        <a href="#" style="color: #8a2be2; text-decoration: none; margin: 0 10px;">Terms of Service</a>
        <a href="#" style="color: #8a2be2; text-decoration: none; margin: 0 10px;">Contact Us</a>
    </div>
</div>
""", unsafe_allow_html=True)

