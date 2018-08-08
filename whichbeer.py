#! /usr/bin/python3.5

import accessUntappd, pictureToText, calculateScore
import sys, pprint, datetime, database

def main():
    if len(sys.argv) < 2:
        print('Usage : ./whichbeer.py <username> <menuPictureFileName>')
        sys.exit()

    username = sys.argv[1]
    pictureFile = sys.argv[2]
    # currentTime = datetime.datetime.today()
    
    now = datetime.datetime.today()
    if now - database.timeStamp < datetime.timedelta(days=1):
        databaseFile = open('database.py', 'w')
        databaseFile.write('import datetime\n')
        databaseFile.write('timeStamp = ' + pprint.pformat(now) + '\n')
        accessAPI = True
    else:
        accessAPI = False
    # Find upto 50 top rated beers by user
    print(accessAPI)

    if accessAPI:
        usersTopBeers = accessUntappd.getUsersTopBeers(username)
        databaseFile.write('usersTopBeers = ' + pprint.pformat(usersTopBeers, width=1000000) + '\n')
    else:
        usersTopBeers = database.usersTopBeers
    print(usersTopBeers)
    
    # Find up to 15 other users who also rated the top beers highly
    # similarUsers = {'Anton_W': [], 'Bordwickc': [], 'Brewbuddy313': [], 'Georgiecat': [], 'Jgrimes12': [], 'JorgesThemeSwimming': [], 'Serendipity81': [], 'Sherman14': [], 'carbomb16': [], 'jjkick123': [], 'knutemilk1': [], 'nwa_beer': [], 'samuelmarciano': [], 'timahrens': [], 'trancechemist': []}
    if accessAPI:
        similarUsers = accessUntappd.getSimilarUsers(usersTopBeers, username)
        databaseFile.write('similarUsers = ' + pprint.pformat(similarUsers, width=1000000) + '\n')
    else:
        similarUsers = database.similarUsers
    pprint.pprint(similarUsers)
    sys.exit()

    # Find how many top 10 beers of user these similar users also rated highly
    accessUntappd.updateSimilarityIndex(similarUsers, usersTopBeers)
    print('similarity index updated:')
    pprint.pprint(similarUsers)

    # Obtain list of beer names from menu picture
    menuBeerList = pictureToText.extractBeerNamesFromImg(pictureFile)

    # Convert list of menu beers into beer IDs
    menuBeers = accessUntappd.getBeerIds(menuBeerList)

    # Go through the menu beers and update its score


if __name__=='__main__':
    main()