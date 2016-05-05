# import data

# def functionCalculateResult(team 1, team 2)
# -1 = team 1 100%, +1 = team 2 100%, -0.25 - +0.25 = draw, 

# work out group results

# probably manual hacky method to get knock out results

import betfair_connector as bf
import database as db
import datetime
import sys
import time

database=db.Euro2016DB()
database.setup()
client=bf.Betfair(sys.argv[1],sys.argv[2])

# go forever
while True:
    # Get euro2016 match ids
    match_ids,match_names,match_dates=client.get_match_event_ids('4527196')

    # For each match id, get the odds
    for match_id,name,date in zip(match_ids,match_names,match_dates):
        odds= client.get_match_odds_market(match_id)
        print match_id,name, date, ' Home: ',odds[0],'(',round(100/float(odds[0]),2),'%)',' Away: ',odds[1],'(',round(100/float(odds[1]),2),'%)',' Draw: ',odds[2],'(',round(100/float(odds[2]),2),'%)'
        #def store_odds(self,timestamp,event_id,name,date,home_odds,away_odds,draw_odds):
        database.store_odds(str(datetime.datetime.now()),match_id,name,odds[0],odds[1],odds[2],date)
    
    # wait 6 hours then run again
    time.sleep(21600)