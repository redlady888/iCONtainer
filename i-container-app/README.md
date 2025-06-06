# i-CONtainer App

## Overview

The i-CONtainer app is a professional, mobile-friendly platform simulation for a smart food storage product. It uses a clean dark theme with violet as the key accent color. The app demonstrates how the real i-CONtainer platform will function: sensors collect data, the platform processes it, and the app delivers clear feedback to users.

## Features

### Food Spoilage Detection
- Select food type (meat, eggs, rice, etc.)
- Input simulated sensor readings for CO₂, Ammonia (NH₃), H₂S, and VOCs
- View spoilage status with color-coded indicators (Fresh, Warning, Spoiled)
- Detailed breakdown of gas values with visual indicators

### Account Management
- User profile information
- Subscription management
- Payment processing simulation
- Payment history tracking

### Device Management
- Device information display
- Battery status monitoring
- Firmware version information
- Sensor calibration

### Additional Features
- Multiple product support
- Mobile-responsive design
- High-tech modern interface
- Traffic light visualization for food status

## Installation and Setup

### Prerequisites
- Python 3.7+
- pip

### Installation Steps

1. Clone the repository:
```
git clone https://github.com/your-username/i-container-app.git
cd i-container-app
```

2. Install the required dependencies:
```
pip install streamlit pandas numpy matplotlib
```

3. Run the application:
```
streamlit run app.py
```

4. Access the application in your web browser at:
```
http://localhost:8501
```

## Usage Guide

### Food Spoilage Detection

1. Select the "Food Spoilage Detection" tab
2. Choose a food type (meat, eggs, dairy, fruits, vegetables, rice)
3. Adjust the sliders to simulate sensor readings for different gases
4. Click "Analyze Food Status" to see the results
5. View the traffic light indicator and detailed gas readings

### Account Management

1. Select the "Account Details" tab to view your account information
2. View subscription details and payment history
3. See connected products and device information

### Subscription Management

1. Select a subscription plan from the sidebar
2. Click "Process Payment" to simulate a payment
3. Complete the payment form with the provided test credit card details
4. View updated subscription information in the Account Details tab

## Demo Accounts

The app includes two demo accounts for testing:

1. **Demo User**
   - Basic subscription ($1/month)
   - One connected product (i-CONtainer)

2. **Premium User**
   - Premium subscription ($500/3-years)
   - Two connected products (i-CONtainer, Smart Shelf)

You can switch between these accounts using the buttons in the sidebar.

## Deployment

The app is currently deployed and accessible at:
https://8501-ibujdrm9445l3qllulxo0-cc8447c1.manusvm.computer

## Project Structure

```
i-container-app/
├── app.py                  # Main application file
├── user_management.py      # User account management module
├── payment_simulation.py   # Payment processing simulation
├── assets/
│   ├── logo.png            # App logo
│   ├── style.css           # Custom CSS styling
│   ├── create_logo.py      # Logo generation script
│   ├── thresholds.json     # Food spoilage thresholds data
│   └── users.json          # User account data
└── README.md               # This documentation file
```

## Future Enhancements

- Integration with real sensor hardware
- Automatic stock refill functionality
- Additional smart device integration
- Mobile app version
- Data analytics and trend reporting

## Support

For any questions or issues, please contact support@i-container.com

