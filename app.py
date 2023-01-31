from flask import Flask, render_template, request, make_response
import numpy as np
import pandas as pd
import pickle
import json

app = Flask(__name__)

model = pickle.load(open('linearmodel.pkl', 'rb'))

@app.route('/')
def home():
    return 'Hello, I am Jarvis'

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    year = parameters.get("year")

    intent = result.get("intent").get('displayName')

    if intent == 'DataYes':
        prediction = model.predict([[year]])
        output = round(prediction[0], 2)

        fulfillmentText = "The predicted value for year " + str(year) + " is " + str(output)

        return {"fulfillmentText": fulfillmentText}

if __name__ == '__main__':
    app.run(debug=True)