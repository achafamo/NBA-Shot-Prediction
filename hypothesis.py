from __future__ import division
import csv
import matplotlib.pyplot as plt
import numpy as np
from collections import *
def court_advantage():
    tallies = defaultdict(lambda :defaultdict(int))
    with open('shot_logs.csv','rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shot_result= row["SHOT_RESULT"]
            loc = row["LOCATION"]
            dist = float(row["SHOT_DIST"])
            tallies[loc][shot_result]+=1
            tallies[loc]["TOTAL_DIST"]+=dist
            tallies[loc]["COUNT"]+=1
        for lc in {"A", "H"}:
            tallies[lc]["AVERAGE_DISTANCE"] = tallies[lc]["TOTAL_DIST"]/tallies[lc]["COUNT"]
        print "Percentage of shots made by players at home " + str(tallies["H"]["made"]/(tallies["H"]["missed"] + tallies["H"]["made"]))
        print "Percentage of shots made by players away " + str(tallies["A"]["made"] / (tallies["A"]["missed"] + tallies["A"]["made"]))

        print "The total number of shots attempted by players at home" + str((tallies["H"]["missed"] + tallies["H"]["made"]))
        print "The total number of shots attempted by player away" + str((tallies["A"]["missed"] + tallies["A"]["made"]))

        
        print "The average distance of shots attempted by players at home" + str(tallies["H"]["AVERAGE_DISTANCE"])
        print "The average distance of shots attempted by players at away" + str(tallies["A"]["AVERAGE_DISTANCE"])
        #Add random test to find p-value and make it for individual players as opposed to teams
    return
def shot_distance():
    '''
    show how distance is positively correlated to percentage of shots made
    '''
    dist_result = defaultdict(lambda: defaultdict(int))
    with open('shot_logs.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            shot_result = row["SHOT_RESULT"]
            dist = float(row["SHOT_DIST"])
            #print dist
            dist_group = group_dist(dist)

            dist_result[dist_group][shot_result]+=1
        f_g_percentage = []

        for dist_g in sorted(dist_result.keys()):
            dist_result[dist_g]["percentage"] = dist_result[dist_group]["made"]/(dist_result[dist_group]["made"]+
                                                                                 dist_result[dist_group]["missed"])
            f_g_percentage.append(dist_result[dist_g]["percentage"])
        print f_g_percentage
        plt.scatter(sorted(dist_result.keys()), f_g_percentage)
        plt.show()
    return

def group_dist(dist):
    for i in numpy.linspace(0, 30,0.1):
        if dist>i and dist <i+0.1:
            print i
            return i
    return 30
def shot_clock():
    '''
    Test effect of remaining time on shot clock on accuracy of shos
    '''
    pass
def assign_label(xlabel, ylabel, title):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def hist_plot(x, xlabel, ylabel, title, color ='b'):
    plt.hist(x, 30, color=color)
    assign_label(xlabel, ylabel, title)


def bar_plot(x, y, xlabel, ylabel, title, stacked):
    plt.bar(x, y, stacked=stacked)
    assign_label(xlabel, ylabel, title)
    
def clock_fpg(raw):
    shot_n_clock = pd.concat([raw.SHOT_RESULT, raw.SHOT_CLOCK], axis=1)
    shot_n_clock["IS_SHOT_MADE"] = (shot_n_clock.SHOT_RESULT == 'made')
    shot_n_clock.SHOT_CLOCK.describe()
    clock_tick = list(range(0, 25))
    trueList = []
    falseList = []
    for x in clock_tick:
        temp = shot_n_clock[(shot_n_clock.SHOT_CLOCK <= x) & (shot_n_clock.SHOT_CLOCK > x - 1)].groupby("IS_SHOT_MADE").SHOT_RESULT.count()
        trueList.append(temp[1])
        falseList.append(temp[0])

        # Building output dataframe, calculating % column
    final = pd.DataFrame({"sec_left": clock_tick, "True": trueList, "False": falseList})
    final['FG%'] = np.round(final['True'] / (final['True'] + final['False']) * 100, 2)
    return final

def court_adv(raw):
    shot_n_court = pd.concat([raw.SHOT_RESULT, raw.LOCATION], axis=1)
    shot_n_court["MADE"] = (shot_n_court.SHOT_RESULT == 'made')
    home_stats = shot_n_court[shot_n_court.LOCATION == 'H'].groupby("MADE").SHOT_RESULT.count()
    away_stats = shot_n_court[shot_n_court.LOCATION == 'A'].groupby("MADE").SHOT_RESULT.count()
    totals = [0] * 2  # total number of shots attempted for H an A teams
    totals[0] = float(sum(home_stats))
    totals[1] = float(sum(away_stats))
    shots_missed = np.append(home_stats[0] / totals[0], away_stats[0] / totals[1])
    shots_missed = [x * 100 for x in shots_missed]
    shots_made = [100 - missed_perc for missed_perc in shots_missed]
    return shots_made, shots_missed

def plot_court_advantage(made_shots, missed_shots):
    ind = [0.5, 1.5]
    width = 0.15
    fig, ax = plt.subplots()
    made_bar = ax.bar(ind, made_shots, width, color='g')
    missed_bar = ax.bar(ind, missed_shots, width, color='r', bottom = made_shots)

    ax.set_ylabel('Field Goal Percentage ')
    ax.set_title('Home Court Advantage')
    ax.set_xticks(ind)
    ax.set_yticks(np.arange(0,100,10))
    ax.set_xticklabels(('Home', 'Away'))
    ax.legend((made_bar[0], missed_bar[0]), ('% Shots Made ', '% Shots Missed '))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width *1.2, box.height])
    ax.legend(loc='center left')
    autolabel(ax, made_bar)
    return


def autolabel(ax,bars):

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 0.90*height,
                '%f' % float(height),
                ha='center', va='bottom')



