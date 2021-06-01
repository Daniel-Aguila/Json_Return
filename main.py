import json
from urllib.request import urlopen
import re

def saveData(json_url):
    json_object = urlopen(json_url) #gets the json object from the http request
    data = json.loads(json_object.read())
    
    #creates a local file where we can write the information from the json object
    file = open("local.txt","w")
    for sentence in data['sentences']:
        #Since the encoding for the single quotation ' was showing as "\u2019" we replaced it with the appropriate symbol
        sentence = sentence.replace("\u2019","'")
        file.write(sentence + "\n")
    file.close()

def index():
    file = open("local.txt", "r")
    lines = file.read()
    lines = lines[:-1]

def main():
    saveData("https://gist.githubusercontent.com/marshyski/d5839816c2ea730185b0af3570cbc2f7/raw/d6aebfc3f0c202b17fe6b27aae023297d9ba6a67/sentences.json")
    index()
if __name__ == "__main__":
    main()

