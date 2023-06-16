import csv


MIN_MATCHES= 15

U27_BUFF = 1.2
U24_BUFF = 1.3
U21_BUFF = 1.5

OLD_NERF = .8

IGNORE = ["Team","Total","MP","Age"]

# Calculates the average stats of the surrounding teams

def average_stats(team_stats, low, high):
    avg_team = {"Age" : 0, "Gls": 0, "Ast" : 0, "xG" : 0, "xAG" : 0, "PrgC" : 0, "PrgP" : 0, "DefTac": 0, "MidTac" : 0, "AttTac" : 0, "Blocks" : 0, "Int" : 0}
    for team in team_stats:
      if int(team_stats[team]["Ranking"]) >= low and int(team_stats[team]["Ranking"]) <= high:
        for key in team_stats[team]:
            if not key == "Ranking":
                avg_team[key] = float(avg_team[key]) + float(team_stats[team][key])

    for key in avg_team:
        avg_team[key] = round((avg_team[key]) / ((high-low) + 1), 7)
    return avg_team
    
   
# Creates a dictionary that contains the stats for every team

def team_dict():
    stats_dict = {}
    with open('team_stats.csv') as stats_file: 
        reader = csv.DictReader(stats_file)
        for row in reader:
            stats_dict[row["Squad"]]  = {"Ranking" : row["Ranking"], "Age" : row["Age"], "Gls": row['Gls'], "Ast" : row['Ast'], "xG" : row['xG'], "xAG" : row['xAG'], "PrgC": row["PrgC"], "PrgP" : row["PrgP"], "DefTac": row["Def 3rd"], "MidTac" : row["Mid 3rd"], "AttTac" : row["Att 3rd"], "Blocks" : row["Blocks"], "Int" : row["Int"]}

    return stats_dict

# Creates a dictionary that contains the stats for every player

def player_dict():
    stats_dict = {}
    with open('player_stats.csv') as stats_file: 
        reader = csv.DictReader(stats_file)
        for row in reader:
            stats_dict[row["Player"]]  = {"Age" : (2023 - eval(row["Born"])),"Team" : row["Squad"] ,"Gls": row['Gls'], "Ast" : row['Ast'], "xG" : row['xG'], "xAG" : row['xAG'], "PrgC": row["PrgC"], "PrgP" : row["PrgP"], "Total" : 0, "DefTac": row["Def 3rd"], "MidTac" : row["Mid 3rd"], "AttTac" : row["Att 3rd"], "Blocks" : row["Blocks"], "Int" : row["Int"], "MP" : row["MP"]}

    return stats_dict     


def player_score(player_stats, weights):
   
    for stat in player_stats["Bukayo Saka"]:
        if stat not in IGNORE:
            max_norm(player_stats, weights, stat)

            for player in player_stats:
                player_stats[player]["Total"] += float(player_stats[player][stat])

    the_best = []

  
    for i in range(10):
        best_player = "Padraig Littlefield"
        for player in player_stats:
            if player_stats[player]["Total"] > player_stats[best_player]["Total"]:
                best_player = player

        the_best.append((best_player,player_stats[best_player]["Team"],player_stats[best_player]["Age"]))

        print("{}: {}".format(best_player,player_stats[best_player]["Total"]))
        del player_stats[best_player]
    return the_best


def max_norm(player_stats,weights, stat):

    max_stat = 0
    max_player = ""
    for player in player_stats:
        if float(player_stats[player][stat]) > max_stat and float(player_stats[player]["MP"]) > 15:
            max_stat = float(player_stats[player][stat])
            

    print("{}: {} - {}".format(stat, max_stat, max_player))

    for player in player_stats:

        player_age = player_stats[player]["Age"]

        player_stats[player][stat] = round((float(player_stats[player][stat])/(max_stat)) * weights[stat], 20)

        if player_age <= 21:
            player_stats[player][stat] *= U21_BUFF
        elif player_age <= 24:
            player_stats[player][stat] *= U24_BUFF
        elif player_age <= 27:
            player_stats[player][stat] *= U27_BUFF           
        else:
            player_stats[player][stat] *= OLD_NERF


        if int(player_stats[player]["MP"]) < MIN_MATCHES:
            player_stats[player][stat] = 0

        if player_stats[player]["Team"] in weights["Teams"]:
             player_stats[player][stat] = 0
    

def att_weight(team, all_stats):

    team_ranking = int(team["Ranking"])
    teams = []

    if team_ranking <= 5:
        ave_team = average_stats(all_stats, 1 , 5)

        for item in all_stats:
            if int(all_stats[item]["Ranking"]) <= 6:
               teams.append(item)
       
    else:
        ave_team = average_stats(all_stats, team_ranking - 5, team_ranking + 2)

        for item in all_stats:
            if int(all_stats[item]["Ranking"]) <= team_ranking + 3:
                teams.append(item)

    weights = {"Age": 1, "Gls": 1, "Ast": 1,  "xG" : 1, "xAG": 1, "PrgC": 1, "PrgP": 1, "Teams": [], "DefTac": 1, "MidTac" : 1, "AttTac" : 1, "Blocks" : 1, "Int" : 1}
    

    stat_sum = 0

    for stat in weights:
        if not stat == "Teams":
            max_stat = 0

            for item in all_stats:
                if float(all_stats[item][stat]) > max_stat:
                    max_stat = float(all_stats[item][stat])

            print("{}: {}".format(stat, max_stat))
            ave_team[stat] = ave_team[stat]/max_stat
            team[stat] = (float(team[stat]) / max_stat)

           
      
            weights[stat] = (ave_team[stat] - team[stat])

            if weights[stat] > 0:
                stat_sum += weights[stat]
            """
            if(weights[stat] <= 0):
                weights[stat] += 1
            else:
                weights[stat] = (weights[stat] * 100) """
            
    for stat in weights:
    
        if stat not in IGNORE and not stat == "Teams":
            print(stat)
            if weights[stat] > 0:
                weights[stat] = (weights[stat]/stat_sum) * 20
            else:
                weights[stat] += 1



    weights["Teams"] = teams
    print(teams)
    print(weights)
    return weights
