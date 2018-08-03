#! /usr/bin/python3.5

from PIL import Image
import pytesseract, sys

def pictureToText(imageName):
    return pareseMenuText(pytesseract.image_to_string(Image.open(imageName)))

def parseMenuText(menuText):
    menuBeerNames = []

if len(sys.argv) > 1:
    print(pytesseract.image_to_string(Image.open(sys.argv[1])))