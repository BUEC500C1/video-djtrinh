import main


def test_create():
    assert main.create_images("aslfdad", "asldkfdf", "asdfasdf", 5) == None


def test_ffmpeg_call():
    assert main.ffmpeg_call("test") == -1
