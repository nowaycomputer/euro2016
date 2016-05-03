import sys
import json                                                                                                 
import requests
import urllib2

# set initial parameters
application_key=''
payload = 'username='+sys.argv[1]+'&password='+sys.argv[2]
login_headers = {'X-Application': application_key, 'Content-Type': 'application/x-www-form-urlencoded'}
api_headers={}
session_token=''
api_url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
login_url='https://identitysso.betfair.com/api/certlogin'

# read in app key from file
with open('../betfair/appkey.txt', 'r') as app_key_file:
  application_key=app_key_file.read().replace('\n', '')

# slightly re-written betfair api demo functions
def callAping(jsonrpc_req):
    try:
        req = urllib2.Request(api_url, jsonrpc_req, api_headers)
        response = urllib2.urlopen(req)
        jsonResponse = response.read()
        return jsonResponse
    except urllib2.URLError:
        print 'Oops no service available at ' + str(url)
        exit()
    except urllib2.HTTPError:
        print 'Oops not a valid operation from the service ' + str(url)
        exit()

# get a list of event types from the api
def getEventTypes():
    event_type_req = '{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEventTypes", "params": {"filter":{ }}, "id": 1}'
    print 'Calling listEventTypes to get event Type ID'
    eventTypesResponse = callAping(event_type_req)
    eventTypeLoads = json.loads(eventTypesResponse)
    """
    print eventTypeLoads
    """
    try:
        eventTypeResults = eventTypeLoads['result']
        return eventTypeResults
    except:
        print 'Exception from API-NG' + str(eventTypeLoads['error'])
        exit()

# get the integer value of the event type ID of interest
def getEventTypeIDForEventTypeName(eventTypesResult, requestedEventTypeName):
    if(eventTypesResult is not None):
        for event in eventTypesResult:
            eventTypeName = event['eventType']['name']
            if( eventTypeName == requestedEventTypeName):
                return  event['eventType']['id']
    else:
        print 'Oops there is an issue with the input'
        exit()  
        
# do the initial login with self-signed certs to get the session key
login_resp = requests.post(login_url, data=payload, cert=('../betfair/client-2048.pem', '../betfair/client-2048.key'), headers=login_headers)
if login_resp.status_code == 200:
  resp_json = login_resp.json()
  print resp_json['loginStatus']
  print resp_json['sessionToken']
  # set the session token for the api calls to use
  session_token=resp_json['sessionToken']
  # update future api call headers to use the session token
  api_headers = {'X-Application': application_key, 'X-Authentication': session_token, 'content-type': 'application/json'}
  print "Got a login!"
else:
  print "Request failed."

# from here down just messing about

eventTypesResult = getEventTypes()
footballEventTypeID = getEventTypeIDForEventTypeName(eventTypesResult, 'Soccer')

marketCatalogueResult = getMarketCatalogueForSoccer(footballEventTypeID)

print 'Eventype Id for Soccer is :' + str(footballEventTypeID)
#header = { 'X-Application' : "WlE2T8MseDxRI03i",  'X-Authentication' : "7udQ79Gd+xpIhcgmSAx7ZJbEjbxIQdV4xwI6JGLDkaI=", 'content-type' : 'application/json' }                                                                              
                                                                                                                                                                                                                                                                                                                                              
## GET Odds                                                                                                                                                                                                                               
#getMarketId_req='{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": {"eventTypeIds":["1"],"marketName":["Match Odds"]},"maxResults": "500","marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION"]},"id": 1}'                                                                                                                                                                                                            
#marketIdResponse = requests.post(url, data=getMarketId_req, headers=headers)    
#print(marketIdResponse)
#marketData=json.loads(marketIdResponse.text)                                                                                                                                                                                              
#resultData= marketData['result']                                                                                                                                                                                                          
                                    