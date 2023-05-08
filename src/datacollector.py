import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.webdriver import WebDriver
import datetime
import pandas as pd

driver = webdriver.GetWebdriver()
    
date_for_deletion = '2022-05-21'
stop_condition = 5

def ScrapeTweets(driver: WebDriver,stop_condition):
    first_tweet = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[data-testid=cellInnerDiv]")))
    driver.execute_script('arguments[0].scrollIntoView({block: "center", behavior: "smooth"});', first_tweet)
    time.sleep(1)
    foundTweetCount=0

    column_names = ['username', 'tweet_text', 'tweet_date']
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
                # print(date,tm, is_a_tweet[0].text.replace('\n',''))
                if (tweetText != None):
                    foundTweetCount += 1
                    print("Found tweet count "+str(foundTweetCount))
                    dateFromString = datetime.datetime.strptime(date+" "+tm,"%Y-%m-%d %H:%M:%S.%fZ")
                    username = senderName.text
                    username = username.replace("@","")
                    new_tweet = {'username':username,'tweet_text':tweetText.text,'tweet_date':dateFromString.strftime("%Y-%m-%d %H:%M:%S")}
                    tweets_df = pd.concat([tweets_df,pd.DataFrame([new_tweet])],ignore_index = True)
                    
            except Exception:
                print("An exception happened in parsing tweet")
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
    except:
        print("An exception occured")

GetTweetsFromUser(driver,"elonmusk",False) 

def GetTweetsFromURL(driver,url):
    driver.get("https://twitter.com/elonmusk")



