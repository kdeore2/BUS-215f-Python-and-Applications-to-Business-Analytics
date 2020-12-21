# Assignment 2: 
# Kunal Deore
# 
# -------------------------------------------
#

# Importing the libraries
import csv 
import math
from prettytable import PrettyTable

# Importing the statistics module 
import statistics 
from statistics import stdev 

# Exercise 1: Amortization
# Get all inputs from the user such as principal, minimum expected payment, interest and extra payment

# Get input for principal from user and error check it 
while True:
    try:
        principal = float(input("Please enter the principal amount for the loan: "))
        '''
        Making sure that principal is not negative and asking user repeatedly to enter a valid positive amount
        '''
        if not principal < 0:
            print(f"The principal amount is: ${principal} \n")
            break
    except ValueError:
        print("Please enter a valid amount in numeric! \n")
        
# Get input for minimum expected payment from user and error check it 
while True:
    try:
        min_expected_payment = float(input("Please enter the minimum expected payment for the loan:  \n"))
        '''
        Making sure that minimum expected payment is not negative and also 
        asking user repeatedly to enter a valid positive amount
        '''
        if not min_expected_payment < 0:
            '''
            Making sure that minimum expected payment is less than principal and
            also asking user repeatedly to enter a valid positive amount.
            '''
            if min_expected_payment > principal:
                print("The amount needs to be less than principal:  \n")
            else: 
                print(f"The minimum expected payment is: ${min_expected_payment}  \n")
                break
    except ValueError:
        print("Please enter a valid amount in numeric!  \n")

# Get input for interest rate from user and error check it         
while True:
    try:
        interest_rate = float(input("Please enter the interest rate in percentage:  \n"))
        '''
        Making sure that minimum expected payment is not negative, not greater than 100,
        and asking user repeatedly to enter a valid positive amount
        '''  
        if not interest_rate < 0 and not interest_rate > 100:
            print(f"The interest rate is: {interest_rate}%  \n")
            break
    except ValueError:
        print("Please enter a valid amount in numeric!  \n")
        
# Get input for extra payment from user and error check it 
while True:
    try:
        extra_payment = float(input("Please enter the extra payment amount for the loan:  \n"))
        '''
        Making sure that extra payment is not greater than principal and
        asking user repeatedly to enter a valid positive amount
        '''
        if not extra_payment < 0 and not extra_payment > principal:
            print(f"The expected amount is: ${extra_payment}  \n")
            break
    except ValueError:
        print("Please enter a valid amount in numeric!  \n")
        
# Settings global variables for the exercise 
total_payment = 0
total_interest_payment = 0
total_p_applied = 0
month = 0

# Use of prettytable package to create a table for the payment schedule:
x = PrettyTable(["Month", "Begin P", "Payment", "Interest", "Extra Payment", "P Applied", "End P"])

while principal > 0:
    month += 1
    begin_p = principal
    total_payment += min_expected_payment
    interest = (principal * (interest_rate/100)) / 12
    total_interest_payment += interest
    p_applied = min_expected_payment + extra_payment - interest
    '''
    Once end_p is greater than p_applied activate this chunk of code, 
    print the output and stop the loop
    '''
    if begin_p - p_applied < p_applied:
        total_p_applied += end_p
        end_p = 0
        # Add row     
        x.add_row([round(month), round(begin_p, 2), round(min_expected_payment, 2), round(interest, 2), 
                   round(extra_payment, 2), round(p_applied, 2), round(end_p, 2)]) 
        break    
    total_p_applied += p_applied
    end_p = begin_p - p_applied
    # Assign the end_p to principal so that loop can run again until principal is less than zero
    principal = end_p   
    # Print the output in a proper format and run the loop
    x.add_row([round(month), round(begin_p, 2), round(min_expected_payment, 2), round(interest, 2), 
               round(extra_payment, 2), round(p_applied, 2), round(end_p, 2)])   


# # Print the total output for payment, interest payment and p_applied  
x.add_row(["TOTAL", "-", round(total_payment, 2), round(total_interest_payment, 2),
           "-", round(total_p_applied, 2), "-"])
x.hrules = 1
print(x.get_string(title = "Amortization"))
    
# Print a newline 
print('\n')

# Print the total duration of the loan
print(f'The total duration of loan is {int(month/12):.0f} years and {month%12} months.')

# Exercise 2: Rolling Statistics
def read_file(filename, date_index, field_index, has_header = True):
    '''
    Reads a csv file and parses the content field into a time series.
    Input:
    filename: csv filename
    date_index: zero-based index of the time series date field
    field_index: zero-based index of the times series content field
    has_header: True or False on whether the file contents has a header row 
    Output:
    time_series: list of tuples with tuple consisting of (date, content field)
    '''
    time_series = []
    with open (filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        if has_header:
            next(reader, None)
        for row in reader:
            time_series.append((row[date_index], float(row[field_index])))
        return time_series

def main():
    # Open and read file to populate date and adjusted_close
    filename = 'GOOG.csv'
    ts = read_file(filename, 0, 5)
    # Print the total no of rows in the .csv file
    print(f'{filename} has been read with {len(ts)} daily prices')
    # Assigning the total no of rows to the variable total
    total = len(ts)
    # Get the size of the window from the user
    while True:
        try:
            r_s = int(input("Please enter the size of rolling window:  \n"))
            if not r_s <= 0 and not r_s == 1 and r_s < len(ts):
                print("You have entered a valid window size! \n")
                break
        except ValueError:
            print("Please enter a valid amount in numeric!  \n")
            
    # Use of prettytable package to create a table for rolling window statistics:
    x = PrettyTable(["Date", "Range", "Mean P", "Median", "Std_Dev"])
    
    # Unzip the columns to list
    date, adj_r_s = list(zip(*ts))
    date = list(date)
    adj_r_s = list(adj_r_s)
    # Compute the statistics using a loop
    for i in range(0, len(date)):
        date_r_s = date[i]
        # Based on user window size, extract the elements and compute the statistics
        list_r_s = []
        # Check if the window size is same else or else change the extraction to less than window size
        for i in range(r_s):
            if len(adj_r_s) >= r_s:
                list_r_s.append(adj_r_s[i])
            else:
                break
        if len(adj_r_s) < r_s:
            for j in range(len(adj_r_s)):
                list_r_s.append(adj_r_s[j])
        range_r_s = max(list_r_s) - min(list_r_s)
        mean_r_s = statistics.mean(list_r_s)
        median_r_s = statistics.median(list_r_s)
        # If list is equal to 1 make standard deviation to 0
        if len(list_r_s) > 1:
            std_r_s = statistics.stdev(list_r_s)
        else:
            std_r_s = 0
        x.add_row([date_r_s, round(range_r_s, 2), round(mean_r_s, 2), 
                   round(median_r_s, 2),round(std_r_s, 2)])
        adj_r_s.pop(0)
    print(x.get_string(title = "Rolling Statistics"))

    

if __name__ == '__main__':
    main()  