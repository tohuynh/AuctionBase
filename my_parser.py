
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)
    
def transformQuote(str):
    return '"' + str.replace('"', '""') + '"'

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    item_file = open("item.dat", "a")
    user_file = open("user.dat", "a")
    category_file = open("category.dat", "a")
    bid_file = open("bid.dat", "a")
    
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            
            item_id = item["ItemID"]
            name = transformQuote(item["Name"])
            currently = transformDollar(item["Currently"])
            buy_price = 'NULL'
            if "Buy_Price" in item:
                buy_price = transformDollar(item["Buy_Price"])
            first_bid = transformDollar(item["First_Bid"])
            number_of_bids = item["Number_of_Bids"]
            started = transformDttm(item["Started"])
            ends = transformDttm(item["Ends"])
            
            seller = item["Seller"]
            seller_id = transformQuote(seller["UserID"])
            seller_rating = seller["Rating"]
            seller_location = transformQuote(item["Location"])
            seller_country = transformQuote(item["Country"])
            description = 'NULL'
            if item["Description"] != None:
                descriptionn = transformQuote(item["Description"])
            
            # item_id|name|currently|buy_price|first_bid|number_of_bids|started|ends|description|seller_id
            item_file.write(item_id+columnSeparator
                +name+columnSeparator
                +currently+columnSeparator
                +buy_price+columnSeparator
                +first_bid+columnSeparator
                +number_of_bids+columnSeparator
                +started+columnSeparator
                +ends+columnSeparator
                +descriptionn+columnSeparator
                +seller_id+"\n"
            )
            
            #user_id|rating|location|country
            user_file.write(seller_id+columnSeparator
                +seller_rating+columnSeparator
                +seller_location+columnSeparator
                +seller_country+"\n"
            )
            
            #category = item["Category"]
            #item_id|category_name
            for category in item["Category"]:
                category_file.write(item_id+columnSeparator
                    +transformQuote(category)+"\n")
                
            #bids = item["Bids"]
            if item["Bids"] != None:
                for bid in item["Bids"]:
                    bidder_id = transformQuote(bid["Bid"]["Bidder"]["UserID"])
                    bid_time = transformDttm(bid["Bid"]["Time"])
                    bid_amount = transformDollar(bid["Bid"]["Amount"])
                    bidder_rating = bid["Bid"]["Bidder"]["Rating"]
                    bidder_location = 'NULL'
                    if "Location" in bid["Bid"]["Bidder"]:
                        bidder_location = transformQuote(bid["Bid"]["Bidder"]["Location"])
                    bidder_country = 'NULL'
                    if "Country" in bid["Bid"]["Bidder"]:
                        bidder_country = transformQuote(bid["Bid"]["Bidder"]["Country"])
                        
                    user_file.write(bidder_id+columnSeparator
                        +bidder_rating+columnSeparator
                        +bidder_location+columnSeparator
                        +bidder_country+"\n"
                    )
                    
                    #item_id|bidder_id|time|amount
                    bid_file.write(item_id+columnSeparator
                        +bidder_id+columnSeparator
                        +bid_time+columnSeparator
                        +bid_amount+"\n"
                    )
    
    item_file.close()
    user_file.close()
    category_file.close()
    bid_file.close()
    
"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)
    # loops over all .json files in the argument
    for f in argv[1:]:
        if isJson(f):
            parseJson(f)
            print "Success parsing " + f

if __name__ == '__main__':
    main(sys.argv)
