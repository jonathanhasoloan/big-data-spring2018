# Problem Set 3: Scraping and Cleaning Twitter Data

Now that you know how to scrape data from Twitter, let's extend the exercise a little so you can show us what you know. You will set up the scraper, clean the resulting data, and visualize it. Make sure you get your own Twitter key (AND make sure that you don't accidentally push it to GitHub); careful with your `.gitignore`.

## Graphic Presentation

Make sure to label all your axes and add legends and units (where appropriate)! Think of these graphs as though they were appearing in a published report for an audience unfamiliar with the data.

## Don't Work on Incomplete Data!

One of the dangers of cleaning data is that you inadvertently delete data that is pertinent to your analysis. If you find yourself getting strange results, you can always run previous portions of your script again to rewind your data. See the section called 'reloading your Tweets in the workshop.

## Deliverables

### Push to GitHub

1. A Python script that contains your scraper code in the provided submission folder. You can copy much of the provided scraper, but you'll have to customize it. This should include the code to generate two scatterplots, and the code you use to clean your datasets.
2. Extra Credit: A Python script that contains the code you used to scrape Wikipedia with the BeautifulSoup library.

### Submit to Stellar

1. Your final CSV files---one with no search term, one with your chosen search term---appropriately cleaned.
2. Extra Credit: A CSV file produced by your BeautifulSoup scraper.

## Instructions

### Step 1

Using the Twitter REST API, collect at least 80,000 tweets. Do not specify a search term. Use a lat/lng of `42.359416,-71.093993` and a radius of `5mi`. Note that this will probably take 20-30 minutes to run.

```python
import jsonpickle
import tweepy
import pandas as pd

# Imports the keys from the python file
# You may need to change working directory
import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api

api = auth(api_key, api_secret)

def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
    all_tweets.to_json(out_file)
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 2000

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

  tweets = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)


```
### Step 2

Clean up the data so that variations of the same user-provided location name are replaced with a single variation. Once you've cleaned up the locations, create a pie chart of user-provided locations. Your pie chart should strive for legibility! Let the [`matplotlib` documentation](https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.pie.html) be your guide!

```Python
#Read data
tweets = pd.read_json('data/tweets.json')

import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

# Cleaning duplicate & Identifying location names
tweets[tweets.duplicated(subset = 'content', keep = False)]
tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

tweets['location'].unique()

#Formatting names into few legible classifications
bos_list = tweets[tweets['location'].str.contains("Boston|boston|bos|Bos|BOSTON")]['location']
tweets['location'].replace(bos_list, 'Boston, MA', inplace = True)

Cambridge_list = tweets[tweets['location'].str.contains("Cambridge|Harvard",case=False)]['location']
tweets['location'].replace(Cambridge_list, 'Cambridge, MA', inplace = True)
bos_list.count() + Cambridge_list.count()

OtherMA = tweets[tweets['location'].str.contains("massachusetts|MA|allston|watertown|Tufts",case=False) & ~tweets['location'].str.contains("Boston|Cambridge")]['location']
tweets['location'].replace(OtherMA, 'Other Location in MA', inplace = True)

NY_list = tweets[tweets['location'].str.contains("NY|New York|Brooklyn",case=False)]['location']
tweets['location'].replace(NY_list, 'New York', inplace = True)

US_list = tweets[tweets['location'].str.contains("USA|CA|CT|San Diego|US|MI|Arizona|MD|WA|TX|VA|CT|RI|Rhode|FL|KY|CO|Michigan|Washington|Chicago|PA|IN|WY|TN|IN|NJ|GA|MO|LA")]['location']
US_list.count()
tweets['location'].replace(US_list, 'Other Location in US', inplace = True)

US_list2 = tweets[tweets['location'].str.contains("US|Philly|Southie|long island|Midwest|UT|Utah|United states|Cleveland|Portland|Texas|Nevada|WI|Virginia|Wisconsin|tx|OH|Florida|Kansas|Detroit|MN|NC|Cape cod|California|oregon|memphis|atlanta|Bethlehem,|dallas|colorado|omaha|u.s.a|denver|New Jersey|miami|Kentucky|missouri|los angeles|seattle",case=False)]['location']
US_list2.count()
tweets['location'].replace(US_list2, 'Other Location in US', inplace = True)

Other = tweets[~tweets['location'].str.contains("MA|US|New York",case=False)]['location']
Other.count()
tweets['location'].replace(Other, 'Other Location', inplace = True)

colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(df_count_tweets['count'], labels=df_count_tweets.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()


```

### Step 3

Create a scatterplot showing all of the tweets are that are geolocated (i.e., include a latitude and longitude).
```python

#Extracting LatLong
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
tweets_geo
len(tweets_geo)
len(tweets)

#only 3 out of the whole data are geolocated
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()
```
### Step 4

Pick a search term (e.g., "housing", "climate", "flood") and collect tweets containing it. Use the same lat/lon and search radius for Boston as you used above. Dpending on the search term, you may find that there are relatively few available tweets.
```python

def get_tweets(
    geo,
    out_file,
    search_term = 'snow',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
    all_tweets.to_json(out_file)
  return all_tweets

# Set a Lat Lon
latlng = '42.359416,-71.093993' # Eric's office (ish)
# Set a search distance
radius = '5mi'
# See tweepy API reference for format specifications
geocode_query = latlng + ',' + radius
# set output file location
file_name = 'data/tweets2.json'
# set threshold number of Tweets. Note that it's possible
# to get more than one
t_max = 2000

get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)

def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

  tweets2 = get_tweets(
  geo = geocode_query,
  tweet_max = t_max,
  write = True,
  out_file = file_name
)
```
### Step 5

Clean the search term data as with the previous data.
```python

#Read data
tweets2 = pd.read_json('data/tweets2.json')

#Clean duplicate
tweets2[tweets2.duplicated(subset = 'content', keep = False)]
tweets2.drop_duplicates(subset = 'content', keep = False, inplace = True)

#Identifying location names
tweets2['location'].unique()

loc_tweets2 = tweets2[tweets2['location'] != '']
count_tweets2 = loc_tweets2.groupby('location')['id'].count()
df_count_tweets2 = count_tweets2.to_frame()
df_count_tweets2
df_count_tweets2.columns
df_count_tweets2.columns = ['count']
df_count_tweets2

#Formatting names into few legible classifications
bos_list2 = tweets2[tweets2['location'].str.contains("Boston|Bos|Berklee|Fenway|northeastern|bo$ton",case=False)]['location']
bos_list2.count()
tweets2['location'].replace(bos_list2, 'Boston, MA', inplace = True)

Cambridge_list2 = tweets2[tweets2['location'].str.contains("Cambridge|MIT",case=False)]['location']
Cambridge_list2.count()
tweets2['location'].replace(Cambridge_list2, 'Cambridge, MA', inplace = True)

Somerv_list2 = tweets2[tweets2['location'].str.contains("somerville",case=False)]['location']
tweets2['location'].replace(Somerv_list2, 'Somerville, MA', inplace = True)
Somerv_list2.count()

OtherMA2 = tweets2[tweets2['location'].str.contains("massachusetts|MA|allston|watertown|Tufts|Roxbury|chelsea",case=False) & ~tweets2['location'].str.contains("Boston|Cambridge|Somerville")]['location']
tweets2['location'].replace(OtherMA2, 'Other Location in MA', inplace = True)

#The number of tweets at other US location is small individually so they are compounded into one group
OtherUS2 = tweets2[tweets2['location'].str.contains("USA|California|Arizona|Rhode|Washington|US|America|orleans|candyfornia",case=False) | tweets2['location'].str.contains("NY|NE|IL|PA|AZ")]['location']
OtherUS2.count()
tweets2['location'].replace(OtherUS2, 'Other Location in US', inplace = True)

#Grouping weird and international location
Other2 = tweets2[~tweets2['location'].str.contains("Boston|Cambridge|Somerville|MA|US")]['location']
tweets2['location'].replace(Other2, 'Other Location', inplace = True)

#Plot pie chart
plt.pie(df_count_tweets2['count'],labels=df_count_tweets2.index.get_values(), shadow=False, colors=colors,autopct='%1.1f%%')
plt.axis('equal')
plt.title('Distribution of Self-Reported Tweets Location (949 Tweets)')
plt.tight_layout()
plt.show()

```
### Step 6

Create a scatterplot showing all of the tweets that include your search term that are geolocated (i.e., include a latitude and longitude).
```python

#Extracting LatLong
tweets_geo2 = tweets2[tweets2['lon'].notnull() & tweets2['lat'].notnull()]
tweets_geo2
len(tweets_geo2)
len(tweets2)
#only 16 out of the whole data are geolcated
#Plot
plt.scatter(tweets_geo2['lon'], tweets_geo2['lat'], s = 25)
plt.title('Distirbution of Geolocated Tweets (16/949 Tweets)')
plt.xlabel('Latitude')
plt.ylabel('Longitude')
plt.show()

```
Export your scraped Twitter datasets (one with a search term, one without) to two CSV files. We will be checking this CSV file for duplicates and for consistent location names, so make sure you clean carefully!
```python

#Exporting CSV

tweets.to_csv('twitter_data.csv', sep=',', encoding='utf-8') #without search term
tweets2.to_csv('twitter2_data.csv', sep=',', encoding='utf-8') #with search term
```
## Extra Credit Opportunity

Build a scraper that downloads and parses the Wikipedia [List of Countries by Greenhouse Gas Emissions page](https://en.wikipedia.org/wiki/List_of_countries_by_greenhouse_gas_emissions) using BeautifulSoup and outputs the table of countries as as a CSV.
