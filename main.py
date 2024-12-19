import functions
import pandas as pd
import yfinance as yf

def main():
    print("Welcome to the Stock Selection Tool")
    user_authenticated = False
    
    # User Authentication Process
    while not user_authenticated:
        print("\n1. Register\n2. Login")
        choice = input("Enter your choice (1/2): ").strip()
        
        if choice == "1":
            try:
                email = input("Enter your email: ").strip()
                password = input("Enter your password: ").strip()
                functions.register_user(email, password)
                print("Registration successful! Please log in.")
            except ValueError as e:
                print(e)
        elif choice == "2":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            if functions.authenticate_user(email, password):
                user_authenticated = True
            else:
                print("Invalid credentials. Please try again.")
    
    print("Login successful!")
    
    while True:
        # Sequential Flow for Stock Data and Analysis
        ticker = input("Enter stock ticker (e.g., 1155.KL): ").strip()
        start_date = input("Enter start date (YYYY-MM-DD): ").strip()
        end_date = input("Enter end date (YYYY-MM-DD): ").strip()
        
        try:
            # Fetch and Display Stock Data
            closing_prices = functions.get_closing_prices(ticker, start_date, end_date)
            print(f"\nClosing Prices for {ticker}:\n{closing_prices}")
            
            # Perform Analysis
            analysis = functions.analyze_closing_prices(closing_prices)
            print("\nAnalysis Results:")
            for key, value in analysis.items():
                print(f"{key}: {value}")
            
            # Save Data
            functions.save_to_csv({
                "Email": email,
                "Stock Ticker": ticker,
                **analysis
            }, "user_data.csv")
            
            print("\nData saved successfully.")
            
            # Ask to View Previous Data
            view_previous = input("\nDo you want to view previously saved data? (yes/no): ").strip().lower()
            if view_previous == "yes":
                saved_data = functions.read_from_csv("user_data.csv")
                print("\nSaved Data:")
                print(saved_data)
            else:
                print("You chose not to view the saved data.")
        
        except Exception as e:
            print(f"Error processing stock data: {e}")
        
        # Ask if the user wants to do another analysis
        another_analysis = input("\nDo you want to analyze another stock? (yes/no): ").strip().lower()
        if another_analysis != "yes":
            print("Thank you for using the Stock Selection Tool. Goodbye!")
            break
if __name__ == "__main__":
    main()
