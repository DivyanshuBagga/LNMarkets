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
