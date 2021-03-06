#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def adresseaendern(req):
    
    # this is always the same
    result = req.get("result")
    parameters = result.get("parameters")
    
    # extract parameters
    city = parameters.get("geo-city")
    zip2 = parameters.get("zip-code")
    
        
    sub = zip2[:2]  
    
    if sub == "38" : 
        if city != "Braunschweig" : 
            return {
                "speech": "Die Postleitzahl passt nicht zum Ort, wir geben uns trotzdem Mühe!",
                "displayText": "Die Postleitzahl passt nicht zum Ort, wir geben uns trotzdem Mühe!",
                #"data": {},
                # "contextOut": [],
                "source": "shippingcosttest123"
    }
    
    return {
        "speech": "Wunderbar! Wir ändern Ihre Adresse.",
        "displayText": "Wunderbar! Wir ändern Ihre Adresse.",
        #"data": {},
        # "contextOut": [],
        "source": "shippingcosttest123"

    }
    
def shippingcost(req):  
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "shippingcosttest123"

    }

def makeWebhookResult(req):
    # if req.get("result").get("action") != "shipping.cost":
    
    res = req.get("result");
    
    if res.get("action") == "shipping.cost":
        return shippingcost(req)
              
    if res.get("action") == "adresse.aendern":
        return adresseaendern(req)
    
    # add more ifs here: one for each action
    # one method for each action
    

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
