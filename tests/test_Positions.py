from LNMarkets import Positions


def test_getPositions(token):
    assert 'open' in Positions.getPositions(token, 'open')


def test_createPosition(token):
    buyinfo = Positions.buy(token, leverage=1, quantity=1)
    assert 'position' in buyinfo
    assert 'pid' in buyinfo['position']
    assert Positions.closePosition(token, buyinfo['position']['pid'])['closed']
