import twitterdatacollector
import webdriver
import pandas as pd
# GetTweetsFromUser(driver,"elonmusk",False) 

if __name__ == '__main__':
    driver = webdriver.GetWebdriver()
    tweets_df = twitterdatacollector.GetTweetsFromUser(driver,"WSJCentralBanks",False) 
    tweets_df.to_csv("fetchedTweets.csv",index=False)
    readed_df = pd.read_csv("fetchedTweets.csv")
    print(readed_df.head(10))
    webdriver.CloseWebdriver(driver)



