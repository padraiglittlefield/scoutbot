import csv

# Calculates the average stats of the surrounding teams

def average_stats(team_stats, low, high):
    avg_team = {"Age" : 0, "Gls": 0, "Ast" : 0, "G+A" : 0, "xG" : 0, "xAG" : 0, "PrgC" : 0, "PrgP" : 0}
    for team in team_stats:
      if team_stats[team]["Ranking"] >= low and team_stats[team]["Ranking"] <= high:
        for key in team_stats[team]:
            if not key == "Ranking":
                avg_team[key] = float(avg_team[key]) + float(team_stats[team][key])

    for key in avg_team:
        avg_team[key] = round((avg_team[key]) / ((high-low) + 1), 7)
    return avg_team
    
   
# Creates a dictionary that contains the stats for every team

def team_dict():
    stats_dict = {}
    with open('ScoutBot\\team_stats.csv') as stats_file:
        stats_file 
        reader = csv.DictReader(stats_file)
        i = 1
        for row in reader:
            stats_dict[row["Squad"]]  = {"Ranking" : i, "Age" : row["Age"], "Gls": row['Gls'], "Ast" : row['Ast'], "G+A" : row['G+A'], "xG" : row['xG'], "xAG" : row['xAG'], "PrgC": row["PrgC"], "PrgP" : row["PrgP"]}
            i = i + 1

    return stats_dict

# Creates a dictionary that contains the stats for every player

def player_dict():
    stats_dict = {}
    with open('ScoutBot\player_stats.csv') as stats_file:
        stats_file 
        reader = csv.DictReader(stats_file)
        for row in reader:
            stats_dict[row["Player"]]  = {"Age" : (2023 - eval(row["Born"])),"Team" : row["Squad"] ,"Gls": row['Gls'], "Ast" : row['Ast'], "G+A" : row['G+A'], "xG" : row['xG'], "xAG" : row['xAG'], "PrgC": row["PrgC"], "PrgP" : row["PrgP"], "Total" : 0}

    return stats_dict     

# Orginal "Sum" Method for giving the players a score

def old_player_score_sum_norm(player_stats, weights):

    for stat in player_stats["Bukayo Saka"]:
        if not stat == "Team":
            stat_sum = 0
            for player in player_stats:
                stat_sum += float(player_stats[player][stat])
            for player in player_stats:
                player_stats[player][stat] = round((float(player_stats[player][stat])/(stat_sum)) * weights[stat], 20)
    
    print(player_stats["Lionel Messi"])

# Orginal "Max" Method for giving the players a score

def old_player_score(player_stats,weights):
    for stat in player_stats["Bukayo Saka"]:
        if not stat == "Team":
            max_stat = 0
            for player in player_stats:
                if float(player_stats[player][stat]) > max_stat:
                    max_stat = float(player_stats[player][stat])
            for player in player_stats:
                player_stats[player][stat] = round((float(player_stats[player][stat])/(max_stat)) * weights[stat], 20)
    
    print(player_stats["Lionel Messi"])
   


def player_score(player_stats, weights):
    for stat in player_stats["Bukayo Saka"]:
        if not stat == "Team" and not stat == "Total":
            max_norm(player_stats, weights, stat)

            for player in player_stats:
                player_stats[player]["Total"] += float(player_stats[player][stat])

    the_best = []
    for i in range(5):
        best_player = "Bukayo Saka"
        for player in player_stats:
            if player_stats[player]["Total"] > player_stats[best_player]["Total"]:
                best_player = player
        the_best.append(best_player)
        print("{}: {}".format(best_player,player_stats[best_player]["Total"]))
        del player_stats[best_player]
    return the_best




    


def sum_norm(player_stats, weights, stat):
    stat_sum = 0
    for player in player_stats:
        stat_sum += float(player_stats[player][stat])
    for player in player_stats:
        player_stats[player][stat] = round((float(player_stats[player][stat])/(stat_sum)) * weights[stat], 20)


def max_norm(player_stats,weights, stat):
    max_stat = 0
    for player in player_stats:
        if float(player_stats[player][stat]) > max_stat:
            max_stat = float(player_stats[player][stat])
    for player in player_stats:
        player_stats[player][stat] = round((float(player_stats[player][stat])/(max_stat)) * weights[stat], 20)
        if stat == "Age":
            player_stats[player][stat] = 1 - player_stats[player][stat]

        if player_stats[player]["Team"] in weights["Teams"]:
             player_stats[player][stat] = 0
    

def att_weight(team, all_stats):

    team_ranking = int(team["Ranking"])
    ave_team = average_stats(all_stats, team_ranking - 5, team_ranking + 2)

    weights = {"Age": 1, "Gls": 1, "Ast": 1, "G+A": 1, "xG" : 1, "xAG": 1, "PrgC": 1, "PrgP": 1, "Teams": []}

    for stat in weights:
        if not stat == "Teams":
            max_stat = 0

            for item in all_stats:
                if float(all_stats[item][stat]) > max_stat:
                    max_stat = float(all_stats[item][stat])
            
            
            #if stat == "Age":
            #    ave_team[stat] =  1 - (float(ave_team[stat])/max_stat)
            #  team[stat] = 1 - (float(team[stat]) / max_stat)


            ave_team[stat] = ave_team[stat]/max_stat
            team[stat] = (float(team[stat]) / max_stat)

            if stat == "Age":
                weights[stat] = (team[stat] - ave_team[stat])
            else :
                weights[stat] = (ave_team[stat] - team[stat])

            if(weights[stat] <= 0):
                weights[stat] += 1
            else:
                weights[stat] = (weights[stat] * 10) + 5
            #print("{}: {}".format(stat, max_stat))
    #print(team)
    #print(ave_team)
    #print(weights)

    teams = []
    for item in all_stats:
        if all_stats[item]["Ranking"] <= team_ranking:
            teams.append(item)


    #print(teams)
    weights["Teams"] = teams

    return weights

