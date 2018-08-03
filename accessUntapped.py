#! /usr/bin/python3.5

import requests
import pprint

# API access variables
clientId = '12345'
clientSecret = '12345678'
accessToken = 'accesstoken'
username = 'dupark3'
baseURL = 'https://api.untappd.com/v4/'

# Get user's JSON data on the top highly rated beers
res = requests.get(baseURL + 
    '/user/beers/%s?client_id=%s&client_secret=%s&sort=highest_rated_you' 
    %(username, clientId, clientSecret))
userBeerData = res.json()
pprint.pprint(userBeerData)

# Parse through userBeerData and obtain top 10 beer IDs
### Could change this to top 10% beers?
usersTopBeers = []
for i in range(max(10,userBeerData['beers']['items']['count'])):
    usersTopBeers.append(userBeerData['beers']['items'][i]['beer']['bid'])
    
# Get users who also rated highly the usersTopBeers
similarUsers = {}
for i in range(len(usersTopBeers)):
    # get beer activity feed of usersTopBeers[i] 
    maxId = ''
    similarUsersThisBeer = []
    # beer #0 gets 11 similar users, #1 gets 10 similar users, etc until #10 gets 1 similar user
    while (len(similarUsersThisBeer) < len(usersTopBeers) + 1 - i):
        res = requests.get(baseURL + 
            '/beer/checkins/%s?client_id=%s&client_secret=%smax_id=%s' 
            %s(usersTopBeers[i], clientId, clientSecret, maxId))
        beerActivityData = res.json()
        for i in range(25):
            # if [rating_score] of returned JSON is > 4
            if beerActivityData['checkins']['items'][i]['rating_score'] > 4:
                # get [user_name] and add him to similarUsers
                similarUsersThisBeer.append(beerActivityData['checkins']['items'][i]['user']['user_name'])
        # obtain checkin_id of the 25th activity, pass it again as max_id
        maxId = beerActivityData['checkins']['items'][24]['checkin_id']
        # loop through the next 25, so forth, until we get the correct number of similar users
    for user in similarUsersThisBeer:
        similarUsers[user] = 1

# Store similarUsers' similarity index (number of beers matched)
for user, similarityIndex in similarUsers:
    similarUsersBeers = []
    offset = 0
    finished = False
    while not finished:
        res = requests.get(baseURL + 
            '/user/beers/%s?client_id=%s&client_secret=%s&limit=50&offset=%s&sort=highest_rated_you'
            %(user, clientId, clientSecret, str(offset)))
        similarUsersBeerData = res.json()
        count = int(similarUsersBeerData['beers']['count'])
        if count != 0:
            offset += count
            for j in range(count):
                checkinData = similarUsersBeerData['beers']['items'][j]
                if checkinData['rating_score'] >= 4:
                    similarUsersBeers.append(checkinData['beer']['bid'])
                else:
                    finished = True
    
    similarUsers[key] = len(list(set(usersTopBeers).intersection(similarUsersBeers)))
    


    

