
import requests
import json
from . import APIUrls


def userInformation(token):
    """
    Get the user account Information.

    Parameters-
    token: Authentication token.
    """
    headers = {
        'accept': "application/json",
        'authorization': f"Bearer {token}",
    }
    userInfo = requests.get(
        APIUrls.lnapi+APIUrls.userUrl,
        headers=headers,
    )
    if userInfo.status_code == 200:
        return userInfo.json()
    else:
        raise RuntimeError(
            'Unable to get user information:\n'
            f'{userInfo.text}'
        )


def getBalance(token):
    """
    Get the user account balance.

    Parameters-
    token: Authentication token.
    """

    return userInformation(token)['balance']


def updateUser(token, leaderboard=None, showUsername=None, username=None):
    """
    Update user account information.

    Parameters-
    token: Authentication token.
    leaderboard: True to show user's profit on leaderboard.
    showUsername: True to show the username on LN Marktes public data.
    username: username to display.
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
        'authorization': f"Bearer {token}",
    }
    payloadDict = dict()
    if showUsername is not None:
        payloadDict['show_username'] = showUsername
    if leaderboard is not None:
        payloadDict['show_leaderboard'] = leaderboard
    if username is not None:
        payloadDict['username'] = username
    payload = json.dumps(payloadDict)
    userInfo = requests.put(
        APIUrls.lnapi+APIUrls.userUrl,
        data=payload,
        headers=headers,
    )
    if userInfo.status_code == 200:
        return userInfo.json()
    else:
        raise RuntimeError(
            'Unable to update user information:\n'
            f'{userInfo.text}'
            )


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
        'authorization': f"Bearer {token}",
    }
    payload = json.dumps({
        'previousPassword': previousPassword,
        'newPassword': newPassword,
        })

    updateInfo = requests.put(
        APIUrls.lnapi+APIUrls.updateUrl,
        data=payload,
        headers=headers,
    )
    return updateInfo.ok


def getTransactions(token, type, nbitem=-1, index=1, getLength=False,
                    start=None, end=None):
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
        'authorization': "Bearer {token}",
    }
    params = {
        "type": type,
        "getLength": str(getLength).lower()
    }
    if nbitem != -1:
        params['nbitem'] = nbitem
        params['index'] = index
    if start is not None:
        params['start'] = start
    if end is not None:
        params['end'] = end

    transactions = requests.get(
        APIUrls.lnapi+APIUrls.userHistoryUrl,
        headers=headers,
        params=params,
    )
    if transactions.status_code == 200:
        return transactions.json()
    else:
        raise RuntimeError(
            'Unable to get user transactions:\n'
            f'{transactions.text}'
        )


def getTokens():
    """
    Retrieves the list of active JSON Web Token user currently holds.
    """

    headers = {
        'accept': "application/json",
    }

    tokens = requests.get(
        APIUrls.lnapi+APIUrls.tokenUrl,
        headers=headers,
    )
    if tokens.status_code == 200:
        return tokens.json()
    else:
        raise RuntimeError(
            'Unable to get user tokens:\n'
            f'{tokens.text}'
        )


def revokeToken(token=None):
    """
    identifies and revoke usage of a given JWT.

    Parameters-
    token: Identifier of Token to be removed (optional)
    """

    if token is None:
        tokenInfo = requests.delete(
            APIUrls.lnapi + APIUrls.tokenUrl,
        )
    else:
        params = {
            "jti": token,
        }
        tokenInfo = requests.delete(
            APIUrls.lnapi+APIUrls.tokenUrl,
            params=params,
        )
    if tokenInfo.status_code == 200:
        return True
    else:
        raise RuntimeError(
            'Unable to revoke user tokens:\n'
            f'{tokenInfo.text}'
        )


def generateToken(expiry, deposit=False, withdraw=False, positions=False,
                  user=False):
    """
    Using the given scopes, generate token to give access to different parts
    of the public API.

    Parameters-
    expiry: token expiry in seconds.
    deposit: Allow deposit (optional)
    withdraw: Allow withdraw (optional)
    positions: Allow opening or closing trade positions (optional)
    user: Allow access to user information (optional)
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
    }
    scopes = []
    if deposit:
        scopes += "deposit"
    if withdraw:
        scopes += "withdraw"
    if positions:
        scopes += "positions"
    if user:
        scopes += "user"
    payloadDict = {
        'expiry': expiry,
        'scopes': scopes,
        }
    payload = json.dumps(payloadDict)

    tokenInfo = requests.post(
        APIUrls.lnapi+APIUrls.tokenUrl,
        data=payload,
        headers=headers,
    )
    if tokenInfo.status_code == 200:
        return tokenInfo.json()['token']
    else:
        raise RuntimeError(
            'Unable to generate user tokens:\n'
            f'{tokenInfo.text}'
        )


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
        'authorization': f"Bearer {token}",
    }
    payload = json.dumps({
        'amount': amount,
        'unit': unit,
    })

    invoice = requests.post(
        APIUrls.lnapi+APIUrls.depositUrl,
        data=payload,
        headers=headers,
    )
    if invoice.status_code == 200:
        return invoice.json()
    else:
        raise RuntimeError(
            'Unable to get invoice:\n'
            f'{invoice.text}'
        )


def withdrawInvoice(token, amount, invoice, unit="sat"):
    """
    Move funds from the Lightning channel with LN Markets to user wallet
    by using an invoice directly.

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
        'authorization': f"Bearer {token}",
    }
    payload = json.dumps({
        'amount': amount,
        'unit': unit,
        'invoice': invoice,
    })

    payment = requests.post(
        APIUrls.lnapi+APIUrls.withdrawUrl,
        data=payload,
        headers=headers,
    )
    if payment.status_code == 200:
        return payment.json()
    else:
        raise RuntimeError(
            'Unable to make payment:\n'
            f'{payment.text}'
        )


def withdrawLNURL(token, amount, unit="sat"):
    """
    Move funds from the Lightning channel with LN Markets to user wallet
    by using an LNURL.

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
        'authorization': "Bearer {token}",
    }
    payload = json.dumps({
        'amount': amount,
        'unit': unit,
    })

    LNUrlInfo = requests.post(
        APIUrls.lnapi+APIUrls.withdrawLNUrl,
        data=payload,
        headers=headers,
    )
    if LNUrlInfo.status_code == 200:
        return LNUrlInfo.json()
    else:
        raise RuntimeError(
            'Unable to create LNURL:\n'
            f'{LNUrlInfo.text}'
        )


def login(username, password):
    """
    Use existing credentials to log in.
    """

    headers = {
        'content-type': "application/json",
        'accept': "application/json",
    }
    session = requests.Session()
    payload = json.dumps({
        'login': username,
        'password': password,
    })
    loginResp = session.post(
        APIUrls.lnapi+APIUrls.loginUrl,
        data=payload,
        headers=headers,
    )
    if loginResp.status_code == 200:
        return session
    else:
        raise RuntimeError(
            'Unable to login:\n'
            f'{loginResp.text}'
        )


def logout(session):
    """
    Deletes session cookie
    """

    return session.post(APIUrls.lnapi+APIUrls.logoutUrl).ok
