import datetime

class Tweetdata:
    def __init__(username:str,text:str,tweetDate:str):
        self.username = username
        self.text = text
        self.tweetDate = tweetDate
    def __str__(self) -> str:
        return self.tweetDate +" "+self.username+" "+self.text
