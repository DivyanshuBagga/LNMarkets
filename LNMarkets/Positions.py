
import requests
from . import APIUrls

def getPositions(token, type = None):
    """
    Retrieves either opened, closed or all positions.

    Parameters-
    token: Authentication token.
    type: what kind of positions ('open' or 'closed' or 'all') to fetch (optional)

    """
    
    headers = {
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    if type == None:
        positionData = requests.get(APIUrls.lnapi+APIUrls.positionUrl,headers=headers)
        if positionData.status_code == 200:
            return positionData.json()
        else:
            raise RuntimeError('Unable to get positions')
    else:
        params = {"type":type}
        positionData = requests.get(APIUrls.lnapi+APIUrls.positionUrl,params = params,headers=headers)
        if positionData.status_code == 200:
            return positionData.json()
        else:
            raise RuntimeError('Unable to get positions: %s' % positionData.text)


def createPosition(token, type, side, leverage, margin=None, quantity=None, stoploss=None, takeprofit=None, price=None):
    """
    Send the order form parameters to add a new position in database. If type="l", the property price must be included in the request to know when the position should be filled. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you choosed.

    Parameters-
    token: Authentication token.
    type: "l" for limit order, "m" for market order.
    side: "b" for buy, "s" for sell.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    price: limit price for limit order. (optional)
    """
    if margin == None and quantity == None:
        raise ValueError('Either margin or quantity must be provided')
    if type == "l" and price == None:
        raise ValueError('Limit Price must be pprovided for limit order')

    payload = "{\"type\":\"%s\",\"side\":\"%s\",\"leverage\":%.2f" %(type, side, leverage)

    if type == "l":
        payload += ",\"price\":%.2f" % price
    if margin == None:
        payload += ",\"quantity\":%d" % quantity
    else:
        payload += ",\"margin\":%d" % margin
    if stoploss != None:
        payload += ",\"stoploss\":%.2f" % stoploss
    if takeprofit != None:
        payload += ",\"takeprofit\":%.2f" % takeprofit

    payload += "}"        
        
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    positionData = requests.post(APIUrls.lnapi+APIUrls.positionUrl,data=payload,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to create position: %s' % positionData.text)

def buy(token, leverage, margin=None, quantity=None, stoploss=None, takeprofit=None):
    """
    Send the buy order. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you choosed.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(token,"m","b",leverage,margin,quantity,stoploss,takeprofit)

def sell(token, leverage, margin=None, quantity=None, stoploss=None, takeprofit=None):
    """
    Send the sell order. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you choosed.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(token,"m","s",leverage,margin,quantity,stoploss,takeprofit)

def limitBuy(token, leverage, price, margin=None, quantity=None, stoploss=None, takeprofit=None):
    """
    Send the limit buy order. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you choosed.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    price: Limit price of order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(token,"l","b",leverage,margin,quantity,stoploss,takeprofit,price)

def limitSell(token, leverage, price, margin=None, quantity=None, stoploss=None, takeprofit=None):
    """
    Send the limit sell order. You can choose to use the margin or the quantity as a parameter, the other will be calculated with the one you choosed.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    price: Limit price of order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(token,"l","s",leverage,margin,quantity,stoploss,takeprofit,price)

def updatePosition(token, pid, type, value):
    """
    Allows user to modify stoploss or takeprofit parameters of an existing position.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    type: "takeprofit" or "stoploss".
    value: Price level to set.
    """

    payload = "{\"pid\":\"%s\",\"type\":\"%s\",\"value\":%.2f}" %(pid, type, value)
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    positionData = requests.put(APIUrls.lnapi+APIUrls.positionUrl,data=payload,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to update position %s, reason: %s' % (pid,positionData.text))

def closePosition(token, pid):
    """
    Close the user position, the PL will be calculated against the current bid or offer depending on the side of the position.
 
    Parameters-
    token: Authentication token.
    pid: ID of the position.
    """

    params = {"pid": pid}
    headers = {
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    positionData = requests.delete(APIUrls.lnapi+APIUrls.positionUrl,params=params,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to close position %s, reason: %s' % (pid,positionData.text))
        
def closeAllLongs(token):
    """
    Close all positions on long side.
 
    Parameters-
    token: Authentication token.
    """   

    positionData = getPositions(token, "open")['open']
    pl = 0.0
    for position in positionData:
        if position['side'] == "b" and not position['closed'] and not position['canceled']:
            closeData = closePosition(token, position['pid'])
            pl += float(closeData['pl'])

    return pl;

def closeAllShorts(token):
    """
    Close all positions on short side.
 
    Parameters-
    token: Authentication token.
    """   
    
    positionData = getPositions(token, "open")['open']
    pl = 0.0
    for position in positionData:
        if position['side'] == "s" and not position['closed'] and not position['canceled']:
            closeData = closePosition(token, position['pid'])
            pl += float(closeData['pl'])

    return pl;

def marginWithheld(openPositions):
    """
    Calculates the margin withheld in the open positions.

    Parameters-
    openPositions: Array of open positions.
    """
    totalMargin = 0.0
    for position in openPositions:
        totalMargin += float(position['margin'])

    return totalMargin

def calculateProfit(positions):
    """
    Calculates the total profit/loss from input positions.

    Parameters-
    positions: Array of positions.
    """
    totalProfit = 0.0
    for position in positions:
        totalProfit += float(position['pl'])

    return totalProfit

def realizedProfit(token):
    """
    Calculates the total profit/loss from closed positions.

    Parameters-
    token: Authentication token.
    """
    closedPositions = getPositions(token,"closed")['closed']
    return calculateProfit(closedPositions)

def unrealizedProfit(token):
    """
    Calculates the total profit/loss from open positions.

    Parameters-
    token: Authentication token.
    """
    openPositions = getPositions(token,"open")['open']
    return calculateProfit(openPositions)

def addMargin(token, pid, amount):
    """
    Adds margin to a running position.
 
    Parameters-
    token: Authentication token.
    pid: ID of the position.
    amount: amount to add in sats.
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"amount\":%d,\"pid\":\"%s\"}" % (amount,pid)
    positionData = requests.post(APIUrls.lnapi+APIUrls.addMarginUrl,data=payload,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to add margin to position %s, reason: %s' % (pid,positionData.text))

def cashin(token, pid, amount):
    """
    Retrieves part of a running position's profit.
 
    Parameters-
    token: Authentication token.
    pid: ID of the position.
    amount: amount to retrieve in sats.
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"amount\":%d,\"pid\":\"%s\"}" % (amount,pid)
    positionData = requests.post(APIUrls.lnapi+APIUrls.cashinnUrl,data=payload,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to cash-in position %s, reason: %s' % (pid,positionData.text))

def cancelPosition(token, pid):
    """
    Cancel the position linked to the given pid.Only works on positions that are not currently filled.
 
    Parameters-
    token: Authentication token.
    pid: ID of the position.
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"pid\":\"%s\"}" % pid
    positionData = requests.post(APIUrls.lnapi+APIUrls.cancelUrl,data=payload,headers=headers)
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError('Unable to cancel position %s, reason: %s' % (pid,positionData.text))
    
