
import requests
from . import APIUrls

def userInformation(token):    
    """
    Get the user account Information.

    Parameters-
    token: Authentication token.
    """
    headers = {
    'accept': "application/json",
    'authorization': "Bearer %s" % token
    }
    userInfo = requests.get(APIUrls.lnapi+APIUrls.userUrl,headers=headers)
    if userInfo.status_code == 200:
        return userInfo.json()
    else:
        raise RuntimeError('Unable to get user information: %s' % userInfo.text)

def getBalance(token):
    """
    Get the user account balance.

    Parameters-
    token: Authentication token.
    """
    
    return userInformation(token)['balance']

def updateUser(token, leaderboard = None, showUsername = None, username = None):    
    """
    Update user account information.

    Parameters-
    token: Authentication token.
    leaderboard: True, if allowed to show user's profit on leaderboard.
    showUsername: True, if allowed to show the username on LN Marktes public data.
    username: username to display.
    """

    headers = {
    'content-type': "application/json",        
    'accept': "application/json",
    'authorization': "Bearer %s" % token
    }
    payload = "{"
    comma = False
    if showUsername != None:
        payload += "\"show_username\":%s" % str(showUsername).lower()
        comma = True
    if leaderboard != None:
        if comma:
            payload += ",\"show_leaderboard\":%s" % str(leaderboard).lower()
        else:
            payload += "\"show_leaderboard\":%s" % str(leaderboard).lower()
        comma = True
    if username == None:
        payload += "}"
    else:
        if comma:
            payload += ",\"username\":\"%s\"}" % username
        else:
            payload += "\"username\":\"%s\"}" % username

    userInfo = requests.put(APIUrls.lnapi+APIUrls.userUrl,data=payload,headers=headers)
    if userInfo.status_code == 200:
        return userInfo.json()
    else:
        raise RuntimeError('Unable to update user information: %s' % userInfo.text)


def updatePassword(token, previousPassword, newPassword):
    """
    Update user account information.

    Parameters-
    token: Authentication token.
    previousPassword: Previous Password.
    newPassword: New Password.
    """
    headers = {
    'content-type': "application/json",        
    'authorization': "Bearer %s" % token
    }
    payload="{\"previousPassword\":\"%s\",\"newPassword\":\"%s\"}" %(previousPassword,newPassword)

    updateInfo = requests.put(APIUrls.lnapi+APIUrls.updateUrl,data=payload,headers=headers)
    return updateInfo.ok

def getTransactions(token, type, nbitem=-1, index=1, getLength=False, start=None, end=None):    
    """
    Retrieves all withdraw or deposit you did with LN Markets or just one page

    Parameters-
    token: Authentication token.
    type: what kind of transactions ('withdraw' or 'deposit') to fetch
    nbitem: maximum length of returned table (optional)
    index: page offset (optional)
    getLength: Boolean. True if need length of date splice (optional)
    start: start of time interval (optional)
    end: end of time interval (optional)
    """

    headers = {
    'accept': "application/json",
    'authorization': "Bearer %s" % token
    }
    params = { "type": type, "getLength": str(getLength).lower()}
    if nbitem != -1:
        params['nbitem'] = nbitem
        params['index'] = index
    if start != None:
        params['start'] = start
    if end != None:
        params['end'] = end
        
    transactions = requests.get(APIUrls.lnapi+APIUrls.userHistoryUrl,headers=headers,params=params)
    if transactions.status_code == 200:
        return transactions.json()
    else:
        raise RuntimeError('Unable to get user transactions: %s' % transactions.text)

def getTokens():
    """
    Retrieves the list of active JSON Web Token user currently holds.
    """
    
    headers = {
    'accept': "application/json"
    }
        
    tokens = requests.get(APIUrls.lnapi+APIUrls.tokenUrl,headers=headers)
    if tokens.status_code == 200:
        return tokens.json()
    else:
        raise RuntimeError('Unable to get user tokens: %s' % tokens.text)

def revokeToken(token=None):
    """
    identifies and revoke usage of a given JWT.

    Parameters-
    token: Identifier of Token to be removed (optional)
    """
    
    if token == None:   
        tokenInfo = requests.delete(APIUrls.lnapi+tokenUrl)
    else:
        params = {"jti": token}
        tokenInfo = requests.delete(APIUrls.lnapi+APIUrls.tokenUrl,params=params)        
    if tokenInfo.status_code == 200:
        return True
    else:
        raise RuntimeError('Unable to revoke user token: %s' % tokenInfo.text)

def generateToken(expiry,deposit=False,withdraw=False,positions=False,user=False):
    """
    Using the given scopes, generate token to give access to different parts of the public API.

    Parameters-
    expiry: token expiry in seconds.
    deposit: Allow deposit (optional)
    withdraw: Allow withdraw (optional)
    positions: Allow opening or closing trade positions (optional)
    user: Allow access to user information (optional)
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json"
    }

    payload = "{\"expiry\":%d,\"scopes\":[" % expiry
    putComma = False
    if deposit:
        if putComma:
            payload+=","
        payload+="\"deposit\""
        putComma=True
    if withdraw:
        if putComma:
            payload+=","
        payload+="\"withdraw\""
        putComma=True
    if positions:
        if putComma:
            payload+=","
        payload+="\"positions\""
        putComma=True
    if user:
        if putComma:
            payload+=","
        payload+="\"user\""
        putComma=True
    payload+="]}"
    
    tokenInfo = requests.post(APIUrls.lnapi+APIUrls.tokenUrl,data=payload,headers=headers)        
    if tokenInfo.status_code == 200:
        return tokenInfo.json()['token']
    else:
        raise RuntimeError('Unable to generate user token: %s' % tokenInfo.text)

def deposit(token, amount, unit="sat"):
    """
    Add fund to your LN Markets balance.

    Parameters-
    token: Authentication token
    amount: amount to deposit
    unit: sat by default (optional)

    Returns-
    paymentRequest: Invoice to pay to add balanceto the account
    expiry: time in seconds before expiry of request
    """
    
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"amount\":%d,\"unit\":\"%s\"}" % (amount, unit)
    
    invoice = requests.post(APIUrls.lnapi+APIUrls.depositUrl,data=payload,headers=headers)
    if invoice.status_code == 200:
        return invoice.json()
    else:
        raise RuntimeError('Unable to get invoice: %s' % invoice.text)

def withdrawInvoice(token, amount, invoice, unit="sat"):
    """
    Move funds from the Lightning channel with LN Markets to user wallet by using an invoice directly.

    Parameters-
    token: Authentication token
    amount: amount to withdraw
    unit: Currently only sat (optional)
    invoice: BOLT 11 invoice with same amount

    Returns-
    wid: withdraw ID
    amount: amount withdrawn
    paymentSecret: Payment secret of settled invoice
    paymentHash: Payment hash of settled invoice
    """
    
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"amount\":%d,\"unit\":\"%s\",\"invoice\":\"%s\"}" % (amount,unit,invoice)
    
    payment = requests.post(APIUrls.lnapi+APIUrls.withdrawUrl,data=payload,headers=headers)
    if payment.status_code == 200:
        return payment.json()
    else:
        raise RuntimeError('Unable to make payment: %s' % payment.text)

def withdrawLNURL(token, amount, unit="sat"):
    """
    Move funds from the Lightning channel with LN Markets to user wallet by using an LNURL.

    Parameters-
    token: Authentication token
    amount: amount to withdraw
    unit: Currently only sat (optional)

    Returns-
    lnurl: LNURL BECH32 encoded string for wallet
    """
    
    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': "Bearer %s" % token
    }
    payload = "{\"amount\":%d,\"unit\":\"%s\"}" % (amount,unit)
    
    LNUrlInfo = requests.post(APIUrls.lnapi+APIUrls.withdrawLNUrl,data=payload,headers=headers)
    if LNUrlInfo.status_code == 200:
        return LNUrlInfo.json()
    else:
        raise RuntimeError('Unable to create LNURL: %s' % LNUrlInfo.text)
    
def login(username, password):
    """
    Use existing credentials to log in.
    """
    
    headers = {
        'content-type': "application/json",
        'accept': "application/json"
    }
    payload = "{\"login\":\"%s\",\"password\":\"%s\"}" % (username,password)
    loginResp = requests.post(APIUrls.lnapi+APIUrls.loginUrl,data=payload,headers=headers)
    if loginResp.status_code == 200:
        return loginResp.json()
    else:
        raise RuntimeError('Unable to login: %s' % loginResp.text)

def logout():
    """
    Deletes session cookie
    """

    return requests.post(APIUrls.lnapi+APIUrls.logoutUrl).ok

    
