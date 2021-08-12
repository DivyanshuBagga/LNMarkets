
import requests
import json
from . import APIUrls


def getPositions(token, type_=None):
    """
    Retrieves either opened, closed or all positions.

    Parameters-
    token: Authentication token.
    type_: kind of positions ('open' or 'closed' or 'all') to fetch (optional)

    """
    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    if type_ is None:
        positionData = requests.get(
            APIUrls.lnapi+APIUrls.positionUrl,
            headers=headers,
        )
        if positionData.status_code == 200:
            return positionData.json()
        else:
            raise RuntimeError('Unable to get positions')
    else:
        params = {"type": type_}
        positionData = requests.get(
            APIUrls.lnapi+APIUrls.positionUrl,
            params=params,
            headers=headers,
        )
        if positionData.status_code == 200:
            return positionData.json()
        else:
            raise RuntimeError(f'Unable to get positions: {positionData.text}')


def createPosition(token, type_, side, leverage, margin=None, quantity=None,
                   stoploss=None, takeprofit=None, price=None):
    """
    Send the order form parameters to add a new position in database.
    If type_="l", the property price must be included in the request to know
    when the position should be filled. You can choose to use the margin or
    the quantity as a parameter, the other will be calculated with the one
    you selected.

    Parameters-
    token: Authentication token.
    type_: "l" for limit order, "m" for market order.
    side: "b" for buy, "s" for sell.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    price: limit price for limit order. (optional)
    """
    if margin is None and quantity is None:
        raise ValueError('Either margin or quantity must be provided')
    if type_ == "l" and price is None:
        raise ValueError('Limit Price must be pprovided for limit order')

    payloadDict = {
        'type': type_,
        'side': side,
        'leverage': leverage,
        }

    if type_ == "l":
        payloadDict['price'] = price
    if margin is None:
        payloadDict['quantity'] = quantity
    else:
        payloadDict['margin'] = margin
    if stoploss is not None:
        payloadDict['stoploss'] = stoploss
    if takeprofit is not None:
        payloadDict['takeprofit'] = takeprofit

    payload = json.dumps(payloadDict)
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    positionData = requests.post(
        APIUrls.lnapi+APIUrls.positionUrl,
        data=payload,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(f'Unable to create position: {positionData.text}')


def buy(token, leverage, margin=None, quantity=None, stoploss=None,
        takeprofit=None):
    """
    Send the buy order.
    You can choose to use the margin or the quantity as a parameter,
    the other will be calculated with the one you selected.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(
        token=token,
        type_="m",
        side="b",
        leverage=leverage,
        margin=margin,
        quantity=quantity,
        stoploss=stoploss,
        takeprofit=takeprofit,
    )


def sell(token, leverage, margin=None, quantity=None, stoploss=None,
         takeprofit=None):
    """
    Send the sell order.
    You can choose to use the margin or the quantity as a parameter,
    the other will be calculated with the one you selected.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(
        token=token,
        type_="m",
        side="s",
        leverage=leverage,
        margin=margin,
        quantity=quantity,
        stoploss=stoploss,
        takeprofit=takeprofit,
    )


def limitBuy(token, leverage, price, margin=None, quantity=None, stoploss=None,
             takeprofit=None):
    """
    Send the limit buy order.
    You can choose to use the margin or the quantity as a parameter,
    the other will be calculated with the one you selected.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    price: Limit price of order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(
        token=token,
        type_="l",
        side="b",
        leverage=leverage,
        margin=margin,
        quantity=quantity,
        stoploss=stoploss,
        takeprofit=takeprofit,
        price=price,
    )


def limitSell(token, leverage, price, margin=None, quantity=None,
              stoploss=None, takeprofit=None):
    """
    Send the limit sell order.
    You can choose to use the margin or the quantity as a parameter,
    the other will be calculated with the one you selected.

    Parameters-
    token: Authentication token.
    leverage: Leverage of the order.
    price: Limit price of order.
    margin: margin or quantity must be given (optional)
    quantity: margin or quantity must be given (optional)
    stoploss: StopLoss level. (optional)
    takeprofit: Profit taking level. (optional)
    """
    return createPosition(
        token=token,
        type_="l",
        side="s",
        leverage=leverage,
        margin=margin,
        quantity=quantity,
        stoploss=stoploss,
        takeprofit=takeprofit,
        price=price,
    )


def updatePosition(token, pid, type_, value):
    """
     Modifies stoploss or takeprofit parameters of an existing position.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    type: "takeprofit" or "stoploss".
    value: Price level to set.
    """

    payload = json.dumps({
        'pid': pid,
        'type': type_,
        'value': value,
        })
    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    positionData = requests.put(
        APIUrls.lnapi+APIUrls.positionUrl,
        data=payload,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(
            f'Unable to update position {pid},\n'
            f'reason: {positionData.text}'
        )


def closePosition(token, pid):
    """
    Close the user position,
    the PL will be calculated against the current bid or offer
    depending on the side of the position.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    """

    params = {
        "pid": pid,
    }
    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    positionData = requests.delete(
        APIUrls.lnapi+APIUrls.positionUrl,
        params=params,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(
            f'Unable to close position {pid},\n'
            f'reason: {positionData.text}'
        )


def isOpen(token, pid):
    """
    Checks if a position is open.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    """

    positionData = getPositions(token, "running")
    for position in positionData:
        if (position['pid'] == pid):
            return True

    return False


def closeAllLongs(token):
    """
    Close all positions on long side.

    Parameters-
    token: Authentication token.
    """

    positionData = getPositions(token, "running")
    pl = 0.0
    for position in positionData:
        if (
                position['side'] == "b" and
                not position['closed'] and
                not position['canceled']
        ):
            closeData = closePosition(token, position['pid'])
            pl += float(closeData['pl'])

    return pl


def closeAllShorts(token):
    """
    Close all positions on short side.

    Parameters-
    token: Authentication token.
    """

    positionData = getPositions(token, "running")
    pl = 0.0
    for position in positionData:
        if (
                position['side'] == "s" and
                not position['closed'] and
                not position['canceled']
        ):
            closeData = closePosition(token, position['pid'])
            pl += float(closeData['pl'])

    return pl


def closeAll(token):
    """
    Close all positions.

    Parameters-
    token: Authentication token.
    """

    headers = {
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    positionData = requests.delete(
        APIUrls.lnapi+APIUrls.closeAllUrl,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()['pl']
    else:
        raise RuntimeError(
            f'Unable to close all positions.\n'
            f'reason: {positionData.text}'
        )

    return pl


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

    closedPositions = getPositions(token, "closed")
    return calculateProfit(closedPositions)


def unrealizedProfit(token):
    """
    Calculates the total profit/loss from open positions.

    Parameters-
    token: Authentication token.
    """

    openPositions = getPositions(token, "running")
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
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    payload = json.dumps({
        'amount': amount,
        'pid': pid,
        })
    positionData = requests.post(
        APIUrls.lnapi+APIUrls.addMarginUrl,
        data=payload,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(
            f'Unable to add margin to position {pid},\n'
            f'reason: {positionData.text}'
        )


def cashin(token, pid, amount):
    """
    Retrieves part of a running position's profit.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    amount: amount to retrieve in sats.
    """

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f'Bearer {token}',
    }
    payload = json.dumps({
        'amount': amount,
        'pid': pid,
        })
    positionData = requests.post(
        APIUrls.lnapi+APIUrls.cashinUrl,
        data=payload,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(
            f'Unable to cash-in position {pid},\n'
            f'reason: {positionData.text}'
        )


def cancelPosition(token, pid):
    """
    Cancel the position linked to the given pid.
    Only works on positions that are not currently filled.

    Parameters-
    token: Authentication token.
    pid: ID of the position.
    """

    headers = {
        'Content-Type': "application/json",
        'Accept': "application/json",
        'Authorization': f"Bearer {token}",
    }
    payload = json.dumps({
        'pid': pid,
        })
    positionData = requests.post(
        APIUrls.lnapi+APIUrls.cancelUrl,
        data=payload,
        headers=headers,
    )
    if positionData.status_code == 200:
        return positionData.json()
    else:
        raise RuntimeError(
            f'Unable to cancel position {pid},\n'
            f'reason: {positionData.text}'
        )
