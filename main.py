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
    #since in the text the last line is empty
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

def Search(string_):
    json_data = index()

    #by using upper() we can make it case insensitive since Dinner would be the same word as dinner
    wanted_word = string_.upper()
    count_of_word_per_sentence = 0

    dict = {}
    for sentence in json_data['data']:
        for word in sentence.split():
            #remove special characters so for example "dinner." is now "dinner"
            #using regex
            word = re.sub('[^A-Za-z0-9]+', '', word).upper()
            if(wanted_word == word):
                count_of_word_per_sentence += 1

        dict[sentence] = count_of_word_per_sentence
        count_of_word_per_sentence = 0

        #Sorts the dictionary and reverses the order since the instructions said the first should have the most multiple of a word
        sorted_dict = sorted(dict.items(),key=lambda x:x[1], reverse=True)

    #create a new list where we keep only the keys from the dictionary already in the correct order
    data = []
    for key, value in sorted_dict:
        data.append(key)

    json_write = {
        "results": data,
        "error": "error string"
    }

    json_string = json.dumps(json_write)
    json_object = json.loads(json_string)

    return json_object

def main():
    saveData("https://gist.githubusercontent.com/marshyski/d5839816c2ea730185b0af3570cbc2f7/raw/d6aebfc3f0c202b17fe6b27aae023297d9ba6a67/sentences.json")
    #Test case 1 print(Search("we"))
    #Test case 2 print(Search("IN"))
    #Test case 3 print(Search("dinner"))
    #Test case 4 print(Search("DiNner"))
    #Test case 5 print(Search("I"))

if __name__ == "__main__":
    main()

#A way we can improve the solution is by doing multithreading or multiprocesses since we are going through every sentence in the the "sentences", I can create a multithreading function to have them all being checked at the same time
#saving so much time on the solution instead of waiting one by one.
#At the moment the program does not distinguish between I and I've. Althought the word "I" is technically in I've = "I have". Another way we can improve the program
#is to create a try and catch safety addition for example in the case one inputs a number in the Search function, since the Search function only takes in a string, having an int variable
#will produce errors. We can add a try and catch to catch all the exceptions that could make it crash.