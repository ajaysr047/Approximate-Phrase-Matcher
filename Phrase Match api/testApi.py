from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return '<h1> Home </h1>'

@app.route('/aish', methods=['POST'])
def aish():

    print("Hi this is aish!")

    return jsonify({"message" : 'Success!'})

if __name__ == '__main__' :
    app.run(debug=True)