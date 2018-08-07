#! /usr/bin/python3.5

import requests
import pprint

# API access variables
#accessToken = 'accesstoken'
client_id = '97759B6FEFAB5D2DCF9398B0067E03B26E7F2C1A'
client_secret = 'FE8A3493C40B95E16930B07528FF46CCE07954F3'
baseURL = 'https://api.untappd.com/v4/'

def getUsersTopBeers(user):
    # Get user's JSON data on the top highly rated beers
    res = requests.get(baseURL + 
        '/user/beers/%s?client_id=%s&client_secret=%s&sort=highest_rated_you&limit=5' 
        %(user, client_id, client_secret))
    userBeerData = res.json()['response']['beers']['items']

    # Parse through userBeerData and obtain top 5 beer IDs
    ### Could change this to top 10% beers?
    usersTopBeers = []
    for i in range(max(5, len(userBeerData))):
        usersTopBeers.append(userBeerData[i]['beer']['bid'])    

    return usersTopBeers

    
def getSimilarUsers(usersTopBeers):
    # Get users who also rated highly the usersTopBeers
    similarUsers = {}
    count = 0
    for i in range(len(usersTopBeers)):
        # get beer activity feed of usersTopBeers[i] 
        maxId = ''
        similarUsersThisBeer = []
        # beer #0 gets 5 similar users, #1 gets 4 similar users, #4 gets 1
        while (len(similarUsersThisBeer) < len(usersTopBeers) - i):
            #https://api.untappd.com/v4//beer/checkins/36834?client_id=97759B6FEFAB5D2DCF9398B0067E03B26E7F2C1A&client_secret=max_id=%s
            res = requests.get(baseURL + 
                '/beer/checkins/%s?client_id=%s&client_secret=%s&max_id=%s' 
                %(usersTopBeers[i], client_id, client_secret, maxId))
            beerActivityData = res.json()['response']['checkins']['items']
            count += 1
            for j in range(25):
                if beerActivityData[j]['rating_score'] >= 3.75:
                    # get [user_name] and add him to similarUsers
                    similarUsersThisBeer.append(beerActivityData[j]['user']['user_name'])
                    similarUsers[beerActivityData[j]['user']['user_name']] += 1
                if len(similarUsersThisBeer) == len(usersTopBeers) - i:
                    break
            # obtain checkin_id of the 25th activity, pass it again as max_id
            maxId = beerActivityData[24]['checkin_id']
            # loop through the next 25, so forth, until we get the correct number of similar users
    print('API Requests made : ' + str(count))
    return similarUsers

def updateSimilarityIndex(similarUsers, usersTopBeers):
    # Store similarUsers' similarity index (number of beers matched)
    for user, similarityIndex in similarUsers:
        # First, check all beers for ones rated >=4 from similar user
        similarUsersTopBeers = []
        offset = 0
        reachedEndOfBeers = False 
        while not reachedEndOfBeers or offset > 150:
            res = requests.get(baseURL + 
                '/user/beers/%s?client_id=%s&client_secret=%s&limit=50&offset=%s&sort=highest_rated_you'
                %(user, client_id, client_secret, str(offset)))
            similarUsersBeerData = res.json()
            count = int(similarUsersBeerData['beers']['count'])
            if count != 0:
                offset += count
                for j in range(count):
                    checkinData = similarUsersBeerData['beers']['items'][j]
                    if checkinData['rating_score'] >= 4:
                        similarUsersTopBeers.append(checkinData['beer']['bid'])
                    else:
                        reachedEndOfBeers = True # what a sad statement

        # Find common beers and update the value in the similarUsers dict
        similarUsers[key] = len(list(set(usersTopBeers).intersection(similarUsersTopBeers)))
    
    # End of for loop, move on to next similarUser


def getBeerIds(menuText):
    beerIDs = []
    for beer in menuText:
        res = requests.get(baseURL + 
            'search/beer/%s?client_id=%s&client_secret=%sq=%s'
            %(client_id, client_secret, beer))
        beerSearchData = res.json()
        if beerSearchData['found'] != 0:
            beerIDs.append(beerSearchData['beers']['items'][0]['beer']['bid'])
    return beerIDs


# Iterate through menuBeers, looking for it in the topBeers of similarUsers
# If found, use similarityIndex w user and similarUser's rating to calculate rating
# If found again in another similarUser, amplify score even further
# Score should be out of a scale of 100 at the end, with 100 being all similar users rated it at 5 stars
