#! /usr/bin/python3.5

import accessUntappd, pictureToText, calculateScore
import sys

if len(sys.argv) < 2:
    print('Usage : ./whichbeer.py <username> <menuPictureFileName>')
    sys.exit()

username = sys.argv[1]
pictureFile = sys.argv[2]

# Find up to 10 top rated beers by user
usersTopBeers = accessUntappd.getUsersTopBeers(username)

# Find other users who also rated the top 10 beers highly
similarUsers = accessUntappd.getSimilarUsers(usersTopBeers)

# Find how many top 10 beers of user these similar users also rated highly
accessUntappd.updateSimilarityIndex(similarUsers, usersTopBeers)

# Obtain list of beer names from menu picture
menuBeerList = pictureToText.pictureToText(pictureFile)

# Obtain menu beers
#menuBeers = accessUntappd.getBeerIds(menuBeerList)

# Go through the menu beers and update its score


if __name__=='__main__':
    main()