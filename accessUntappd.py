#! /usr/bin/python3.5

import requests
import pprint

# API access variables
#accessToken = 'accesstoken'
client_id = '97759B6FEFAB5D2DCF9398B0067E03B26E7F2C1A'
client_secret = 'FE8A3493C40B95E16930B07528FF46CCE07954F3'
baseURL = 'https://api.untappd.com/v4/'


# TODO : Store user's top beers in a database, update only if too old
def getUsersTopBeers(user):
    # Get user's JSON data on the top highly rated beers
    res = requests.get(baseURL + 
        '/user/beers/%s?client_id=%s&client_secret=%s&sort=highest_rated_you&limit=50' 
        %(user, client_id, client_secret))
    userBeerData = res.json()['response']['beers']['items']

    # Parse through userBeerData and obtain top 50 beer IDs
    ### Could change this to top 10% beers?
    usersTopBeers = []
    for i in range(max(50, len(userBeerData))):
        usersTopBeers.append(userBeerData[i]['beer']['bid'])    

    return usersTopBeers

    
def getSimilarUsers(usersTopBeers, user):
    # Get users who also rated highly the usersTopBeers
    topBeersToConsider = 5
    similarUsers = {}
    APIRequestsMade = 0

    # Outside loop up to 5 top beers of user looking for similar users
    for i in range(min(topBeersToConsider, len(usersTopBeers))):
        maxId = ''
        similarUsersThisBeer = []

        # beer #0 gets 5 similar users, #1 gets 4 similar users, etc
        while len(similarUsersThisBeer) < topBeersToConsider - i:
            res = requests.get(baseURL + 
                '/beer/checkins/%s?client_id=%s&client_secret=%s&max_id=%s' 
                %(usersTopBeers[i], client_id, client_secret, maxId))
            beerActivityData = res.json()['response']['checkins']['items']
            totalActivity = int(res.json()['response']['checkins']['count'])
            APIRequestsMade += 1

            # Loop through the returned data looking for users who rated highly
            for j in range(totalActivity):
                if beerActivityData[j]['rating_score'] >= 4:
                    # get [user_name] and add him to similarUsers
                    similarUser = beerActivityData[j]['user']['user_name']
                    if similarUser not in similarUsers and similarUser != user:
                        similarUsersThisBeer.append(similarUser)
                        similarUsers[similarUser] = []
                if len(similarUsersThisBeer) == topBeersToConsider - i:
                    break

            # obtain checkin_id of the 25th activity, pass it again as max_id
            # OR, if the beer is rare enough that it has fewer than 25 checkins, move on
            if totalActivity < 25:
                break
            else:
                maxId = beerActivityData[24]['checkin_id']
            # loop through the next 25, so forth, until we get the correct number of similar users
    return similarUsers

def getSimilarUsersTopBeers(similarUsers, usersTopBeers):
    # Store similarUsers' similarity index (number of beers matched)
    APIRequestsMade = 0

    for user, similarityIndex in similarUsers.items():
        # Gather similarUser's top beers
        res = requests.get(baseURL + 
            '/user/beers/%s?client_id=%s&client_secret=%s&limit=50&sort=highest_rated_you'
            %(user, client_id, client_secret))
        APIRequestsMade += 1
        similarUsersBeerData = res.json()['response']['beers']['items']

        # Add each top beer until we run out of beers or hit lower than 3.75 rating
        for j in range(len(similarUsersBeerData)):
            if similarUsersBeerData[j]['rating_score'] >= 3.75:
                similarUsers[user].append(similarUsersBeerData[j]['beer']['bid'])
            else:
                break

        # Find common beers and update the value in the similarUsers dict
        similarityIndex = len(list(set(usersTopBeers).intersection(similarUsers[user])))
        print('user beers : ', end='')
        print(usersTopBeers)
        print('similar user ' + user + ' top beers: ', end='')
        print(similarUsers[user])
        print('user : ' + user + ' similarity index: ' +str(similarityIndex))
    print('API Requests made : ' + str(APIRequestsMade))
    
    # End of for loop, move on to next similarUser


def getBeerIds(menuBeers):
    beerIDs = {}
    for beer in menuBeers:
        res = requests.get(baseURL + 
            'search/beer?client_id=%s&client_secret=%s&q=%s'
            %(client_id, client_secret, beer))
        print(res.text)
        print('\n\n')
        beerSearchData = res.json()['response']
        pprint.pprint(beerSearchData)
        if beerSearchData['found'] != 0:
            beerIDs[beer] = beerSearchData['beers']['items'][0]['beer']['bid']

    return beerIDs


# Iterate through menuBeers, looking for it in the topBeers of similarUsers
# If found, use similarityIndex w user and similarUser's rating to calculate rating
# If found again in another similarUser, amplify score even further
# Score should be out of a scale of 100 at the end, with 100 being all similar users rated it at 5 stars
