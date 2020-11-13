import pandas as pd
from fuzzywuzzy import fuzz
import nltk
from nltk.corpus import stopwords
import re

from flask import Blueprint
from flask import Flask, request, jsonify
from flask_cors import CORS

from flask_pymongo import PyMongo
import traceback 

# Init
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb+srv://Ajay:M8LMRe76xSngt8o2@cluster0-cxkfs.mongodb.net/CloudDemo"
mongo = PyMongo(app)

CORS(app)

nltk.download('stopwords')
nltk.download('punkt')


@app.route('/') #Home url
def index(): 
    return '<h1>Home Page</h1>'


@app.route('/extractTags', methods=['POST'])
def extractTags(): 

    stop_words = set(stopwords.words('english'))
    stop_words.add(".")
    stop_words.add(",")
    stop_words.add("!")
    stop_words.add("(")
    stop_words.add(")")


    result=[]
    features = []
    dbReference = mongo.db.Tags
    data = dbReference.find()

    for d in data :
        features.append(d['Tag'])
    
    match = 75
    query = request.json['query']
    # print(features)

    for feature in features:
        print(feature)
        lenfeature = len(feature.split(" "))
        word_tokens = nltk.word_tokenize(query)
        filterd_word_tokens = [w for w in word_tokens if not w in stop_words]
        for i in range (len(word_tokens)-lenfeature+1):
            wordtocompare = ""
            j=0
            for j in range(i, i+lenfeature):
                if re.search(r'[,!?{}\[\]\"\"\'\']',word_tokens[j]):
                    break
                wordtocompare = wordtocompare+" "+word_tokens[j].lower()
            wordtocompare.strip()
            if not wordtocompare=="":
                if(fuzz.ratio(wordtocompare,feature.lower())> match):
                    result.append(feature)
    if len(result) == 0:
        return jsonify({
            "isSuccess" : False,
            "Tags" : result
        })

    return jsonify({
        "isSuccess" : True,
        "Tags" : result
    })


@app.route('/addTag', methods=['POST'])
def addTags():
    
    try:
        tag = request.json['Tag']
        if len(tag) == 0:
            return jsonify({
            "isPosted" : False
        })
        dbReference = mongo.db.Tags
        dbReference.insert({
            "Tag" : tag.strip()
        })
    except Exception as e:
        print(traceback.print_exception(type(e), e, e.__traceback__))
        return jsonify({
            "isPosted" : False,
            "Message" : "Key error! required key: " + e.args[0] 
        })
    return jsonify({
        "isPosted" : True
    })

# Get all tags
@app.route('/getAllTags', methods=['GET'])
def getAllTags():
    features = []
    try:
        dbReference = mongo.db.Tags
        data = dbReference.find()

        for d in data :
            features.append(d['Tag'])
    except Exception as e:
        print(traceback.print_exception(type(e), e, e.__traceback__))
        return jsonify({
            "isFetched" : False,
            "Message" : "Db error please check logs for more info!" 
        })
    return jsonify({
        "isFetched" : True,
        "Tags" : features
    })


# Run Server
if __name__ == '__main__' :
    app.run(debug=True)
