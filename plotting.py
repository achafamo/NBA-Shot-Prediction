import matplotlib.pyplot as plt
import numpy as np
import rating_create
def make_bar_graph(desired_info):


    if(desired_info == "shot_vs_def_dist"):
        vis_data = rating_create.shot_vs_def_dist()
        title = 'Shot outcomes against defenders in different distance ranges'
        y_label = 'Number of shots'
        x_label = 'Defender distance ranges'
        xtick_labels = ('25thp', '50thp', '75thp', 'higher')
    elif (desired_info == "shot_vs_distance"):
        vis_data = rating_create.shot_vs_distance()
        title = 'Shots outcomes from different distance ranges'
        y_label = 'Number of shots'
        x_label = 'Shot distance ranges'
        xtick_labels = ('25thp', '50thp', '75thp', 'higher')
    elif (desired_info == "shot_vs_period"):
        vis_data = rating_create.shot_vs_period()
        title = 'Shot outcomes in different quarters'
        y_label = 'Number of shots'
        x_label = 'Quarters'
        xtick_labels = ('1st','2nd','3rd','4th','OT1','OT2','OT3')
    elif (desired_info == "shot_vs_pts"):
        vis_data = rating_create.shot_vs_distance()
        title = 'Outcomes for all 2 and 3 point shots'
        y_label = 'Number of shots'
        x_label = 'Type of Shot'
        xtick_labels = ('2pts','3pts')

    made_shots = []
    missed_shots = []
    for data in vis_data:
        made_shots.append(data['made'])
        missed_shots.append(data['missed'])

    N = len(xtick_labels)
    width = 0.35
    ind = np.arange(N)
    fig, ax = plt.subplots()
    made_bar = ax.bar(ind, made_shots, width, color = 'y')
    missed_bar = ax.bar(ind + width,missed_shots,width,color = 'g')

    ax.set_ylabel (y_label)
    ax.set_xlabel (x_label)
    ax.set_title (title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(xtick_labels)
    ax.legend((made_bar[0],missed_bar[0]),('Made Shots','Missed Shots'))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.8, box.height*1.8])
    ax.legend(loc='center left',bbox_to_anchor=(1, 0.5))
    autolabel(made_bar,ax)
    autolabel(missed_bar,ax)
    plt.show()

def autolabel(bars,ax):
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., 1.01*height,
                '%d' % int(height),
                ha='center', va='bottom')

def plot_two_vs_three():
    vis4_data = rating_create.shot_vs_pts()
    made_shots = []
    missed_shots = []
    for data in vis4_data:
        made_shots.append(data['made'])
        missed_shots.append(data['missed'])
    N = 2
    width = 0.35
    ind = np.arange(N)
    fig, ax = plt.subplots()
    made_bar = ax.bar(ind, made_shots, width, color='yellow')
    missed_bar = ax.bar(ind + width, missed_shots, width, color='green')

    ax.set_ylabel('Number of shots')
    ax.set_xlabel('Type of Shot')
    ax.set_title('Numbe of made/missed 2 and 3 pointers')
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(('2pts', '3pts'))
    ax.legend((made_bar[0], missed_bar[0]), ('Made Shots', 'Missed Shots'))
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 1.8, box.height * 1.8])
    autolabel(made_bar, ax)
    autolabel(missed_bar, ax)
    plt.show()