# LNMarkets API Wrapper

This is a Python wrapper for [LNMarkets](https://lnmarkets.com/) API.

To install: `pip install LNMarkets`

Documentation: `help(LNMarkets)`
To access documentation on idividual module, eg User: `help(LNMarkets.User)`

Example Usage:
```python
import LNMarkets

LNMToken = '<YOUR TOKEN>'
apiState = LNMarkets.State.getState()
openPositions = LNMarkets.Positions.getPositions(LNMToken)['open'] #Token must have position scope
userInfo = LNMarkets.User.userInformation(LNMToken) #Token must have user scope
buyInfo = LNMarkets.Positions.buy(LNMToken,leverage,quantity=quantity)
```

Note:
* It is recommended that you use token with only 'positions' scope, as leaking it cannot result in loss of funds through withdrawal. 
* Methods in Lnmarkets.User need token with 'user' scope.

## Running Unit Tests
To run unit tests, run the following command in main directory, where setup.py is present.
```console
$ python3 setup.py test --token '<Your Token>'
```
You need a token with both 'positions' and 'user' scope to run test. One of the test will buy and sell one contract, hence your account need small amount of balance.
