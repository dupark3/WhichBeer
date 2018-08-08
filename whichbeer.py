#! /usr/bin/python3.5

import accessUntappd, pictureToText, calculateScore
import sys, pprint, datetime
import database, beerIDs

def main():
    if len(sys.argv) < 2:
        print('Usage : ./whichbeer.py <username> <menuPictureFileName>')
        sys.exit()

    username = sys.argv[1]
    pictureFile = sys.argv[2]

    # Open database file to write to if more than 1 day old        
    now = datetime.datetime.today()
    if now - database.timeStamp > datetime.timedelta(days=1):
        databaseFile = open('database.py', 'w')
        databaseFile.write('import datetime\n')
        databaseFile.write('timeStamp = ' + pprint.pformat(now) + '\n')
        accessAPI = True
    else:
        accessAPI = False
    print(accessAPI)

    # Find upto 50 top rated beers by user
    if accessAPI:
        usersTopBeers = accessUntappd.getUsersTopBeers(username)
        databaseFile.write('usersTopBeers = ' + pprint.pformat(usersTopBeers, width=1000000) + '\n')
    else:
        usersTopBeers = database.usersTopBeers
    
    # Find up to 15 other users who also rated the top beers highly
    # Also find their top beers and save in dict
    if accessAPI:
        similarUsers = accessUntappd.getSimilarUsers(usersTopBeers, username)
        accessUntappd.getSimilarUsersTopBeers(similarUsers, usersTopBeers)
        databaseFile.write('similarUsers = ' + pprint.pformat(similarUsers, width=1000000) + '\n')
    else:
        similarUsers = database.similarUsers

    # Obtain list of beer names from menu picture
    menuBeerList = pictureToText.extractBeerNamesFromImg(pictureFile)
    print(menuBeerList)

    # Convert list of menu beers into a dict to get beer IDs
    if accessAPI:
        menuBeerIDs = accessUntappd.getBeerIds(menuBeerList)
    else:
        menuBeerIDs = beerIDs.beerDict
    print(menuBeerIDs)

    # Go through the menu beers and update its score
    menuBeerRating = {}
    for user, similarUserTopBeers in similarUsers.items():
        for beer, bid in menuBeerIDs.items():
            if bid in similarUserTopBeers:
                similarityIndex = len(list(set(similarUserTopBeers).intersection(beerIDs.beerIDList)))
                if beer in menuBeerRating.keys():
                    menuBeerRating[beer] += similarityIndex
                else:
                    menuBeerRating[beer] = similarityIndex
                print(beer + ' - ' + user + ' - ' + str(similarityIndex))
    
    print('\n\n')
    print(menuBeerRating)

if __name__=='__main__':
    main()