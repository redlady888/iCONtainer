import streamlit as st
import json
import os
from datetime import datetime, timedelta

# User management functions
class UserManagement:
    def __init__(self):
        self.users_file = os.path.join(os.path.dirname(__file__), "assets", "users.json")
        self.load_users()
    
    def load_users(self):
        """Load users from JSON file or create default if not exists"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r') as f:
                    self.users = json.load(f)
            else:
                # Create default users
                self.users = {
                    "demo_user": {
                        "username": "Demo User",
                        "email": "demo@i-container.com",
                        "subscription": "$1/month",
                        "subscription_start": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                        "subscription_end": (datetime.now() + timedelta(days=15)).strftime("%Y-%m-%d"),
                        "products": ["i-CONtainer"],
                        "payment_history": [
                            {
                                "date": (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d"),
                                "amount": "$1.00",
                                "description": "Monthly subscription"
                            }
                        ]
                    },
                    "premium_user": {
                        "username": "Premium User",
                        "email": "premium@i-container.com",
                        "subscription": "$500/3-years",
                        "subscription_start": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                        "subscription_end": (datetime.now() + timedelta(days=1065)).strftime("%Y-%m-%d"),
                        "products": ["i-CONtainer", "Smart Shelf"],
                        "payment_history": [
                            {
                                "date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
                                "amount": "$500.00",
                                "description": "3-year subscription"
                            }
                        ]
                    }
                }
                self.save_users()
        except Exception as e:
            st.error(f"Error loading users: {e}")
            self.users = {}
    
    def save_users(self):
        """Save users to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump(self.users, f, indent=4)
        except Exception as e:
            st.error(f"Error saving users: {e}")
    
    def get_user(self, user_id):
        """Get user by ID"""
        return self.users.get(user_id, None)
    
    def update_subscription(self, user_id, subscription):
        """Update user subscription"""
        if user_id in self.users:
            self.users[user_id]["subscription"] = subscription
            
            # Update subscription dates
            self.users[user_id]["subscription_start"] = datetime.now().strftime("%Y-%m-%d")
            
            if subscription == "$1/month":
                end_date = datetime.now() + timedelta(days=30)
            elif subscription == "$200/year":
                end_date = datetime.now() + timedelta(days=365)
            else:  # $500/3-years
                end_date = datetime.now() + timedelta(days=1095)
            
            self.users[user_id]["subscription_end"] = end_date.strftime("%Y-%m-%d")
            
            # Add payment to history
            amount = subscription.split("/")[0]
            period = subscription.split("/")[1]
            
            payment = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": amount,
                "description": f"{period} subscription"
            }
            
            if "payment_history" not in self.users[user_id]:
                self.users[user_id]["payment_history"] = []
            
            self.users[user_id]["payment_history"].append(payment)
            
            self.save_users()
            return True
        return False
    
    def add_product(self, user_id, product):
        """Add product to user"""
        if user_id in self.users:
            if "products" not in self.users[user_id]:
                self.users[user_id]["products"] = []
            
            if product not in self.users[user_id]["products"]:
                self.users[user_id]["products"].append(product)
                self.save_users()
            return True
        return False
    
    def get_subscription_details(self, user_id):
        """Get subscription details for user"""
        if user_id in self.users:
            user = self.users[user_id]
            return {
                "plan": user.get("subscription", ""),
                "start_date": user.get("subscription_start", ""),
                "end_date": user.get("subscription_end", ""),
                "status": "Active" if datetime.now() < datetime.strptime(user.get("subscription_end", "2099-12-31"), "%Y-%m-%d") else "Expired"
            }
        return None
    
    def get_payment_history(self, user_id):
        """Get payment history for user"""
        if user_id in self.users:
            return self.users[user_id].get("payment_history", [])
        return []

# Initialize user management
def get_user_manager():
    if 'user_manager' not in st.session_state:
        st.session_state.user_manager = UserManagement()
    return st.session_state.user_manager

# Payment processing simulation
def process_payment_simulation(user_id, subscription):
    """Simulate payment processing"""
    user_manager = get_user_manager()
    
    # In a real app, this would connect to a payment gateway
    # For simulation, we'll just update the user's subscription
    success = user_manager.update_subscription(user_id, subscription)
    
    return success

