import oauth2
import time
import requests
import json
import sys
import csv
import ConfigParser

Config = ConfigParser.ConfigParser()
Config.read("account.ini")

base_url = Config.get("General", "workspace")
api_key = Config.get("General", "api_key")
api_secret = Config.get("General", "api_secret")

def do_hackapad_request(api, params = None):
    api_method = base_url+api;

    # uses 0-legged OAuth signature validation
    params = {
        'oauth_version': "1.0",
        'oauth_nonce': oauth2.generate_nonce(),
        'oauth_timestamp': int(time.time()),
    }

    consumer = oauth2.Consumer(key=api_key, secret=api_secret)
    params['oauth_consumer_key'] = consumer.key
    req = oauth2.Request(method='GET', url=api_method, parameters=params)
    signature_method = oauth2.SignatureMethod_HMAC_SHA1()
    req.sign_request(signature_method, consumer, None)
    # print req.to_url()
    url = req.to_url()
    myResponse = requests.get(url)

    return myResponse

rest_rep = do_hackapad_request("api/1.0/pads/all")

if rest_rep.status_code == requests.codes.ok:
    jData = json.loads(rest_rep.content)

    print("The response contains {0} properties".format(len(jData)))

else:
    rest_rep.raise_for_status()
    sys.exit(1)

with open('pad_list.csv', 'w') as csvfile:
    fieldnames = ['URL', 'Title']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while jData:
        padId = jData.pop()
        combined_api = "api/1.0/pad/"+ padId + "/content/latest.txt"
        #print combined_api
        rest_rep = do_hackapad_request(combined_api)

        if rest_rep.status_code == requests.codes.ok:
            print base_url+padId, rest_rep.content[:rest_rep.content.find("\n")]
            writer.writerow({'URL': base_url+padId, 'Title': rest_rep.content[:rest_rep.content.find("\n")]})

        else:
            rest_rep.raise_for_status()
            sys.exit(1)