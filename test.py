from urllib import response
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import datetime
import time
import math
import urllib
from requests_oauthlib import OAuth1Session
import tweepy
import requests
import tqdm
import sys

def pick_name (aid):
     for user in users:
        if user["id"] == aid:
            return user["name"]
            break

def pick_id (aid):
     for user in users:
        if user["id"] == aid:
            return user["username"]
            break

ck = "O0OZpFhzy7vdS4ccqvpvBX3RV"
cs = "tCYIl7OK0VFcundMg98PgUoVL7DmjmQzZY9De33mcYSuIinGe3"
bt = "AAAAAAAAAAAAAAAAAAAAAFkYeAEAAAAAdH1nDV6yfPDrKEIkTG4%2FLRYllco%3DUYRAeiEIFEefZOHNOtVdHs66XFQgqrNpJNreJ8hOUJzIUf50bm"
at = "741647183045218304-DLetVq5SNKvc0mTvJZ4k3UAEf35vOR2"
ats = "n4W5UK4bSSTqqVTOu3LZr53ytudpWYiiHNiSamd9mnikM"

auth = tweepy.OAuthHandler(ck, cs)
auth.set_access_token(at, ats)
api = tweepy.API(auth)

ss = open('ss.txt', 'r')
se = ss.readline()
se = se.replace("\n", "")
sa = ss.readline()
sa = sa.replace("\n", "")
ss.close()

nowtime = datetime.datetime.now()
nt = nowtime.strftime('%Y-%m-%dT00:00:00+09:00')
#bef7 = nowtime - datetime.timedelta(days = 6)
bef7 = nowtime - datetime.timedelta(hours = 1)
bet = bef7.strftime('%Y-%m-%dT%H:00:00+09:00')
#client = tweepy.Client(bearer_token = bt, consumer_key = ck, consumer_secret = cs, access_token = at, access_token_secret = ats)
#search = '塩化 -from:enka_Benzen_fan'
search = se
max_count = 500000
tweets = [[],[],[],[]]
#tweets = client.tweets.tweetsRecentSearch({query: search})
#tweets = search_tweets(ck, cs, at, ats, search, tweet_max, 2)
url = "https://api.twitter.com/2/tweets/search/recent"
next_token = None
params = {
    "query": search + " -is:retweet",
    "start_time": bet,
    #"end_time": nt,
    #"expansions": "attachments.poll_ids,attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id",
    "expansions": "author_id",
    "max_results": "10",
    "tweet.fields": "created_at"
    #"media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,public_metrics",
    #"place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
    #"poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
    #"tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld",
    #"user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld",
}

while True:
    if next_token is not None:
        params["next_token"] = next_token
    encoded_params = urllib.parse.urlencode(params)
    headers = {"Authorization": f"Bearer {bt}"}
    res = requests.request("GET", url, params=encoded_params, headers=headers)
    res_json = res.json()
    #print(res_json["data"][0].keys())

    if res.status_code == 429:
        rate_limit_reset = int(res.headers["x-rate-limit-reset"])
        now = time.mktime(datetime.datetime.now().timetuple())
        wait_sec = int(rate_limit_reset - now)
        desc = f"Waiting for {wait_sec} seconds"
        for _ in tqdm.trange(wait_sec, desc=desc):
            time.sleep(1)
    
    elif res.status_code != 200:
        raise Exception(res.status_code, res.text)
    
    else:
        if res_json["meta"]["result_count"] == 0:
         break

        datas = res_json["data"]
        users = res_json["includes"]["users"]
#print (type(users))

        for data in datas:
         print (data["created_at"])
         tweets[0].append(data["created_at"])
         print (pick_id(data["author_id"]))
         tweets[1].append(pick_id(data["author_id"]))
         print (pick_name(data["author_id"]))
         tweets[2].append(pick_name(data["author_id"]))
         print (data["text"])
         tweets[3].append(data["text"])
        
        next_token = res_json.get("meta").get("next_token")
        if next_token is None or len(tweets) >= max_count:
            break

#scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
#creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
#client = gspread.authorize(creds)

#webcomp-srm@srmmarzwebcomp.iam.gserviceaccount.com に共有が必要

key_name = 'client_secret.json'
#sheet_name = 'MySearch'
sheet_name = sa

gc = gspread.service_account(filename = key_name)
wks = gc.open(sheet_name).sheet1

next_row = len(list(filter(None, wks.col_values(1))))+1

for i in range(len(tweets[0])):
    for j in range(4):
        try:
            re = wks.update_cell(i+next_row, j+1, tweets[j][i])
        except gspread.exceptions.APIError:
            print("waiting...")
            time.sleep(110)
            gc = gspread.service_account(filename = key_name)
            wks = gc.open(sheet_name).sheet1
            wks.update_cell(i+next_row, j+1, tweets[j][i])

#print (datas[1]["text"])
#tweets += datas[1]["text"]

#for data in datas:
# tweets += data["text"]

#print (type(tweets[10]))

#tweets = tweepy.Cursor(api.search_tweets, q = search, lang = 'ja').items(tweet_max)
#for tweet in tweets:
 #   print(tweet.text)
#for tweet in tweets:
#    print ((tweet))
#api.update_status("はろーわーるど")

#client.create_tweet(text = geo_data['latitude'] + ", " + geo_data['longitude'])
#.create_tweet(text = "授業中…")