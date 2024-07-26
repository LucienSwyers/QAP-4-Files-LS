#Code for Luciens 4th QAP Python Project
#Description - a program for One Stop Insurance Company
#Author - Lucien Swyers
#Dates - July15th  - July 26th

import datetime
import sys
import time

# Progress Bar Function

def ProgressBar(Iteration, Total, Prefix='', Suffix='', Length=30, Fill='█'):

    # Generate and display a progress bar with % complete at the end.

    Percent = ("{0:.1f}").format(100 * (Iteration / float(Total)))
    FilledLength = int(Length * Iteration // Total)
    Bar = Fill * FilledLength + '-' * (Length - FilledLength)
    sys.stdout.write(f'\r{Prefix} |{Bar}| {Percent}% {Suffix}')
    sys.stdout.flush()

# Load Constants Function

def LoadConstants():
    Constants = {}
    f = open('./Const.dat', 'r')
    for Line in f:
        Name, Value = Line.strip().split('=')
        Constants[Name] = float(Value) if '.' in Value else int(Value)
    f.close()
    return Constants

# Format Values Function

def FormatValues(Value, Currency=False):
    if Currency:
        return f"${Value:,.2f}"
    return str(Value).title()

# Calculate Premium

def CalculatePremium(NumCars, ExtraLiability, GlassCoverage, LoanerCar, Constants):
    TotalPremium = Constants['BasicPremium']
    if NumCars > 1:
        TotalPremium += (NumCars - 1) * Constants['BasicPremium'] * (1 - Constants['AdditionalCarDiscount'])
    TotalExtraCosts = (ExtraLiability * Constants['ExtraLiabilityCost'] +
                       GlassCoverage * Constants['GlassCoverageCost'] +
                       LoanerCar * Constants['LoanerCarCost']) * NumCars
    TotalPremium += TotalExtraCosts
    return TotalPremium

# Get User Input

def GetUserInput(Constants):
    ValidProvinces = ["AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"]
    ValidPaymentMethods = ["Full", "Monthly", "Down Pay"]
    
    while True:
        Province = input("Enter Province (e.g., ON for Ontario): ").upper()
        if Province in ValidProvinces:
            break
        else:
            print("Invalid province. Please enter a valid Canadian province code.")
    
    while True:
        PaymentMethod = input("Payment Method (Full/Monthly/Down Pay): ").title()
        if PaymentMethod in ValidPaymentMethods:
            break
        else:
            print("Invalid payment method. Please enter Full, Monthly, or Down Pay.")
    
    FirstName = input("Enter First Name: ").title()
    LastName = input("Enter Last Name: ").title()
    Address = input("Enter Address: ")
    City = input("Enter City: ").title()
    PostalCode = input("Enter Postal Code: ")
    PhoneNumber = input("Enter Phone Number: ")
    NumCars = int(input("Enter Number Of Cars: "))
    ExtraLiability = input("Extra Liability (Y/N): ").upper() == 'Y'
    GlassCoverage = input("Glass Coverage (Y/N): ").upper() == 'Y'
    LoanerCar = input("Loaner Car (Y/N): ").upper() == 'Y'
    DownPayment = 0.0
    if PaymentMethod == 'Down Pay':
        DownPayment = float(input("Enter Down Payment Amount: "))
    
    Claims = []
    while True:
        ClaimNumber = input("Enter Claim Number (or 'done' to finish): ")
        if ClaimNumber.lower() == 'done':
            break
        ClaimDate = input("Enter Claim Date (YYYY-MM-DD): ")
        ClaimAmount = float(input("Enter Claim Amount: "))
        Claims.append((ClaimNumber, ClaimDate, ClaimAmount))
    
    return {
        "FirstName": FirstName,
        "LastName": LastName,
        "Address": Address,
        "City": City,
        "Province": Province,
        "PostalCode": PostalCode,
        "PhoneNumber": PhoneNumber,
        "NumCars": NumCars,
        "ExtraLiability": ExtraLiability,
        "GlassCoverage": GlassCoverage,
        "LoanerCar": LoanerCar,
        "PaymentMethod": PaymentMethod,
        "DownPayment": DownPayment,
        "Claims": Claims
    }

# Generate Receipt

def GenerateReceipt(CustomerInfo, TotalPremium, HST, TotalCost, MonthlyPayment):
    print("\n--- Insurance Policy Receipt ---")
    print(f"Policy Number: {CustomerInfo['PolicyNumber']}")
    print(f"Name: {CustomerInfo['FirstName']} {CustomerInfo['LastName']}")
    print(f"Address: {CustomerInfo['Address']}, {CustomerInfo['City']}, {CustomerInfo['Province']}, {CustomerInfo['PostalCode']}")
    print(f"Phone: {CustomerInfo['PhoneNumber']}")
    print(f"Number of Cars: {CustomerInfo['NumCars']}")
    print(f"Extra Liability: {'Yes' if CustomerInfo['ExtraLiability'] else 'No'}")
    print(f"Glass Coverage: {'Yes' if CustomerInfo['GlassCoverage'] else 'No'}")
    print(f"Loaner Car: {'Yes' if CustomerInfo['LoanerCar'] else 'No'}")
    print(f"Payment Method: {CustomerInfo['PaymentMethod']}")
    print(f"Down Payment: {FormatValues(CustomerInfo['DownPayment'], True)}")
    print(f"Total Premium: {FormatValues(TotalPremium, True)}")
    print(f"HST: {FormatValues(HST, True)}")
    print(f"Total Cost: {FormatValues(TotalCost, True)}")
    if CustomerInfo['PaymentMethod'] != 'Full':
        print(f"Monthly Payment: {FormatValues(MonthlyPayment, True)}")
    print("\nPrevious Claims:")
    for Claim in CustomerInfo['Claims']:
        print(f"Claim #: {Claim[0]}  Date: {Claim[1]}  Amount: {FormatValues(Claim[2], True)}")
    print("\n----------------------------------\n")

# Main Program

if __name__ == "__main__":

    # Load constants

    Constants = LoadConstants()
    NextPolicyNumber = Constants['NextPolicyNumber']

    while True:
        CustomerInfo = GetUserInput(Constants)
        CustomerInfo['PolicyNumber'] = NextPolicyNumber

        TotalPremium = CalculatePremium(
            CustomerInfo['NumCars'],
            CustomerInfo['ExtraLiability'],
            CustomerInfo['GlassCoverage'],
            CustomerInfo['LoanerCar'],
            Constants
        )

        HST = TotalPremium * Constants['HSTRate']
        TotalCost = TotalPremium + HST

        if CustomerInfo['PaymentMethod'] == 'Monthly':
            MonthlyPayment = (TotalCost + Constants['MonthlyProcessingFee']) / 8
        elif CustomerInfo['PaymentMethod'] == 'Down Pay':
            MonthlyPayment = (TotalCost - CustomerInfo['DownPayment'] + Constants['MonthlyProcessingFee']) / 8
        else:
            MonthlyPayment = 0.0

        GenerateReceipt(CustomerInfo, TotalPremium, HST, TotalCost, MonthlyPayment)

        with open("PolicyData.txt", "a") as File:
            File.write(f"{CustomerInfo}\n")

        print("Saving policy data...")
        Total = 100
        for I in range(Total):
            ProgressBar(I + 1, Total, Prefix='Progress:', Suffix='Complete', Length=50)
        print("\nPolicy data saved successfully!")

        NextPolicyNumber += 1
        Constants['NextPolicyNumber'] = NextPolicyNumber
        f = open('Const.dat', 'w')
        for Key, Value in Constants.items():
            f.write(f"{Key}={Value}\n")
        f.close()

        if input("Would you like to enter another customer? (Y/N): ").upper() != 'Y':
            break


