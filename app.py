import betfair_connector as bf
import database as db
import datetime
import sys
import time
import ratings_scraper as rs
import analysis as an

#setup database
database=db.Euro2016DB()
database.setup()

#setup the betfair connector
client=bf.Betfair(sys.argv[1],sys.argv[2])

#setup the scraper that fetches the ELO ratings for the teams
sc = rs.ELO_Scraper()
international_ratings=sc.get_all_ratings()

#setup the analysis module 
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
                    
                    # catch differences between country names in ELO ratings and Betfair
                    if ('Rep' in home_team):
                        home_team_elo =float(international_ratings.get('Ireland'))+float(analysis.get_news_sentiment_elo_adjustment('Ireland'))
                    elif ('Rep' in away_team):
                        away_team_elo =float(international_ratings.get('Ireland'))+float(analysis.get_news_sentiment_elo_adjustment('Ireland'))
                    else:
                        home_team_elo=float(international_ratings.get(home_team))+float(analysis.get_news_sentiment_elo_adjustment(home_team))
                        away_team_elo=float(international_ratings.get(away_team))+float(analysis.get_news_sentiment_elo_adjustment(away_team))
                    # order matters when calculating the ELO difference and probabilities
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
                    
                    # store the values for the old structure/interface
                    database.store_analysis(str(datetime.datetime.now()),match_id,home_team,away_team,odds[0],odds[1],odds[2],(1/odds[0])/over_round,(1/odds[1])/over_round,(1/odds[2])/over_round,date,home_team_prob,away_team_prob,draw_prob,home_team_elo,away_team_elo,'normal')
                    # store the values for the current structure
                    database.store_odds(str(datetime.datetime.now()),match_id,name,odds[0],odds[1],odds[2],date)
                    
                 #   print home_team,": ",analysis.get_news_sentiment(home_team)
    except Warning as warn:
        print 'Warning: %s ' %warn  + '\nStop.\n'
        # wait 1 hour then run again
    time.sleep(3600)