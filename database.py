import MySQLdb
import datetime as dt
from warnings import filterwarnings

# setup the database
class Euro2016DB:
	def __init__(self):
#		filterwarnings('ignore', category = MySQLDb.Warning)
		self.user = 'euro'
		self.password = '2016'
		self.host = 'localhost'
		self.db='euro2016'
		try:
			self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.password,db=self.db)   
			self.cursor = self.db.cursor()
			self.cursor.execute('select version()')
			print 'Connection OK'
		except MySQLdb.Error as error:
			print 'Error: %s ' %error + '\nStop.\n'

	def setup(self):
		try:
            
# old database structure            
			self.cursor.execute("CREATE TABLE IF NOT EXISTS `euro_2016_betfair` (`id` int(255) NOT NULL primary key AUTO_INCREMENT, `timestamp` datetime NOT NULL, `event_id` int(255) NOT NULL, `event_name` varchar(255) NOT NULL, `home_odds` float(5) NOT NULL, `away_odds` float(5) NOT NULL, `draw_odds` float(5) NOT NULL, `event_date` datetime NOT NULL)")     
			self.cursor.execute("CREATE TABLE IF NOT EXISTS `euro_2016_elo` (`id` int(255) NOT NULL primary key AUTO_INCREMENT, `timestamp` datetime NOT NULL, `elo_type` varchar(255) NOT NULL, `value` float(5) NOT NULL, `team` varchar(255) NOT NULL)")
                        
# new database structure
			self.cursor.execute("CREATE TABLE IF NOT EXISTS `euro_2016_analysis` (`id` int(255) NOT NULL primary key AUTO_INCREMENT, `timestamp` datetime NOT NULL, `event_id` int(255) NOT NULL, `home_team` varchar(255) NOT NULL, `away_team` varchar(255) NOT NULL, `home_odds` float (5) NOT NULL, `away_odds` float (5) NOT NULL, `draw_odds` float (5) NOT NULL, `odds_home_prob` float(5) NOT NULL, `odds_away_prob` float(5) NOT NULL, `odds_draw_prob` float (5) NOT NULL, `event_date` datetime NOT NULL, `calc_draw_prob` float (5) NOT NULL,`calc_home_prob` float (5) NOT NULL,`calc_away_prob` float (5) NOT NULL,`elo_home` int(255) NOT NULL, `elo_away` int(255) NOT NULL, `type` varchar(255) NOT NULL )") 
			self.db.commit()
		except Warning as warn:
			print warn

	def store_odds(self,timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date):
		self.cursor.execute('INSERT INTO euro_2016_betfair (timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date))
		self.db.commit()

	def store_elo(self,timestamp,elo_type,value,team):
		self.cursor.execute('INSERT INTO euro_2016_elo (timestamp,elo_type,value,team) VALUES (%s,%s,%s,%s)',(timestamp,elo_type,value,team))
		self.db.commit()
        
	def store_analysis(self, timestamp,event_id,home_team,away_team,home_odds,away_odds,draw_odds,home_odds_prob, away_odds_prob,draw_odds_prob,event_date,calc_home_prob,calc_away_prob,calc_draw_prob,elo_home,elo_away,match_type):
		self.cursor.execute('INSERT INTO euro_2016_analysis (timestamp,event_id,home_team,away_team,home_odds,away_odds,draw_odds,odds_home_prob,odds_away_prob,odds_draw_prob,event_date,calc_home_prob,calc_away_prob,calc_draw_prob,elo_home,elo_away,type) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (timestamp,event_id,home_team,away_team,home_odds,away_odds,draw_odds,home_odds_prob, away_odds_prob,draw_odds_prob,event_date,calc_home_prob,calc_away_prob,calc_draw_prob,elo_home,elo_away,match_type))
		self.db.commit()
        
	def __del__(self):
		self.cursor.close()
		self.db.close()
