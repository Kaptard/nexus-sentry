import re
import request


# Syntax Variables
TOcount = 0
TOval = []
ITEMcount = 0
ITEMval = []
ITEMessential = ''
ITEMcomponent = ''

# Trade Operators
WTS = ['WTS', 'WTSELL', 'S', 'SELLING', 'SELL']
WTB = ['WTB', 'WTBUY', 'B', 'BUYING', 'BUY']
PC = ['PC', 'CHECK', 'CHECKING', 'PRICECHECK', 'PRICING', 'MUCH'] #dont use 'PRICE' -> PM Price rather common
TOlist = ['WTS', 'WTB', 'PC']

# Define component variations
Blueprint = ['BLUEPRINT', 'BP']
Systems = ['SYSTEMS', 'SYSTEM', 'SYS']
Chassis = ['CHASSIS', 'CHAS']
Neuroptics = ['NEUROPTICS', 'HELMET', 'HELM']
CompParts = ['Blueprint', 'Systems', 'Chassis', 'Neuroptics']



# Get username from first item in array
def getUsername(stringArr):
    if len(stringArr) > 0:
        Username = stringArr[0]
    else:
        Username = ''

    return(Username)



# Check if given string is TO, then return type
def getTradeOperator(string):
    if string in WTS:
        TO = 'Selling'
    elif string in WTB:
        TO = 'Buying'
    #elif string in PC:
    #    TO = 'PC'
    else:
        TO = None
    return(TO)



# Match the given item against those stored in database
def getItem(requested, stored):
    dbName = ItemJSON[j]["name"].upper()
    dbType = ItemJSON[j]["type"].upper()
    dbComp = [each.upper() for each in ItemJSON[j]["components"]]



# Get Item + Components (i+3 further)
def getRequest(i, stringArr, ItemJSON, TOcount, TOval):

    if TOcount > 0:
        TO = TOval[TOcount - 1]
    else:
        TO = ''

    ItemID = ''
    ItemComp = ''
    ItemType = ''
    ItemPrice = 'null'
    ItemCount = 1
    ItemRank = 1
    Request = [] # Create Array to fill later


    # Check if string matches any ID
    for j in range(0, len(ItemJSON)):

        # If string in Message matches
        if matchString(stringArr[i], dbID):

            # If ID > 1: check if follow-up words match
            if len(dbIDwords) > 1:
                for k in range(0, len(dbIDwords) - 1):

                    if i + k + 1 < len(stringArr) and not stringArr[i + k + 1] == dbIDwords[k + 1]:
                        break # Don't check further

                    if i + k + 1 < len (stringArr) and k + 1 == len(dbIDwords) - 1:
                        ItemID = dbID
                        ItemType = dbType
                        i = i + k + 1 # Jump to words behind identified item


            # ID has only one word
            else:
                ItemID = dbID
                ItemType = dbType


            # Append Alternatives to Components
            dbComp = appendComponents(dbComp)


            # Check if Components in messages i + 5
            for y in range(0, 6):

                if i + y <= len(stringArr):

                    # is contained in component list?
                    if stringArr[i + y - 1] in dbComp:
                        ItemComp = stringArr[i + y - 1]

                        # Convert Component name to standard if alt is used
                        for u in range(0, len(CompParts)):
                            CompCheckList = eval(CompParts[u])

                            if ItemComp in CompCheckList:
                                ItemComp = CompParts[u].upper()


                    # has number?
                    if hasNumbers(stringArr[i + y - 1]) == True:

                        # if x found: Probably Count
                        if 'X' in stringArr[i + y - 1]:
                            ItemCount = re.sub("\D", "", stringArr[i + y - 1])

                        # if R found: Probably Rank
                        elif 'R' in stringArr[i + y - 1]:
                            ItemRank = re.sub("\D", "", stringArr[i + y - 1])

                        # else price is detected
                        else:
                            ItemPrice = re.sub("\D", "", stringArr[i + y - 1])


            break # stop matching further entries


    # If no components -> set
    if ItemComp == '':
        ItemComp = 'SET'

    # Extend Request Array and return
    Request.extend((TO, ItemID, ItemComp, ItemType, ItemPrice, ItemCount, ItemRank))
    return(Request)



# Checks every component in DB if contained in alt. Versions. Then appends alt. list.
def appendComponents(array):
    for i in range(0, len(array)):

        for u in range(0, len(CompParts)):
            CompList = eval(CompParts[u])

            if array[i] in CompList:
                array.extend(CompList)

    return(array)








# Check if str contains number (for price/count)
def hasNumbers(string):
    return any(char.isdigit() for char in string)



# Check if string contains full word
def matchString(string1, string2):
   if re.search(r"\b" + re.escape(string1) + r"\b", string2):
      return True
   return False
