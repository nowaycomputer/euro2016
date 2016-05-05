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
			sys.exit()

	def setup(self):
		try:
			self.cursor.execute("CREATE TABLE IF NOT EXISTS `euro_2016_betfair` (`id` int(255) NOT NULL primary key AUTO_INCREMENT, `timestamp` datetime NOT NULL, `event_id` int(255) NOT NULL, `event_name` varchar(255) NOT NULL, `home_odds` float(5) NOT NULL, `away_odds` float(5) NOT NULL, `draw_odds` float(5) NOT NULL, `event_date` datetime NOT NULL)")
			self.db.commit()
		except Warning as warn:
			#print 'Warning: %s ' %warn  + '\nStop.\n'
			sys.exit()

	def store_odds(self,timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date):
		self.cursor.execute('INSERT INTO euro_2016_betfair (timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date) VALUES (%s,%s,%s,%s,%s,%s,%s)',(timestamp,event_id,event_name,home_odds,away_odds,draw_odds,event_date))
		self.db.commit()
        
	def __del__(self):
		self.cursor.close()
		self.db.close()
