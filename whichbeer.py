#! /usr/bin/python3.5

import accessUntappd, pictureToText, calculateScore
import sys, pprint

def main():
    if len(sys.argv) < 2:
        print('Usage : ./whichbeer.py <username> <menuPictureFileName>')
        sys.exit()

    username = sys.argv[1]
    pictureFile = sys.argv[2]

    # Find up to 10 top rated beers by user
    #usersTopBeers = accessUntappd.getUsersTopBeers(username)
    usersTopBeers = ['36834', '1944006', '54386', '1752507', '1353']
    print(usersTopBeers)

    # Find other users who also rated the top 10 beers highly
    similarUsers = accessUntappd.getSimilarUsers(usersTopBeers)
    pprint.pprint(similarUsers)

    # Find how many top 10 beers of user these similar users also rated highly
    # accessUntappd.updateSimilarityIndex(similarUsers, usersTopBeers)

    # Obtain list of beer names from menu picture
    # menuBeerList = pictureToText.extractBeerNamesFromImg(pictureFile)

    # Convert list of 
    # menuBeers = accessUntappd.getBeerIds(menuBeerList)

    # Go through the menu beers and update its score


if __name__=='__main__':
    main()