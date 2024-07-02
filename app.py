# Module 1 content
# Transition from files to DBMS

import csv
import os.path
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

        for s_record in f_reader1:
            if s_record["Account_no"] == debit_account and int(s_record["Balance"]) > int(amount):  #CONDITION CHECK FOR ENOUGH BALANCE
                for r_record in f_reader2:
                    if r_record["Account_no"] == credit_account:

                        s_record["Balance"] = str(int(s_record["Balance"]) - int(amount))
                        temp.append(s_record)
                        f_writer.writerow({'Account1':s_record['Account_no'], 'Account2':r_record['Account_no'], 'Amount':amount, 'D/C':'D'})
                        r_record["Balance"] = str(int(r_record["Balance"]) + int(amount))
                        temp.append(r_record)
                        f_writer.writerow({'Account1': r_record['Account_no'], 'Account2': s_record['Account_no'], 'Amount': amount,'D/C': 'C'})
                        success = success + 1
                        break
        f_obj_Account1.seek(0)
        next(f_obj_Account1)
        for record in f_reader1:
            if record['Account_no'] != temp[0]['Account_no'] and record['Account_no'] != temp[1]['Account_no']:
                temp.append(record)
        # THE TRANSACTION OPERATIONS END HERE
    except:
        print('\nWrong input entered !!!')

    f_obj_Account1.close()
    f_obj_Account2.close()
    f_obj_Ledger.close()
    if success == 1:
        f_obj_Account = open('Accounts.csv', 'w+', newline='')
        f_writer = csv.DictWriter(f_obj_Account, fieldnames=col_name_Account)
        f_writer.writeheader()
        for data in temp:
            f_writer.writerow(data)
        f_obj_Account.close()
        print("\nTransaction is successfull !!")
    else:
        print('\nTransaction failed : Confirm Account details')

    t1 = time.time()
    print('\nTime Elapsed :  ', (t1-t0)*1000, 'millisec')


def main():
    end = 1
    print("===================================================================================")
    print("\nSchema of Accounts table :\n", col_name_Account)
    while end == 1:
        choice = int(input("\nFor adding a record to Account table Press 1\n" +
                           "For displaying all Transaction details Press 2\n" +
                           "For making a Fund Transfer Press 3\n"))

        if choice == 1:
            account_no = input("Enter Account number of the account holder : ")
            name = input("Enter Name of the account holder : ")
            address = input("Enter Address of the account holder : ")
            phone_no = input("Enter Phone_no of the account holder : ")
            pan = input("Enter PAN of the account holder : ")
            type = input("Enter A/C type : ")
            balance = input("Enter initial deposit amount ")

            add_Account(account_no,name,address,phone_no,pan,type,balance)
            print('\nAccount added successfully')

        elif choice == 2:
            account = input('Enter your account number : ')
            display_Transaction_History(account)

        elif choice == 3:
            debit_account = input('\nEnter your Account number : ')
            credit_account = input('\nEnter the Payee Account number : ')
            amount = input('\nEnter the amount to transfer : ')
            begin_Transaction(credit_account, debit_account, amount)

        else:
            print("\nIllegal input !!!")

        end = int(input("\nDo you want to continue ?, If Yes press 1 else press 0\n==>"))
        if end != 0 and end != 1:
            print("\nIllegal input !!!")
            exit()


main()