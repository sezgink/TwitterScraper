import datetime

class TweetData:
    def __init__(username:str,text:str,tweetDate:datetime.datetime):
        self.username = username
        self.text = text
        self.tweetDate = tweetDate
    def __str__(self) -> str:
        return self.tweetDate +" "+self.username+" "+self.text
