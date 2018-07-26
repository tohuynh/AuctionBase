import web

db = web.database(dbn='sqlite',
        #db='[YOUR SQLite DATABASE FILENAME]' #TODO: add your SQLite database filename
        db='auction.db'
    )

######################BEGIN HELPER METHODS######################

# Enforce foreign key constraints
# WARNING: DO NOT REMOVE THIS!
def enforceForeignKey():
    db.query('PRAGMA foreign_keys = ON')

# initiates a transaction on the database
def transaction():
    return db.transaction()
# Sample usage (in auctionbase.py):
#
# t = sqlitedb.transaction()
# try:
#     sqlitedb.query('[FIRST QUERY STATEMENT]')
#     sqlitedb.query('[SECOND QUERY STATEMENT]')
# except Exception as e:
#     t.rollback()
#     print str(e)
# else:
#     t.commit()
#
# check out http://webpy.org/cookbook/transactions for examples

# returns the current time from your database
def getTime():
    # TODO: update the query string to match
    # the correct column and table name in your database
    query_string = 'select cur_time from currenttime'
    results = query(query_string)
    # alternatively: return results[0]['currenttime']
    return results[0].cur_time # TODO: update this as well to match the
                                  # column name
    
# returns a single item specified by the Item's ID in the database
# Note: if the `result' list is empty (i.e. there are no items for a
# a given ID), this will throw an Exception!
def getItemById(item_id):
    # TODO: rewrite this method to catch the Exception in case `result' is empty
    query_string = 'select * from item where item_id = $item_id'
    #result = query(query_string, {'itemID': item_id})
    #return result[0]
    try:
        results = list(db.query(query_string, {'item_id': item_id}))
    except Exception as e:
        return False, str(e)
    else:
        if len(results) == 0:
            return False, 'No item with id: ' + item_id
        else:
            return True, 'Successfully found item: ' + item_id, results[0]

# wrapper method around web.py's db.query method
# check out http://webpy.org/cookbook/query for more info
def query(query_string, vars = {}):
    return list(db.query(query_string, vars))

#####################END HELPER METHODS#####################

#TODO: additional methods to interact with your database,
# e.g. to update the current time


def updateTime(selected_time):
    query_string = 'update currenttime set cur_time = $selected_time'
    t = transaction()
    try:
        db.query(query_string, {'selected_time': selected_time})
    except Exception as e:
        t.rollback()
        print str(e)
        return False, str(e)
    else:
        t.commit()
        print 'success update time'
        return True, 'Successfully changed current time.'
        
def addBid(item_id, bidder_id, amount):
    query_string = 'insert into bid values($item_id, $bidder_id, $time, $amount)'
    t = transaction()
    try:
        result = db.query(query_string, {'item_id': item_id, 'bidder_id': bidder_id, 'time': getTime(), 'amount': amount})
    except Exception as e:
        t.rollback()
        print str(e)
        return False, str(e)
    else:
        t.commit()
        return True, bidder_id + ' successfully bidded ' + amount + ' on item ' + item_id, result
        
def getItems(item_id, seller_id, category, description, minPrice, maxPrice, status):
    query_string = 'select distinct i.item_id, i.seller_id, i.name, i.ends, i.currently, i.buy_price from item i, category c where i.item_id = c.item_id'
    if item_id:
        query_string += ' and i.item_id = $item_id'
    if seller_id:
        query_string += ' and i.seller_id = $seller_id'
    if category:
        query_string += ' and c.category_name = $category'
    if description:
        query_string += ' and i.description like $description'
    if minPrice:
        query_string += ' and i.currently >= $minPrice'
    if maxPrice:
        query_string += ' and i.currently <= $maxPrice'
        
        
    cur_time = getTime();    
    if status == 'open':
        query_string += ' and i.ends > $cur_time and (i.buy_price is null or i.currently < i.buy_price)'
    elif status == 'close':
        query_string += ' and (i.ends <= $cur_time or (i.buy_price is not null and i.currently >= buy_price))'
    elif status == 'notStarted':
        query_string += ' and i.started > $cur_time'
    
    try:
        results = db.query(query_string, {'item_id': item_id, 'seller_id': seller_id, 'category': category, 'description': "%{0}%".format(description), 'minPrice': minPrice, 'maxPrice': maxPrice, 'cur_time': cur_time})
    except Exception as e:
        print str(e)
        return False, str(e)
    else:
        return True, 'Successfully items query', list(results)
        
def getCategories(item_id):
    query_string = 'select category_name from category where item_id = $item_id'
    try:
        results = db.query(query_string, {'item_id': item_id})
    except Exception as e:
        return False, str(e)
    else:
        return True, 'Successfully found categegories for '+ item_id, list(results)

def getBids(item_id):
    #query_string = 'select b.bidder_id, b.time, b.amount from item i, bid b where i.item_id = b.item_id and i.item_id = $item_id order by b.time desc'
    query_string = 'select * from bid where item_id = $item_id order by time desc'
    #results = list(db.query(query_string, {'item_id', item_id}))
    #return True, 'succ', results
    try:
        results = list(db.query(query_string, {'item_id': item_id}))
    except Exception as e:
        return False, str(e)
    else:
        if len(results) == 0:
            return False, 'No bids with item_id: ' + item_id
        else:
            return True, 'Successfully found bids for item_id: ' + item_id, results
        
def getStatus(item_id):
    result = getItemById(item_id)
    if result[0]:
        item = result[2]
        cur_time = getTime()
        if item['ends'] > cur_time and (item['buy_price'] is None or item['currently'] < item['buy_price']):
            status = 'Open'
        elif item['ends'] <= cur_time or (item['buy_price'] is not None and item['currently'] >= item['buy_price']):
            status  = 'Closed'
        else:
            status = 'Not started'
        
        if status == 'Closed':
            if item['number_of_bids'] > 0:
                status += ', Winning bid: ' + getBid(item['item_id'], item['currently'])
            else:
                status += ', No winning bid'
        
        return True, status
    else:
        return False, 'No item with id: ' + item_id
        
def getBid(item_id, currently):
    query_string = 'select bidder_id from bid where item_id = $item_id and amount = $currently'
    result = list(db.query(query_string, {'item_id': item_id, 'currently': currently}))
    return result[0]['bidder_id']