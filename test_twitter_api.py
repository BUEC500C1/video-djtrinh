import twitter_api as twit


def test_invalid_userpic1(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.get_user_pic("alksdhfaksdlfj") == ""


def test_invalid_userpic2(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.get_user_pic("") == ""


def test_invalid_userpic3(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.get_user_pic(5) == ""


def test_invalid_tweet1(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.get_users_tweets("alksdhfaksdlfj") == ""


def test_invalid_tweet2():
    t = twit.twitter_scrapper("keys")
    assert t.get_users_tweets("") != ""


def test_invalid_tweet3(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.get_users_tweets(23) == ""


def test_grab_pictures1(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.grab_pictures("alksdhfaksdlfj") == []


def test_grab_pictures2(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.grab_pictures("") == []


def test_grab_pictures3(capsys):
    t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert captured.err.find('400')
    assert t.grab_pictures(" ") == []