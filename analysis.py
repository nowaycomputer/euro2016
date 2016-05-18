import numpy as np
import urllib2
import socket
from bs4 import BeautifulSoup
from nltk import tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Analysis:
    def __init__(self):
        pass
    
    # calculates the overround for a given set of odds
    # returns a set of odds normalised for the overround
    def get_normalised_overround_prob(self,odds):
        cum_prob=0
        for d in odds:
            cum_prob=cum_prob+(1/d)
        normalised_probs=[]
        for d in odds:
            normalised_probs.append(d/cum_prob)
    
    # returns the probabilities of a higher rated
    # team (A) against a lower rated team (B)
    # 
    # Pr(A) = 1 / (10^(-ELODIFF/400) + 1)
    def get_probabilities_from_elo(self,elo_A,elo_B):
        elo_diff=float(elo_A)-float(elo_B)
        p_a= 1/(np.power(10,(-1*elo_diff/400))+1)
        p_b= 1-p_a
        
        # calculate the draw prob
        p_d= self.get_draw_prob(p_a,p_b)
        
        # adjust the win prob based on the draw prob
        p_a=p_a-p_d/2
        p_b=p_b-p_d/2
        
        return round(p_a,3),round(p_b,3),round(p_d,3)
              
    # estimate prob of a draw - very rough, taken from the average of last few euro tournaments    
    def get_draw_prob(self,prob_A, prob_B):
        return -0.3556*(prob_A-prob_B)+0.3556
    
    # takes a team names and searches for recent news stories (last 7 days)
    # based on the approximate sentiment, it returns an ELO adjustment
    # a maximum of 10 point elo adjustment is pre-set as a typical maximum exchanged
    # between higher rated teams
    def get_news_sentiment_elo_adjustment(self,team):
        max_elo_change=10.
        story_limit=5 
        neg=0
        pos=0
        visible_text=''
        #negative phrases=['unfit','will not be fit','not fit','injured','injuries','depressed','disappointed','controversy','scandal','home','conceded']
        positive_phrases=['fully fit','strong','scored']
        negative_phrases=['unfit','injured']
        base_url='https://www.google.co.uk/search?hl=en&gl=uk&tbm=nws&authuser=0&q=football+european+championships'+team.replace(' ','%20')
        req = urllib2.Request(base_url,headers = {'User-Agent': 'Mozilla/5.0'} )
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page)
        # remove scripts and tags
        for script in soup(["script", "style"]):
                script.extract()    # rip it out
        # find the links
        sentence_count=0
        score=0
        story_count=0
        for a in soup.findAll('a'):
            if story_count<story_limit:
                # ignore internal google links and remove the tracking guff from the end of the URL
                if ('google' not in a.attrs['href'] and '/search?q=football+european+championships' not in a.attrs['href'] and 'http://' in a.attrs['href']):
                    print a.attrs['href'].replace('/url?q=','').split('&')[0]
                    story_req=urllib2.Request(a.attrs['href'].replace('/url?q=','').split('&')[0],headers={'User-Agent': 'Mozilla/5.0'})
                    try:
                        story_page=urllib2.urlopen(story_req,timeout=5)
                        story_soup=BeautifulSoup(story_page)
                        # analyse text
                        visible_text = story_soup.getText()
                        neg=0
                        pos=0
                        sentences = tokenize.sent_tokenize(visible_text)
                        sid = SentimentIntensityAnalyzer()
                        # for each sentence in the story, get the sentiment/polarity
                        for sentence in sentences:
                            ss = sid.polarity_scores(sentence)
                            neg=neg+ss['neg']
                            pos=pos+ss['pos']
                        sentence_count=sentence_count+ len(sentences)
                        score=score+pos-neg
                        # print out a story by story sentiment for logging
                        print 'Sentiment: ',(pos-neg)/len(sentences)
                    except socket.timeout as e:
                        print type(e)    
                    except urllib2.HTTPError:
                        print 'failed on url: ',a.attrs['href']
                    story_count=story_count+1 
        # calculate an average sentiment based on all of the stories
        # return an elo_adjustment based on the max elo change and the sentiment
        norm_sentiment_score=(pos-neg)/len(sentences)
        return norm_sentiment_score*max_elo_change


        norm_sentiment_score=(pos-neg)/len(visible_text)
        
        # do the scraping
        # do the sentiment analysis
        # do the normalising
        
        return norm_sentiment_score*max_elo_change
        