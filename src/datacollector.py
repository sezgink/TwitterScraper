import webdriver
from selenium.webdriver.common.by import By

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import datetime
import pandas as pd

import selenium.webdriver.common

import sys

# driver = webdriver.GetWebdriver()

date_for_deletion = '2022-05-21'
stop_condition = 5
def CountFromText(countText:str):
    countText = countText.replace(",","")
    multiplier = 1
    for c in countText:
        if(c=='K'):
            multiplier=1000
        elif(c=='M'):
            multiplier=1000000
    countText = countText.replace("K","")
    countText = countText.replace("M","")
    
    if countText=="":
        return int(0)

    count =float(countText)
    count*=multiplier
    return int(count)
def ScrapeTweets(driver: WebDriver,stop_condition):
    first_tweet = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid=cellInnerDiv]")))
    driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', first_tweet)
    time.sleep(1)
    foundTweetCount=0

    # column_names = ['username', 'tweet_text', 'tweet_date']
    column_names = ['username', 'tweet_text', 'tweet_date','tweet_like_count','tweet_reply_count','tweet_retweet_count','tweet_transition_count','tweet_status_link']
    # column_names = ['username', 'tweet_text', 'tweet_date','tweet_like_count','tweet_reply_count','tweet_retweet_count','tweet_transition_count']

    tweets_df = pd.DataFrame(columns=column_names)
    for i in range(999):
        tweets = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid=cellInnerDiv]')
        is_a_tweet = tweets[0].find_elements(By.XPATH, './/article[@data-testid="tweet"]')
        # check if list is not empty (i.e. check if element is a tweet or a "who to follow" element)
        if is_a_tweet:
            date = tweets[0].find_element(By.XPATH, './/time').get_attribute('datetime').split('T')[0]
            tm = tweets[0].find_element(By.XPATH, './/time').get_attribute('datetime').split('T')[1]
            try:
                tweetText = tweets[0].find_element(By.CSS_SELECTOR, 'div[data-testid=tweetText]')
                senderName = tweets[0].find_element(By.CSS_SELECTOR, 'div[data-testid=User-Name]')
                senderName = senderName.find_element(By.CSS_SELECTOR,'div[class="css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0"]')
                statusLink = tweets[0].find_element(By.XPATH, './/time').find_element(By.XPATH,"..").get_attribute("href")

                fetched_statistics = False
                tweet_statistics = {}
                try:
                    replyCount = tweets[0].find_element(By.CSS_SELECTOR, 'div[data-testid=reply]').text
                    replyCountNum = CountFromText(replyCount)
                    retweetCount = tweets[0].find_element(By.CSS_SELECTOR, 'div[data-testid=retweet]').text
                    retweetCountNum = CountFromText(retweetCount)
                    likeCount = tweets[0].find_element(By.CSS_SELECTOR, 'div[data-testid=like]').text
                    likeCountNum = CountFromText(likeCount)
                    transitionCountNum = 0
                    try:
                        transitionCount = tweets[0].find_element(By.CSS_SELECTOR, 'span[data-testid=app-text-transition-container]').text
                        transitionCountNum = CountFromText(transitionCount)
                    except Exception as e:
                        print(f"Couldnt get transition because of {e}")
                    # print(replyCountNum,replyCountNum,likeCountNum,transitionCountNum)
                    tweet_statistics["tweet_like_count"]=likeCountNum
                    tweet_statistics["tweet_reply_count"]=replyCountNum
                    tweet_statistics["tweet_retweet_count"]=retweetCountNum
                    tweet_statistics["tweet_transition_count"]=transitionCountNum
                    fetched_statistics = True
                except selenium.common.exceptions.NoSuchElementException:
                    print("No such an element at tweet stats")
                except Exception as e:
                    print(f"Couldn't get reply, retweet, likes because: {str(e)}")            
                # print(date,tm, is_a_tweet[0].text.replace('\n',''))
                if (tweetText != None):
                    foundTweetCount += 1
                    print("Found tweet count "+str(foundTweetCount))
                    dateFromString = datetime.datetime.strptime(date+" "+tm,"%Y-%m-%d %H:%M:%S.%fZ")
                    username = senderName.text
                    username = username.replace("@","")
                    new_tweet = {'username':username,'tweet_text':tweetText.text,'tweet_date':dateFromString.strftime("%Y-%m-%d %H:%M:%S"), 'tweet_status_link':statusLink}
                    # new_tweet = {'username':username,'tweet_text':tweetText.text,'tweet_date':dateFromString.strftime("%Y-%m-%d %H:%M:%S")}
                    if fetched_statistics:
                        new_tweet = {**new_tweet,**tweet_statistics}
                    tweets_df = pd.concat([tweets_df,pd.DataFrame([new_tweet])],ignore_index = True)
            except Exception as e:
                print(f"An exception happened in parsing tweet: {str(e)}")
            time.sleep(0.2)
            # time.sleep(1)
        # delete element from HTML
        driver.execute_script('var element = arguments[0]; element.remove();', tweets[0])
        if foundTweetCount >= stop_condition:
            break
    return tweets_df

def GetTweetsFromUser(driver : WebDriver,username : str,onlyuser : bool):  
    try:
        driver.get(f"https://twitter.com/{username}")
        tweets_df = ScrapeTweets(driver,20)
        if(onlyuser):
            tweets_df = tweets_df[tweets_df.username==username]
            tweets_df = tweets_df.reset_index(drop=True)
        print(tweets_df.head(10))
        return tweets_df
    except Exception as e:
        print(f"An exception occured {str(e)}")

# GetTweetsFromUser(driver,"elonmusk",False) 
# tweets_df = GetTweetsFromUser(driver,"WSJCentralBanks",False) 
# tweets_df.to_csv("fetchedTweets.csv",index=False)
# readed_df = pd.read_csv("fetchedTweets.csv")
# print(readed_df.head(10))

def GetTweetsFromURL(driver,url):
    driver.get("https://twitter.com/elonmusk")

def ScrapeSingleAndSave(driver, username,outputName="fetchedTweets.csv"):
    tweets_df = GetTweetsFromUser(driver,username,False) 
    tweets_df.to_csv(outputName,index=False)
    webdriver.CloseWebdriver(driver)
    # readed_df = pd.read_csv(outputName)
def ReadTxtList(adress):
    my_file = open(adress, "r")    
    data = my_file.read()
    data_into_list = data.split("\n")
    # printing the data
    print(data_into_list)
    my_file.close()
    return data_into_list
def ScrapeMultipleAndSave(driver, usernameSource,outputName="fetchedTweets.csv"):
    fetched_tweets_df = pd.DataFrame()
    usernameList = ReadTxtList(usernameSource)
    for username in usernameList:
        print("Username: "+username)
        tweets_df = GetTweetsFromUser(driver,username,False) 
        fetched_tweets_df = pd.concat([fetched_tweets_df,tweets_df],ignore_index=True)
        # tweets_df.to_csv(outputName,index=False)
    fetched_tweets_df.to_csv(outputName,index=False)
    webdriver.CloseWebdriver(driver)


def NoArgument(driver):
    tweets_df = GetTweetsFromUser(driver,"WSJCentralBanks",False) 
    tweets_df.to_csv("fetchedTweets.csv",index=False)
    readed_df = pd.read_csv("fetchedTweets.csv")
    print(readed_df.head(10))
    webdriver.CloseWebdriver(driver)

def main():
    driver = webdriver.GetWebdriver()

    if len(sys.argv)<2:
        NoArgument(driver)
        return

    command = sys.argv[1]

    if command == 'help':
        print(""" First argument command : [single, multiple, help] \n Second argument scrape target, if command multiple csv file that contain usernames, if command is single single string of username to be scraped
          """)
        return
    
    if len(sys.argv)<3:
        NoArgument(driver)
        return
    
    usernames = sys.argv[2]

    if usernames==None:
        tweets_df = GetTweetsFromUser(driver,"WSJCentralBanks",False) 
        tweets_df.to_csv("fetchedTweets.csv",index=False)
        # readed_df = pd.read_csv("fetchedTweets.csv")
        # print(readed_df.head(10))

    if command == 'single':
        ScrapeSingleAndSave(driver,usernames)
        return
    
    if (command == 'multi') | (command=='multiple'):
        ScrapeMultipleAndSave(driver,usernames)
        return
        # webdriver.CloseWebdriver(driver)

if __name__ == '__main__':
    main()


