# Module 1 content
# Transition from files to DBMS

import csv # Importing the csv module to read and write the csv files
import os.path  # Importing the os module to check if the file is already present or not
from os import path
import time

# Schema of Student table
col_name_Account = ['Account_no', 'Name', 'Address', 'Phone_no', 'PAN', 'A/C type', 'Balance'] # Schema of Account table in csv
col_name_Ledger = ['Account1', 'Account2', 'Amount', 'D/C'] # Schema of Ledger table in csv format  
if path.exists('.\\Accounts.csv') == False and path.exists('.\\Ledger.csv') == False: # Checking if the files are already present or not 
    f_ob = open('Accounts.csv', 'a+') # Creating a new file for Account table if not present  
    f_wr = csv.DictWriter(f_ob, fieldnames=col_name_Account)  # Writing the schema to the file
    f_wr.writeheader() # Writing the header to the file  
    f_ob.close() # Closing the file  
    f_ob = open('Ledger.csv', 'a+') # Creating a new file for Ledger table if not present   
    f_wr = csv.DictWriter(f_ob, fieldnames=col_name_Ledger) # Writing the schema to the file 
    f_wr.writeheader() # Writing the header to the file
    f_ob.close() # Closing the file     


# utility methods for the operations on the tables 
def add_Account(account_no, name, address, phone_no, pan, type, balance): # Method to add a record to the Account table  
    f_obj = open('Accounts.csv', 'a+') # Opening the file in append mode because we need to add a record to the table
    f_writer = csv.DictWriter(f_obj, fieldnames=col_name_Account) # Writing the schema to the file and dictwriter is used to write the data in dictionary format
    f_writer.writerow({'Account_no':account_no, 'Name': name, 'Address': address, 'Phone_no': phone_no, 
                       'PAN': pan, 'A/C type':type, 'Balance':balance}) # Writing the record to the file            
    f_obj.close() # Closing the file after writing the record to the file 


def display_Transaction_History(account_no): # Method to display the transaction history of an account holder 
    f_obj = open('Ledger.csv', 'r') # Opening the file in read mode because we need to read the records from the file
    f_reader = csv.DictReader(f_obj) # Reading the file in dictionary format  
    print("\n") # Printing a new line   
    for record in f_reader: # Iterating through the records in the file  
        if record['Account1'] == account_no or record['Account1'] == account_no: # Checking if the account number is present in the record  and printing the record if present
            print(record)
    f_obj.close()


def begin_Transaction(credit_account, debit_account, amount): # Method to begin the transaction between two accounts  and updating the records in the Account table
    t0=time.time() # Starting the timer to calculate the time taken for the transaction 
    temp = [] # Temporary list to store the records of the Account table
    success = 0 # Variable to check if the transaction is successful or not

    # OPENING FILES TO STORE TRANSACTION DATA
    f_obj_Account1 = open('Accounts.csv', 'r') # Opening the file in read mode because we need to read the records from the file
    f_reader1 = csv.DictReader(f_obj_Account1) # Reading the file in dictionary format 
    f_obj_Account2 = open('Accounts.csv', 'r') # Opening the file in read mode because we need to read the records from the file
    f_reader2 = csv.DictReader(f_obj_Account2) # Reading the file in dictionary format
    f_obj_Ledger = open('Ledger.csv', 'a+') # Opening the file in append mode because we need to add a record to the table
    f_writer = csv.DictWriter(f_obj_Ledger, fieldnames=col_name_Ledger) # Writing the schema to the file and dictwriter is used to write the data in dictionary format
    try:
        #THE TRANSACTION OPERATIONS BEGINS HERE :

        for s_record in f_reader1: #ITERATING THROUGH THE ACCOUNTS FILE TO CHECK FOR ACCOUNTS  AND BALANCE 
            if s_record["Account_no"] == debit_account and int(s_record["Balance"]) > int(amount):  #CONDITION CHECK FOR ENOUGH BALANCE
                for r_record in f_reader2: #ITERATING THROUGH THE ACCOUNTS FILE TO CHECK FOR ACCOUNTS  AND BALANCE
                    if r_record["Account_no"] == credit_account: #CONDITION CHECK FOR ACCOUNT NUMBER MATCH FOR CREDIT ACCOUNT

                        s_record["Balance"] = str(int(s_record["Balance"]) - int(amount)) #UPDATING THE BALANCE OF DEBIT ACCOUNT after transaction 
                        temp.append(s_record)
                        f_writer.writerow({'Account1':s_record['Account_no'], 'Account2':r_record['Account_no'], 'Amount':amount, 'D/C':'D'}) #WRITING THE TRANSACTION RECORD TO LEDGER FILE  
                        r_record["Balance"] = str(int(r_record["Balance"]) + int(amount)) #updating the balance of credit account after transaction
                        temp.append(r_record) #appending the record to the temporary list 
                        f_writer.writerow({'Account1': r_record['Account_no'], 'Account2': s_record['Account_no'], 'Amount': amount,'D/C': 'C'})
                        success = success + 1 #incrementing the success variable to indicate the success of the transaction 
                        break #breaking the loop if the record is found  
        f_obj_Account1.seek(0) #setting the file pointer to the beginning of the file 
        next(f_obj_Account1) #skipping the header of the file 
        for record in f_reader1: #iterating through the records in the file   
            if record['Account_no'] != temp[0]['Account_no'] and record['Account_no'] != temp[1]['Account_no']: #checking if the record is not the one which is updated
                temp.append(record) #appending the record to the temporary list 
        # THE TRANSACTION OPERATIONS END HERE
    except:
        print('\nWrong input entered !!!') #printing the error message if the input is wrong  

    f_obj_Account1.close() #closing the file after reading the records from the file 
    f_obj_Account2.close() #closing the file after reading the records from the file
    f_obj_Ledger.close() #closing the file after writing the records to the file
    if success == 1: #checking if the transaction is successful or not  
        f_obj_Account = open('Accounts.csv', 'w+', newline='') #opening the file in write mode because we need to write the records to the file
        f_writer = csv.DictWriter(f_obj_Account, fieldnames=col_name_Account) #writing the schema to the file and dictwriter is used to write the data in dictionary format
        f_writer.writeheader() #writing the header to the file 
        for data in temp: #iterating through the records in the temporary list 
            f_writer.writerow(data) #writing the record to the file 
        f_obj_Account.close() #closing the file after writing the records to the file
        print("\nTransaction is successfull !!") #printing the success message if the transaction is successful
    else: #if the transaction is not successful 
        print('\nTransaction failed : Confirm Account details') #printing the error message if the transaction is not successful

    t1 = time.time() #ending the timer to calculate the time taken for the transaction
    print('\nTime Elapsed :  ', (t1-t0)*1000, 'millisec') #printing the time taken for the transaction in milliseconds


def main(): #main method to run the program  
    end = 1 #variable to check if the user wants to continue or not 
    print("===================================================================================") #printing the header of the program  
    print("\nSchema of Accounts table :\n", col_name_Account) #printing the schema of the Account table
    while end == 1: #checking if the user wants to continue or not
        choice = int(input("\nFor adding a record to Account table Press 1\n" + 
                           "For displaying all Transaction details Press 2\n" +
                           "For making a Fund Transfer Press 3\n")) #taking the choice from the user to perform the operation 1 for  adding a record, 2 for displaying the transaction history, 3 for making a fund transfer

        if choice == 1: #if the choice is 1 then add a record to the Account table 
            account_no = input("Enter Account number of the account holder : ") #taking the input from the user for the record to be added to the table
            name = input("Enter Name of the account holder : ") #taking the input from the user for the record to be added to the table 
            address = input("Enter Address of the account holder : ") #taking the input from the user for the record to be added to the table
            phone_no = input("Enter Phone_no of the account holder : ") #taking the input from the user for the record to be added to the table
            pan = input("Enter PAN of the account holder : ") #taking the input from the user for the record to be added to the table
            type = input("Enter A/C type : ") #taking the input from the user for the record to be added to the table 
            balance = input("Enter initial deposit amount ") #taking the input from the user for the record to be added to the table

            add_Account(account_no,name,address,phone_no,pan,type,balance) #calling the method to add the record to the Account table 
            print('\nAccount added successfully')

        elif choice == 2: #if the choice is 2 then display the transaction history of an account holder
            account = input('Enter your account number : ')
            display_Transaction_History(account) #calling the method to display the transaction history of an account holder

        elif choice == 3: #if the choice is 3 then make a fund transfer between two accounts
            debit_account = input('\nEnter your Account number : ')
            credit_account = input('\nEnter the Payee Account number : ')
            amount = input('\nEnter the amount to transfer : ')
            begin_Transaction(credit_account, debit_account, amount) #calling the method to begin the transaction between two accounts

        else: #if the input is wrong then print the error message 
            print("\nIllegal input !!!") #printing the error message if the input is wrong

        end = int(input("\nDo you want to continue ?, If Yes press 1 else press 0\n==>")) #asking the user if he wants to continue or not
        if end != 0 and end != 1: #checking if the input is wrong or not 
            print("\nIllegal input !!!")  #printing the error message if the input is wrong
            exit() #exiting the program if the input is wrong 


main() #calling the main method to run the program 