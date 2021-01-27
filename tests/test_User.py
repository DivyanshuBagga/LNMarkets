from LNMarkets import User


def test_userInformation(token):
    userInfo = User.userInformation(token)
    assert 'show_leaderboard' in userInfo
    show_leaderboard = userInfo['show_leaderboard']
    assert not User.updateUser(token, leaderboard=False)['show_leaderboard']
    assert User.updateUser(token, leaderboard=True)['show_leaderboard']
    User.updateUser(token, leaderboard=show_leaderboard)
