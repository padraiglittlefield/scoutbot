import scoutbot.scoutbot as scoutbot
from scoutbot.scoutbot import *


def main():

    team_stats = team_dict()
    player_stats = player_dict()
    
    

    team = str(input("Enter a Football Team: "))



    top_rated = player_score(player_stats, att_weight(team_stats[team], team_stats))

    print("")
    print("Recommended Players for {}:".format(team))
    print("")
    for i in range(10):
        print(" {}: {} - {}, {}".format(i + 1, top_rated[i][0], top_rated[i][1], top_rated[i][2] ))
    print("")

main()
