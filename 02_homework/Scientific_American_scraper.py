import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 
import os.path

#Connecing to Twilio
from twilio.rest import Client
account_sid = "XXXXX"
auth_token  = "XXXXX"
client = Client(account_sid, auth_token)

#Scrape Science mag
response = requests.get("https://www.scientificamerican.com/")
doc = BeautifulSoup(response.text, 'html.parser')

#Let's try to pull out the feature article
feature_article = doc.find('div', {'class': 'listing-feature__inner'})

#Let's create a dictionary for our feature story

feature_story = {
    'headline': feature_article.find("h1").text,
    'href': feature_article.find("a")["href"],
    'summary': feature_article.find("p", {"class": "listing-feature__summary t_body"}).text,
    'date': time.strftime("%Y-%m-%d-%H-%M")
}

def send_sms():
    sms_msg = "NEW Feature from Scientific American: " + feature_story['headline']

    client.messages.create(
        to="XXXXX",
        from_="XXXXX",
        body=sms_msg,
        media_url=feature_story['href'])


#Check if the current path has a file called features history
#IF it doesn't, create one using our feature story

if os.path.isfile('features_history.csv'):
    features_history = pd.read_csv('features_history.csv')
    
else:
    df_feature_story = pd.DataFrame([feature_story])
    df_feature_story.to_csv('features_history.csv', index=False)

#Check to see if the last feature article on the list is different from the current one
#If it is different, append the new feature story to our history file and save it

if features_history['headline'].tail(1).item() != feature_story['headline']:
    features_history = features_history.append([feature_story])
    features_history.to_csv('features_history.csv', index=False)
    send_sms()