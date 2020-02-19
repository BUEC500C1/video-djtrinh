import twitter_api as twit


def test_invalid_username():
    t = twit.twitter_scrapper("keys")
    assert t.get_user_pic("alksdhfaksdlfj") == ""


def test_invalid_username2():
    t = twit.twitter_scrapper("keys")
    assert t.get_users_tweets("alksdhfaksdlfj") == ""


def test_invalid_username3():
    t = twit.twitter_scrapper("keys")
    assert t.grab_pictures("alksdhfaksdlfj") == []
