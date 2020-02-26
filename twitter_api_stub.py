import json


class twitter_api_stub():


    def __init__(self):
        self.j = json.load(open("google.json"))

    def get_user_pic(self, username):
        if username == "Google":
            pass
        else:
            return ""

    def get_users_tweets(self, username):
        if username == "Google":
            return self.j["full_text"]
        else:
            return ''

    def grab_pictures(self, username):
        if username == "Google":
            pass
        else:
            return []