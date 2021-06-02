import json
from urllib.request import urlopen
import re
import collections

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

    data = []
    for line in lines.splitlines():
        data.append(line)

    json_write = {
        "data": data,
        "error": "error string"
    }

    #create a json string and then a json object
    #json loads returns an object from a json representing string
    json_string = json.dumps(json_write)
    json_object = json.loads(json_string)
    file.close()

    return json_object

def search(string_):
    json_data = index()
    wanted_word = string_.upper()
    count_of_word_per_sentence = 0

    dict = {}
    count = 0
    for sentence in json_data['data']:
        myList = []
        count+=1
        for word in sentence.split():
            #remove special characters so for example "dinner." is now "dinner"
            word = re.sub('[^A-Za-z0-9]+', '', word).upper()
            if(wanted_word == word):
                count_of_word_per_sentence += 1
        myList.append(count_of_word_per_sentence)
        count_of_word_per_sentence = 0
        dict[sentence] = myList

        sorted_dict = sorted(dict.items(),key=lambda x:x[1], reverse=True)

    data = []
    for key, value in sorted_dict:
        data.append(key)
    json_write = {
        "results": data,
        "error": "error string"
    }

    #create a json string and then a json object
    #json loads returns an object from a json representing string
    json_string = json.dumps(json_write)
    json_object = json.loads(json_string)

    return json_object

def main():
    saveData("https://gist.githubusercontent.com/marshyski/d5839816c2ea730185b0af3570cbc2f7/raw/d6aebfc3f0c202b17fe6b27aae023297d9ba6a67/sentences.json")
    print(search("we"))
    print(search("In"))
    print(search("dinner"))
    print(search("Dinner"))
if __name__ == "__main__":
    main()