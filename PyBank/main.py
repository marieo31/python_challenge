# -*- coding: utf-8 -*-

"""
date: 2018-09-01
author: Marie-Océane
description: In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. You will give a set of financial data called budget_data.csv. The dataset is composed of two columns: Date and Profit/Losses. (Thankfully, your company has rather lax standards for accounting so the records are simple.)
Your task is to create a Python script that analyzes the records to calculate each of the following:
-> The total number of months included in the dataset
-> The total net amount of "Profit/Losses" over the entire period
-> The average change in "Profit/Losses" between months over the entire period
-> The greatest increase in profits (date and amount) over the entire period
-> The greatest decrease in losses (date and amount) over the entire period
In addition, your final script should both print the analysis to the terminal and export a text file with the results.
"""
import csv
import logging
import numpy as np

# Initialation and parameters
#----------------------------
csvpath = "budget_data.csv"     #path to the csv file
nb_month = 0        # nb of month included in the dataset
total = 0           # total net amount of profit/losses over the entire period
months = []         # list of the months
profits_losses = [] # list of the profits/losses
changes = []        # changes

# Logging set-up
#---------------
# this will allow us to write in a text-file and in the terminal at the same time
logfile = "results.txt"
open(logfile, 'w').close()  #to delete the existing content of the file
# we only need to set up the INFO level
level = logging.INFO
format = '%(message)s'
handlers = [logging.FileHandler(logfile), logging.StreamHandler()]
logging.basicConfig(level = level, format = format, handlers = handlers)

# Reading and processing the csv data
#-------------------------------------
with open(csvpath, newline='',encoding='utf-8') as csvfile:
    #open the csvfile
    csvreader = csv.reader(csvfile, delimiter=',')
    #skip the header line
    next(csvreader,None)    
    #looping on each row
    for row in csvreader:
        # Append the months and profit/losses lists
        months.append(row[0])
        profits_losses.append(float(row[1]))
        #Incrementing the number of months and the total amount of profits/losses
        nb_month += 1
        total = total + float(row[1])

# Calculating the changes
#------------------------
changes = [a2 - a1 for a2, a1 in zip(profits_losses[1:], profits_losses)]
# for ii in range(1,len(profits_losses)):    
#     changes.append(profits_losses[ii] - profits_losses[ii-1])

        
# Printing the total number of months and profit/losses into the logfile
#-----------------------------------------------------------------------
logging.info('Financial Analysis')
logging.info('-------------------')
logging.info("Total Months: %i"%(nb_month))
logging.info("Total: $%.1f"%(total))

# Calculate the Average change and finding the extreme values
#------------------------------------------------------------
avg = np.mean(changes)
# Top profit month and value (strored in a tuple)
top_profit = max(zip(months[1:],changes),key=lambda x:x[1])
# top_profit2 = ( months[np.argmax(changes)+1], np.max(changes))

# same for the top loss
top_loss = min(zip(months[1:],changes),key=lambda x:x[1])
# top_loss2 = (months[np.argmin(profits_losses)], np.min(profits_losses))


# Printing the avg and extreme values into the log file
#------------------------------------------------------
logging.info("Average Change: $%.2f"%(avg))
logging.info("Greatest Increase in Profits: %s ($%.1f)"%(top_profit))
logging.info("Greatest Decrease in Profits: %s ($%.1f)"%(top_loss))
logging.info("")
