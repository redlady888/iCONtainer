import streamlit as st
import time
from datetime import datetime
from user_management import get_user_manager

class PaymentSimulation:
    def __init__(self):
        self.user_manager = get_user_manager()
    
    def display_payment_form(self, user_id, subscription):
        """Display payment form for subscription"""
        st.subheader("Payment Information")
        
        # Get subscription amount
        amount = subscription.split("/")[0]
        period = subscription.split("/")[1]
        
        # Display payment summary
        st.markdown(f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px; margin: 15px 0;">
            <h4>Payment Summary</h4>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Plan:</div>
                <div>{period} subscription</div>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Amount:</div>
                <div style="color: #8a2be2; font-weight: bold;">{amount}</div>
            </div>
            <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                <div>Start Date:</div>
                <div>{datetime.now().strftime("%Y-%m-%d")}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Payment method selection
        payment_method = st.radio(
            "Select Payment Method",
            ["Credit Card", "PayPal", "Apple Pay"],
            horizontal=True
        )
        
        # Credit card form
        if payment_method == "Credit Card":
            col1, col2 = st.columns(2)
            
            with col1:
                card_number = st.text_input("Card Number", value="4242 4242 4242 4242", help="For simulation, use 4242 4242 4242 4242")
            
            with col2:
                expiry = st.text_input("Expiry Date", value="12/25")
            
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Cardholder Name", value="Demo User")
            
            with col2:
                cvv = st.text_input("CVV", value="123", type="password")
        
        elif payment_method == "PayPal":
            st.info("You will be redirected to PayPal to complete the payment.")
            st.text_input("PayPal Email", value="demo@example.com")
        
        else:  # Apple Pay
            st.info("You will be redirected to Apple Pay to complete the payment.")
        
        # Terms and conditions
        terms = st.checkbox("I agree to the Terms and Conditions", value=True)
        
        # Process payment button
        if st.button("Complete Payment", disabled=not terms):
            return self.process_payment(user_id, subscription, payment_method)
        
        return False
    
    def process_payment(self, user_id, subscription, payment_method):
        """Process payment simulation"""
        with st.spinner("Processing payment..."):
            # Simulate payment processing delay
            time.sleep(2)
            
            # Update user subscription
            success = self.user_manager.update_subscription(user_id, subscription)
            
            if success:
                st.success(f"Payment successful! Your subscription has been updated to {subscription}.")
                
                # Display receipt
                st.markdown("""
                <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px; margin: 15px 0;">
                    <h4>Receipt</h4>
                    <div style="text-align: center; margin: 20px 0;">
                        <div style="font-size: 3rem; color: #00cc66;">✓</div>
                        <div style="color: #00cc66; font-weight: bold;">Payment Successful</div>
                    </div>
                    <div style="margin-top: 20px; font-size: 0.8rem; color: #cccccc; text-align: center;">
                        A receipt has been sent to your email.
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                return True
            else:
                st.error("Payment failed. Please try again.")
                return False
    
    def display_payment_history(self, user_id):
        """Display payment history for user"""
        payment_history = self.user_manager.get_payment_history(user_id)
        
        if payment_history:
            st.subheader("Payment History")
            
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
    
    def display_subscription_details(self, user_id):
        """Display subscription details for user"""
        subscription = self.user_manager.get_subscription_details(user_id)
        
        if subscription:
            st.subheader("Subscription Details")
            
            status_color = "#00cc66" if subscription['status'] == "Active" else "#ff4500"
            
            st.markdown(f"""
            <div style="background-color: #1e1e1e; padding: 20px; border-radius: 8px; margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <div>Plan:</div>
                    <div>{subscription['plan']}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <div>Start Date:</div>
                    <div>{subscription['start_date']}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <div>End Date:</div>
                    <div>{subscription['end_date']}</div>
                </div>
                <div style="display: flex; justify-content: space-between; margin: 10px 0;">
                    <div>Status:</div>
                    <div style="color: {status_color}; font-weight: bold;">{subscription['status']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No subscription details found.")

