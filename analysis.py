import numpy as np

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
        