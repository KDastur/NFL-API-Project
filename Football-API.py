import requests
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

url = "https://api.sportsdata.io/v3/nfl/stats/json/PlayerSeasonStats/2025reg?key=ca9d175c962e4b2f911441b1b848e375"

headers = {
    "X-RapidAPI-Key": "ca9d175c962e4b2f911441b1b848e375",
    "X-RapidAPI-Host": "sportsdata.io/developers/api-documentation/nfl#team-player-stats"
}
response = requests.get(url, headers=headers)
players = response.json()

df = pd.DataFrame(players)
df = df.set_index("Name")

while True:
    action = input("\nWhat would you like to do?\n(1) Search Player\n(2) Compare Players\n(3) Filter by Position and Statistic\n(4) View Positional Graphs\n(5) Exit\n")

#Search a single player

    if action == "1":
        pl_name = input("What Player would you like to view? (First Initial.Last Name)\n")
        if pl_name in df.index:
            print()
            print(df.loc[pl_name][["RushingYards", "ReceivingYards", "PassingYards"]].to_string())
            print()

    #Bar Graph for player stats

            stats = [df.loc[pl_name]["RushingYards"], df.loc[pl_name]["ReceivingYards"], df.loc[pl_name]["PassingYards"]]
            labels = ["Rush Yds", "Receiving Yds", "Pass Yds"]
            plt.bar(labels, stats)
            plt.title(f"{pl_name} Stats")
            plt.ylabel("Yards")
            plt.show()
        else:
            print("\nPlayer Not Found\n")

#Compare Players

    elif action == "2":
        while True:
            pl1 = input("\nChoose the first player to compare: (First Initial.Last Name)\n")
            if pl1 in df.index:
                break
            else:
                print("\nInvalid Input, Try again\n")
                continue
        while True:
            pl2 = input("\nChoose Another Player (First Initial.Last Name)\n")
            if pl2 in df.index:
                break
            elif pl2 == pl1:
                print("\nPlayer has already been entered, Try again")
                continue
            else:
                print("\nInvalid Input, Try again\n")
                continue
            
        pl_names = [pl1, pl2]
        while True:
            next_player = input("\nChoose another player to compare (First Initial.Last Name), or type Done to see results\n")
            if next_player == "Done":
                break
            elif next_player not in df.index:
                print("\nInvalid Input, Try again\n")
                continue
            elif next_player in pl_names:
                print("\nPlayer has already been added\n")
                continue
            else:
                pl_names.append(next_player)
        print()
        print(df.loc[pl_names][["RushingYards", "ReceivingYards", "PassingYards"]])
        print()

    #Stacked Bar graph

        rushing = df.loc[pl_names]["RushingYards"]
        receiving = df.loc[pl_names]["ReceivingYards"]
        passing = df.loc[pl_names]["PassingYards"]
        
        plt.bar(pl_names, rushing, label="Rushing", color="green")
        plt.bar(pl_names, receiving, bottom=rushing, label="Receiving", color="blue")
        plt.bar(pl_names, passing, bottom=rushing+receiving, label="Passing", color="red")

        plt.ylim(0, 3500)
        plt.ylabel("Total Yards")
        plt.title("Player Comparison")
        plt.legend()
        plt.show()

#Filter by position and Statistic

    elif action == "3":
        while True:
            pos = input("\nWhat Position would you like to sort through (ex: RB, WR, QB...):\n").upper()
            if pos in df["Position"].values:
                break
            else:
                print("\nInvalid Position, try again\n")
                continue
        while True:
            stat = input("\nWhat Statistic would you like to view (No Spaces)(ex: RushingYards, RushingTouchdowns...)\n")
            if stat in df.columns:
                break
            else:
                print("\nInvalid Statistic, try again\n")
                continue
        sort_df = df[df["Position"] == pos]
        sort_df = sort_df.sort_values(by=stat, ascending=False)
        print(sort_df[["Position", stat]].head(10))
        print()

    

        

#Plotting Statistics

    elif action == "4":
        pos = input("\nChoose to view the top 20 for yards in these Three Positions:\n(1) RB\n(2) WR\n(3) QB\n")

        top_wr = df[df["Position"]=="WR"].sort_values("ReceivingYards", ascending=False).head(20)
        top_rb = df[df["Position"]=="RB"].sort_values("RushingYards", ascending=False).head(20)
        top_qb = df[df["Position"]=="QB"].sort_values("PassingYards", ascending=False).head(20)

        if pos == "1":

    #Adding a line of best fit

            x = top_rb["RushingAttempts"]
            y = top_rb["RushingYards"]
            plt.scatter(x, y, color="green")
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x+b, color="red", linestyle="--", label="Best Fit")
            
    #Labeling each point

            for i, player in enumerate(top_rb.index): 
                plt.text(x.iloc[i], y.iloc[i], player, fontsize=5, ha='right', va='bottom')

            plt.grid(True)
            plt.xlabel("Rushing Att")
            plt.ylabel("Rushing Yds")
            plt.title("Top 20 RBs: Rushing Attempts vs Rushing Yards")
            plt.legend()
            plt.show()

        elif pos == "2":

            x = top_wr["Receptions"]
            y = top_wr["ReceivingYards"]
            plt.scatter(x, y, color="blue")
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x+b, color="red", linestyle="--", label="Best Fit")

            for i, player in enumerate(top_wr.index): 
                plt.text(x.iloc[i], y.iloc[i], player, fontsize=5, ha='right', va='bottom')

            plt.grid(True)
            plt.xlabel("Receptions")
            plt.ylabel("Receiving Yds")
            plt.title("Top 20 WRs: Receptions vs Receiving Yards")
            plt.legend()
            plt.show()

        elif pos == "3":

            x = top_qb["PassingAttempts"]
            y = top_qb["PassingYards"]
            plt.scatter(x, y, color="red")
            m, b = np.polyfit(x, y, 1)
            plt.plot(x, m*x+b, color="blue", linestyle="--", label="Best Fit")

            for i, player in enumerate(top_qb.index): 
                plt.text(x.iloc[i], y.iloc[i], player, fontsize=5, ha='right', va='bottom')

            plt.grid(True)
            plt.xlabel("Pass Att")
            plt.ylabel("Passing Yds")
            plt.title("Top 20 QBs: Pass Attempts vs Passing Yards")
            plt.legend()
            plt.show()

        else:
            print("\nInvalid Input\n")

    elif action == "5":
        print("\nExiting Program...")
        break

    else:
        print("\nInvalid Input, try again\n")
        continue




            
