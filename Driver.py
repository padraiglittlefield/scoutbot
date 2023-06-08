import scoutbot
from scoutbot import *


def main():

    team_stats = team_dict()
    player_stats = player_dict()
    

    
    weights = {"Age": 1, "Gls": 1, "Ast": 1, "G+A": 1, "xG" : 1, "xAG": 1, "PrgC": 1, "PrgP": 1}
    
    team = str(input("Enter a Football Team: "))
    
    top_rated = player_score(player_stats, att_weight(team_stats[team], team_stats))
    for i in range(5):
        print("{}: {}".format(i + 1, top_rated[i]))
    
    
main()
