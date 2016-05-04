import sys
import json                                                                                                 
import requests
import urllib2

class Betfair:
    
    def __init__(self, username,password):
        # set initial parameters
        self.application_key=''
        self.payload = 'username='+username+'&password='+password
        self.api_headers={}
        self.session_token=''
        self.api_url = 'https://api.betfair.com/exchange/betting/json-rpc/v1'
        self.login_url='https://identitysso.betfair.com/api/certlogin'
        # read in app key from file
        with open('../betfair/appkey.txt', 'r') as app_key_file:
            self.application_key=app_key_file.read().replace('\n', '')
        # do the initial login with self-signed certs to get the session key
        self.login_headers = {'X-Application': self.application_key, 'Content-Type': 'application/x-www-form-urlencoded'}
        login_resp = requests.post(self.login_url, data=self.payload, cert=('../betfair/client-2048.pem', '../betfair/client-2048.key'), headers=self.login_headers)
        if login_resp.status_code == 200:
            resp_json = login_resp.json()
            print resp_json['loginStatus']
            #print resp_json['sessionToken']
            # set the session token for the api calls to use
            self.session_token=resp_json['sessionToken']
            # update future api call headers to use the session token
            self.api_headers = {'X-Application': self.application_key, 'X-Authentication': self.session_token, 'content-type': 'application/json'}
            print "Got a login!"
        else:
            print "Request failed."

    # slightly re-written betfair api demo functions
    def callAping(self,jsonrpc_req):
        try:
            req = urllib2.Request(self.api_url, jsonrpc_req, self.api_headers)
            response = urllib2.urlopen(req)
            jsonResponse = response.read()
            return jsonResponse
        except urllib2.URLError:
            print 'Oops no service available at ' + str(url)
            exit()
        except urllib2.HTTPError:
            print 'Oops not a valid operation from the service ' + str(url)
            exit()
    
    def getEuro2016Odds(self):
        # 4527196 is hardcoded as the competition id
        euro_matches_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{ "competitionIds" : ["4527196"]  }}}'
        euro_matches=json.loads(self.callAping(euro_matches_req))
        #print json_matches
        matches=euro_matches['result'] 
        for m in matches:
            # get group stage games
            if ('Group' not in m['event']['name'] and 'Euro' not in m['event']['name']):
                print m['event']['id'], m['event']['name']
                # get the market ID for the game
                getMarketId_req='{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": {"eventIds":["'+m['event']['id']+'"],"marketName":["Match Odds"]},"maxResults": "500","priceProjection" : { "priceData": ["EX_BEST_OFFERS"]}}}'
                market_ids=json.loads(self.callAping(getMarketId_req))
                markets=market_ids['result']
                for m in markets:
                    if 'Match Odds' in m['marketName']:
                        # get the market id for match odds
                        #print 'market ID: ',m['marketId']
                        get_match_odds_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listMarketBook", "params": {"marketIds":["'+m['marketId']+'"],"priceProjection":{"priceData":["EX_BEST_OFFERS"],"virtualise":"true"}}, "id": 1}'
                        match_odds=json.loads(self.callAping(get_match_odds_req))
                        home_odds=match_odds['result'][0]['runners'][0]['ex']['availableToBack'][0]['price']
                        away_odds=match_odds['result'][0]['runners'][1]['ex']['availableToBack'][0]['price']
                        draw_odds=match_odds['result'][0]['runners'][2]['ex']['availableToBack'][0]['price']
                        print('home odds:',home_odds)
                        print('away odds:',away_odds)
                        print('draw odds:',draw_odds)


    

    # from here down just messing about
#client=Betfair(sys.argv[1],sys.argv[2])
#euro_matches_req='{"jsonrpc": "2.0", "method": "SportsAPING/v1.0/listEvents", "params": {"filter":{ "competitionIds" : ["4527196"]  }}}'        
#print(json.loads(client.callAping(euro_matches_req)))

    ## GET Odds                                                                                                                                                                                                                               
    #getMarketId_req='{"jsonrpc": "2.0","method": "SportsAPING/v1.0/listMarketCatalogue","params": {"filter": {"eventTypeIds":["1"],"marketName":["Match Odds"]},"maxResults": "500","marketProjection": ["COMPETITION","EVENT","EVENT_TYPE","RUNNER_DESCRIPTION"]},"id": 1}'                                                                                                                                                                                                            
    #marketIdResponse = requests.post(url, data=getMarketId_req, headers=headers)    
    #print(marketIdResponse)
    #marketData=json.loads(marketIdResponse.text)                                                                                                                                                                                              
    #resultData= marketData['result']                                                                                                                                                                                                          
                                    