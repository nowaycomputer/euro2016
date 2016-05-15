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
import ratings_scraper as rs
import analysis as an

database=db.Euro2016DB()
database.setup()
client=bf.Betfair(sys.argv[1],sys.argv[2])

sc = rs.ELO_Scraper()
international_ratings=sc.get_all_ratings()

analysis=an.Analysis()

# go forever
while True:
    try:
        # Get euro2016 match ids
        match_ids,match_names,match_dates=client.get_match_event_ids('4527196')
        if match_ids is not None and match_names is not None and match_dates is not None:
            
            # For each match id, get the odds
            for match_id,name,date in zip(match_ids,match_names,match_dates):
                odds= client.get_match_odds_market(match_id)
                if (len(odds)==3):
                    print match_id,name, date, ' Home: ',odds[0],'(',round(100/float(odds[0]),2),'%)',' Away: ',odds[1],'(',round(100/float(odds[1]),2),'%)',' Draw: ',odds[2],'(',round(100/float(odds[2]),2),'%)'
                    
                    # calculate what the result SHOULD BE
                    over_round=1/odds[0]+1/odds[1]+1/odds[2]
                    teams=name.split(' v ')
                    home_team=teams[0]
                    away_team=teams[1]
                  
                    home_team_elo=international_ratings.get(home_team)
                    away_team_elo=international_ratings.get(away_team)
                    
                    # catch differences between country names in ELO ratings and Betfair
                    if ('Rep' in home_team):
                        home_team_elo =international_ratings.get('Ireland')
                    elif ('Rep' in away_team):
                        away_team_elo =international_ratings.get('Ireland')
                        
                    if (home_team_elo>away_team_elo):
                        probs = analysis.get_probabilities_from_elo(home_team_elo,away_team_elo)
                        home_team_prob=probs[0]
                        away_team_prob=probs[1]
                        draw_prob=probs[2]
                    else:
                        probs = analysis.get_probabilities_from_elo(away_team_elo, home_team_elo)
                        home_team_prob=probs[1]
                        away_team_prob=probs[0]
                        draw_prob=probs[2]
                        
                    print home_team, home_team_elo, home_team_prob
                    print away_team, away_team_elo, away_team_prob
                    print 'Draw: ', draw_prob
                    
                    database.store_analysis(str(datetime.datetime.now()),match_id,home_team,away_team,odds[0],odds[1],odds[2],(1/odds[0])/over_round,(1/odds[1])/over_round,(1/odds[2])/over_round,date,home_team_prob,away_team_prob,draw_prob,home_team_elo,away_team_elo,'normal')
                    #timestamp,event_id,home_team,away_team,home_odds,away_odds,draw_odds,home_odds_prob, 
                    # away_odds_prob,draw_odds_prob,event_date,calc_draw_prob,calc_away_prob,elo_home,elo_away,match_type):
                    
                    # old page, continue to generate
                    database.store_odds(str(datetime.datetime.now()),match_id,name,odds[0],odds[1],odds[2],date)
    except Warning as warn:
        print 'Warning: %s ' %warn  + '\nStop.\n'
        # wait 6 hours then run again
    time.sleep(3600)