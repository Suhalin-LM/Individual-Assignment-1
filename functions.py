import yfinance as yf
import pandas as pd
import os
import re  # Add this at the top for regular expression support

CREDENTIALS_FILE = "credentials.csv"



def register_user(email, password):
    """
    Register a new user by saving their email and password to a CSV file.
    """
    # Email validation
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValueError("Invalid email format. Please enter a valid email address.")
    
    if not os.path.isfile(CREDENTIALS_FILE):
        # Create the file with headers if it doesn't exist
        pd.DataFrame(columns=["Email", "Password"]).to_csv(CREDENTIALS_FILE, index=False)

    # Check if the email is already registered
    existing_users = pd.read_csv(CREDENTIALS_FILE)
    if email in existing_users["Email"].values:
        raise ValueError("Email is already registered. Please log in.")

    # Append the new user
    new_user = pd.DataFrame([{"Email": email, "Password": password}])
    new_user.to_csv(CREDENTIALS_FILE, mode="a", header=False, index=False)


def authenticate_user(email, password):
    """
    Authenticate the user by checking their credentials in the CSV file.
    """
    if not os.path.isfile(CREDENTIALS_FILE):
        return False

    # Read credentials from the file
    users = pd.read_csv(CREDENTIALS_FILE)
    matching_user = users[(users["Email"] == email) & (users["Password"] == password)]
    return not matching_user.empty

def get_closing_prices(ticker, start_date, end_date):
    stock_data = yf.download(ticker, start=start_date, end=end_date)
    return stock_data['Close']

def analyze_closing_prices(data):
    """
    Analyze the closing prices to calculate key statistics and include dates for the highest and lowest prices.
    """
    avg_price = data.mean()
    percent_change = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
    highest_price = data.max()
    lowest_price = data.min()
    
    highest_price_date = data.idxmax()  # Date of the highest price
    lowest_price_date = data.idxmin()  # Date of the lowest price
    
    return {
        "Average Closing Price": avg_price,
        "Percentage Change": percent_change,
        "Highest Closing Price": highest_price,
        "Highest Price Date": highest_price_date,
        "Lowest Closing Price": lowest_price,
        "Lowest Price Date": lowest_price_date
    }


def save_to_csv(data, filename):
    file_exists = os.path.isfile(filename)
    df = pd.DataFrame([data])
    
    if not file_exists:
        df.to_csv(filename, index=False)
    else:
        df.to_csv(filename, mode='a', header=False, index=False)

def read_from_csv(filename):
    return pd.read_csv(filename)
