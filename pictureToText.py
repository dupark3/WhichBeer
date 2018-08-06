#! /usr/bin/python3.5

from PIL import Image
import pytesseract, sys

def extractBeerNamesFromImg(imageName):
    return parseMenuText(pytesseract.image_to_string(Image.open(imageName)))

def parseMenuText(menuText):
    menuBeerNames = []
    allBeerNames = { }
    beerfile = open('beernames.txt', 'r')
    for line in beerfile.readlines():
        allBeerNames[line[:-1]] = 1
    print('all beer count: ' + str(len(allBeerNames)))

    for line in menuText.split('\n'):
        lineList = line.split()
        for i in range(len(lineList)):
            phrase = ' '.join(lineList[:i])
            if phrase in allBeerNames:
                menuBeerNames.append(phrase)
                print('phrase added: ' + phrase)
    
    print('total added : ' + str(len(menuBeerNames)))
    beerfile.close()
    return menuBeerNames

# extractBeerNamesFromImg('exampleMenu.jpg')

if len(sys.argv) > 1:
    filename = sys.argv[1]
    print(pytesseract.image_to_string(Image.open(filename)))