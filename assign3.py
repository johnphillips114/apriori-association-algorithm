# This is my association rule mining algorithm implementation for my
# Data Mining course CSCI4144 at Dalhousie for Winter 2018.

import sys
import assign3_functions as a3f

#this flag is turned to True if the user enters an invalid input
flag = False

dataInput = input("What is the name of the file containing your data?")
dataPath = "./{}".format(dataInput)
flag = False

# Ensure the user enters a valid support rate
minSup = float(input("Please enter the minimum support rate (0.00-1.00):"))
if(minSup < 0) or (minSup > 1):
    flag = True
    while(flag == True):
        minSup = float(input("Invalid input. Please enter the minimum support rate (0.00-1.00):"))
        if(minSup >= 0) and (minSup <= 1):
            flag = False

# Ensure the user enters a valid confidence rate
minCon = float(input("Please enter the minimum confidence rate (0.00-1.00):"))
if(minCon < 0) or (minCon > 1):
    flag = True
    while(flag == True):
        minCon = float(input("Invalid input. Please enter the minimum confidence rate (0.00-1.00):"))
        if(minCon >= 0) and (minCon <= 1):
            flag = False

itemSet, transactionList = a3f.loadDB(dataPath)

firstItemSet = a3f.buildFirstItemset(transactionList, itemSet, minSup)

#twoItemCandidates = a3f.generateCandidates(2, transactionList, firstItemSet)
twoItemFrequents = a3f.genFrequentKItemset(transactionList, firstItemSet, minSup, 2)
threeItemFrequents = a3f.genFrequentKItemset(transactionList, twoItemFrequents, minSup, 3)
fourItemFrequents = a3f.genFrequentKItemset(transactionList, threeItemFrequents, minSup, 4)
fiveItemFrequents = a3f.genFrequentKItemset(transactionList, fourItemFrequents, minSup, 3)

#Merge all frequent items into a single dictionary
allFrequentItems = {**firstItemSet, **twoItemFrequents, **threeItemFrequents, **fourItemFrequents, **fiveItemFrequents}

#Create rules based on the frequent item itemsets
rules = a3f.createRules(allFrequentItems, minSup, minCon)
print(rules)

#output the rules for the specified output format
result = a3f.outputRules(rules)
