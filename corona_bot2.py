

#%%
import pandas as pd
import datetime 
import requests
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') 
import tweepy
from tweepy import OAuthHandler
import os



parser = argparse.ArgumentParser(description="Does some awesome things.")
parser.add_argument('--twitter_access_secret', type=str, help="pass a message into the script")
parser.add_argument('--twitter_access_token', type=str, help="pass a message into the script")
parser.add_argument('--twitter_consumer_key', type=str, help="pass a message into the script")
parser.add_argument('--twitter_consumer_secret', type=str, help="pass a message into the script")

args = parser.parse_args()
print ("Test", args.twitter_consumer_key)

consumer_key = args.twitter_consumer_key
consumer_secret = args.twitter_consumer_secret
access_token = args.twitter_access_token
access_secret = args.twitter_access_secret

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

#%%
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    now = datetime.datetime.now()
    current_time = now.strftime("%d.%m.%Y %H:%M:%S")

    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    pro_string = f'\r{prefix} |{bar}| {percent}% {suffix} {current_time}'
    return pro_string

#%%

df = pd.read_excel('https://storage.googleapis.com/ndrdata-impfungen/rki_data/rki_impfquotenmonitoring_latest.xlsx', sheet_name=1)

impfungen = df[(df['Bundesland'] == 'Gesamt')].iloc[0,1]
bev = 83166711
impfquote = impfungen / bev * 100
text2 = '{} von 83 Mio. Impfungen'.format(int(impfungen))

string = printProgressBar(impfquote, 100, prefix = 'Impffortschritt Deutschland:', suffix = 'komplett (Erstimpfung)', length = 40)

tweettext = string + " - " + text2
print (tweettext)



#%% Tweet


api.update_status(status=tweettext)