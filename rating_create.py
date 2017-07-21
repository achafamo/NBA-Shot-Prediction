import csv
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
#import pydotplus

def player_rating(def_off,with_percentile=False):
    player_dict = {}
    pts_list_2 = []
    pts_list_3 = []
    n =0
    with open('shot_logs.csv','rb') as f:
        #print "here"
        reader = csv.DictReader(f)
        #writer = csv.DictWriter(f2,['TailNum','ActualDepTime','ActualArrTime','Origin','Dest'])
        #writer.writeheader()
        #print "printing reader" , reader
        for row in reader:
            #print "printing rows"
            #print row
            game_id = int(row['GAME_ID'])
            if game_id <= 21400615:
                if(def_off == "offense"):
                    pid = row['player_id']
                elif(def_off == "defense"):
                    pid = row["CLOSEST_DEFENDER_PLAYER_ID"]
                pts = row['PTS_TYPE']
                ptresult = row['SHOT_RESULT']
                if  pid in player_dict:
                    player_dict[pid][pts+ptresult] +=1
                else:
                    player_dict[pid] = new_dict()
                    player_dict[pid][pts+ptresult] =1
        #print player_dict
    result_dict = {}
    for player in player_dict:
        #print player
        temp_dict = player_dict[player]
        made3 = temp_dict['3made']
        made2 = temp_dict['2made']
        miss3 = temp_dict['3missed']
        miss2 = temp_dict['2missed']

        if (made2 == 0 and miss2 == 0):
            if (def_off == "offense"):
                percent2pts =0
            elif (def_off == "defense"):
                percent2pts = 0.5 #arbitrary number chosen
        else:
            if (def_off == "offense"):
                percent2pts = float(made2)/(made2+miss2)
            elif (def_off == "defense"):
                percent2pts =  float(miss2)/(made2+miss2)

        if (made3 == 0 and miss3 == 0):
            if (def_off == "offense"):
                percent3pts = 0
            elif (def_off == "defense"):
                percent3pts = 0.65 #arbitrary number chosen
        else:
            if (def_off == "offense"):
                percent3pts = float(made3)/(made3+miss3)
            elif (def_off == "defense"):
                percent3pts = float(miss3) / (made3 + miss3)
        pts_list_2.append(percent2pts)
        pts_list_3.append(percent3pts)
        n+=1
        result_dict[player] = (  percent2pts,percent3pts )

    #print pts_list_2
    #print pts_list_3
    if not with_percentile:
        return result_dict
    else:
        player_ratings = {}
        p2_25,p2_50,p2_75 = find_percentile(pts_list_2,n)
        p3_25,p3_50,p3_75 = find_percentile(pts_list_3,n)


        #print p2_25,p2_50,p2_75
        #print p3_25,p3_50,p3_75
        for player in result_dict:
            p2, p3 = result_dict[player]
            r2 = rate(p2, (p2_25,p2_50,p2_75))
            r3 = rate(p3, (p3_25,p3_50,p3_75))
            player_ratings[player] = (r2,r3)
        # print player_ratings
        return player_ratings


def rate10(r,tenths_tuples):
    distance10, distance20, distance30, distance40, distance50, distance60, distance70, distance80, distance90 = tenths_tuples
    cat1 = '0' + '-' + str("%.3f" % distance10)
    cat2 = str("%.3f" % distance10) + '-' + str("%.3f" % distance20)
    cat3 = str("%.3f" % distance20) + '-' + str("%.3f" % distance10)
    cat4 = str("%.3f" % distance30) + '-' + str("%.3f" % distance10)
    cat5 = str("%.3f" % distance40) + '-' + str("%.3f" % distance10)
    cat6 = str("%.3f" % distance50) + '-' + str("%.3f" % distance10)
    cat7 = str("%.3f" % distance60) + '-' + str("%.3f" % distance10)
    cat8 = str("%.3f" % distance70) + '-' + str("%.3f" % distance10)
    cat9 = str("%.3f" % distance80) + '-' + str("%.3f" % distance10)
    cat10 = str("%.3f" % distance90) + '-' + 'max'
    if r<=distance10:
        rate = cat1
    elif r <= distance20:
        rate = cat2
    elif r <= distance30:
        rate = cat3
    elif r <= distance40:
        rate = cat4
    elif r <= distance50:
        rate = cat5
    elif r <= distance60:
        rate = cat6
    elif r <= distance70:
        rate = cat7
    elif r <= distance80:
        rate = cat8
    elif r <= distance90:
        rate = cat9
    else:
        rate = cat10
    return rate


def rate(r,percentile_tuple):
    p25,p50,p75 = percentile_tuple
    cat1 = '0' + '-' + str("%.3f" %p25)
    cat2 = str("%.3f" %p25) + '-' + str("%.3f" %p50)
    cat3 = str("%.3f" %p50) + '-' + str("%.3f" %p75)
    cat4 = str("%.3f" %p75) + '-' + 'max'
    if r <= p25:
        rate = cat1
    elif r <= p50:
        rate = cat2
    elif r <= p75:
        rate = cat3
    else:
        rate = cat4
    return rate

def new_dict():
    new_dict = {}
    for field in ['2made', '2missed','3made','3missed']:
        new_dict[field] = 0;
    return new_dict



def shot_vs_period():
    player_dict = [ {'made':0, 'missed':0}, {'made':0, 'missed':0},{'made':0, 'missed':0},
                    {'made':0, 'missed':0},{'made':0, 'missed':0},{'made':0, 'missed':0},
                    {'made':0, 'missed':0}]
    with open('shot_logs.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            period = int(row['PERIOD'])
            pts = row['PTS_TYPE']
            ptresult = row['SHOT_RESULT']
            player_dict[period -1 ][ptresult] +=1
        return player_dict

def shot_vs_pts():
    player_dict = [{'made': 0, 'missed': 0}, {'made': 0, 'missed': 0}]
    with open('shot_logs.csv', 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            period = int(row['PERIOD'])
            pts = int(row['PTS_TYPE'])
            ptresult = row['SHOT_RESULT']
            #print period, ptresult
            player_dict[pts - 2][ptresult] += 1
        return player_dict
#111

def shot_vs_distance():
    player_dict = iterate_count('shot_logs.csv', 'SHOT_DIST', 4)
    return player_dict


def iterate_perc(filename, column_name):
    player_dict = []
    n = 0
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            distance = float(row[column_name])
            player_dict.append(distance)
            n += 1

    distance25, distance50, distance75 = find_percentile(player_dict, n)
    return distance25, distance50, distance75

def find_percentile(player_list, n):
    player_list.sort()
    distance25, distance50, distance75 = player_list[n/4], player_list[n/2], player_list[3*(n/4)]
    return distance25, distance50, distance75

def find_tenths(player_list,n):
    player_list.sort()
    distance10,distance20,distance30,distance40,distance50,distance60,distance70,distance80,distance90 = player_list[n/10],player_list[2*n/10],player_list[3*n/10],player_list[4*n/10],player_list[5*n/10],player_list[6*n/10],player_list[7*n/10],player_list[8*n/10],player_list[9*n/10]
    return distance10,distance20,distance30,distance40,distance50,distance60,distance70,distance80,distance90

def iterate_count(filename, column_name, n):
    distance25, distance50,distance75 = iterate_perc(filename,column_name)
    player_dict = new_list(n)
    #print distance25,distance50,distance75
    with open(filename, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            distance = float(row[column_name])
            #pts = int(row['PTS_TYPE'])
            ptresult = row['SHOT_RESULT']
            #print period, ptresult
            if distance <= distance25:
                player_dict[0][ptresult]+=1
            elif distance <= distance50:
                player_dict[1][ptresult]+=1
            elif distance <= distance75:
                player_dict[2][ptresult]+=1
            else:
                player_dict[3][ptresult]+=1

    return player_dict

def new_list(n):
    new_list = []
    for i in range(n):
        new_list.append({'made': 0, 'missed': 0})
    return new_list

def shot_vs_def_dist():
    player_dict = iterate_count('shot_logs.csv', 'CLOSE_DEF_DIST',4)
    return player_dict

def create_new_file(all_features= False):
    player_offensive_rating = player_rating("offense",True)
    player_defensive_rating = player_rating("defense",True)

    #print player_defensive_rating
    #print player_offensive_rating
    shot_clock_list, touch_time_list, shot_dist_list, close_def_dist_list , dribble_list, n = pre_process('shot_logs.csv')

    #finalize data
    shot_clock_Thresholds, touch_time_Thresholds, shot_dist_Thresholds, close_def_dist_Thresholds, dribble_Thresholds = finalize_data(shot_clock_list,touch_time_list,shot_dist_list,close_def_dist_list, dribble_list, n)
    #print shot_clock_Thresholds
    #print touch_time_Thresholds
    #print shot_dist_Thresholds
    #print close_def_dist_Thresholds
    #(7.5, 12.0, 16.4)
    #(0.9, 1.6, 3.7)
    #(4.7, 13.7, 22.5)
    #(2.3, 3.7, 5.3)

    with open("shot_logs.csv", 'r') as f, open("shots.csv", 'w') as f1:
        reader = csv.DictReader(f)
        if not all_features:
            writer = csv.DictWriter(f1, ['SHOT_DIST', 'PTS_TYPE', 'COSE_DEF_DIST', 'player_shot_pct',
                                     'defender_defensive_pct', 'SHOT_RESULT'])
        else:
            writer = csv.DictWriter(f1, ["LOCATION", "PERIOD", "SHOT_CLOCK", 'DRIBBLES', 'TOUCH_TIME',
                                         'SHOT_DIST', 'PTS_TYPE', 'COSE_DEF_DIST',
                                         'player_shot_pct',
                                         'defender_defensive_pct', 'SHOT_RESULT'])
        writer.writeheader()

        # pre-processing
        for row in reader:
            pid = row['player_id']
            did = row['CLOSEST_DEFENDER_PLAYER_ID']
            if row['SHOT_CLOCK'] == '':
                shot_clock = 0.0
            else:
                shot_clock = float(row['SHOT_CLOCK'])
            touch_time = float(row['TOUCH_TIME'])
            shot_dist = float(row['SHOT_DIST'])
            close_def_dist = float(row['CLOSE_DEF_DIST'])
            dribble_num = int(row['DRIBBLES'])

            shot_clock_rate = rate(shot_clock,shot_clock_Thresholds)
            touch_time_rate = rate(touch_time,touch_time_Thresholds)
            shot_dist_rate = rate10(shot_dist,shot_dist_Thresholds)
            close_def_rate = rate(close_def_dist,close_def_dist_Thresholds)
            dribble_rate = rate(dribble_num,dribble_Thresholds)


            if(row['PTS_TYPE']==str(2)):
                player_shot_pct,y = player_offensive_rating[pid]
                #defender_defensive_pct,y = player_defensive_rating[did]
                if pid in player_defensive_rating:
                    # print pid,player_defensive_rating[pid]
                    defender_defensive_pct, y = player_defensive_rating[pid]
                else:
                    defender_defensive_pct = 0.5
            else:
                #y,player_shot_pct = player_offensive_rating[pid]
                #y,defender_defensive_pct = player_defensive_rating[did]
                if pid in player_defensive_rating:
                    #print pid,player_defensive_rating[pid]
                    y, defender_defensive_pct = player_defensive_rating[pid]
                else:
                    defender_defensive_pct = 0.65
                y, player_shot_pct = player_offensive_rating[pid]
            if not all_features:
                writer.writerow({'SHOT_DIST':shot_dist_rate,'PTS_TYPE':row["PTS_TYPE"],'COSE_DEF_DIST':close_def_rate,'player_shot_pct':player_shot_pct,'defender_defensive_pct':defender_defensive_pct,'SHOT_RESULT':row["SHOT_RESULT"]})
            else:
                writer.writerow({'LOCATION': row['LOCATION'], "PERIOD": row["PERIOD"], "SHOT_CLOCK": shot_clock_rate,'DRIBBLES': row["DRIBBLES"], 'TOUCH_TIME': touch_time_rate, 'SHOT_DIST': shot_dist_rate,'PTS_TYPE': row["PTS_TYPE"], 'COSE_DEF_DIST': close_def_rate,'player_shot_pct': player_shot_pct, 'defender_defensive_pct': defender_defensive_pct,'SHOT_RESULT': row["SHOT_RESULT"]})

def finalize_data(shot_clock_list,touch_time_list,shot_dist_list,close_def_dist_list, dribble_list, n):
    shot_clock_list.sort()
    touch_time_list.sort()
    shot_dist_list.sort()
    close_def_dist_list.sort()
    dribble_list.sort()

    shot_clock_Thresholds = (shot_clock_list[n / 4], shot_clock_list[n / 2], shot_clock_list[3 * n / 4])
    touch_time_Thresholds = (touch_time_list[n / 4], touch_time_list[n / 2], touch_time_list[3 * n / 4])
    shot_dist_Thresholds = (shot_dist_list[n/10],shot_dist_list[2*n/10],shot_dist_list[3*n/10],shot_dist_list[4*n/10],shot_dist_list[5*n/10],shot_dist_list[6*n/10],shot_dist_list[7*n/10],shot_dist_list[8*n/10],shot_dist_list[9*n/10])
    close_def_dist_Thresholds = (close_def_dist_list[n / 4], close_def_dist_list[n / 2], close_def_dist_list[3 * n / 4])
    dribble_Thresholds = (dribble_list[n / 4], dribble_list[n / 2], dribble_list[3 * n / 4])
    #print "Printing thresholds"
    # print shot_dist_Thresholds

    return shot_clock_Thresholds,touch_time_Thresholds,shot_dist_Thresholds,close_def_dist_Thresholds, dribble_Thresholds

def pre_process(filename):
    game_clock_list = []
    shot_clock_list = []
    touch_time_list = []
    shot_dist_list = []
    close_def_dist_list = []
    dribble_list = []
    n = 0

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)

        # pre-processing
        for row in reader:
            #game_clock = float(row['GAME_CLOCK'])
            #print row['SHOT_CLOCK']
            if row['SHOT_CLOCK'] == '':
                shot_clock = 0.0
            else:
                shot_clock = float(row['SHOT_CLOCK'])
            touch_time = float(row['TOUCH_TIME'])
            shot_dist = float(row['SHOT_DIST'])
            close_def_dist = float(row['CLOSE_DEF_DIST'])
            dribble_num = int(row['DRIBBLES'])

            #game_clock_list.append(game_clock)
            shot_clock_list.append(shot_clock)
            touch_time_list.append(touch_time)
            shot_dist_list.append(shot_dist)
            close_def_dist_list.append(close_def_dist)
            dribble_list.append(dribble_num)
            n+=1

    return shot_clock_list, touch_time_list, shot_dist_list, close_def_dist_list, dribble_list, n


#create_new_file()
#2.3 3.7 5.3
#player_rating("defense")
#[{'made': 15288, 'missed': 18353}, {'made': 15190, 'missed': 16913}, {'made': 13807, 'missed': 17708}, {'made': 13620, 'missed': 17190}]
#4.7 13.7 22.5
#[{'made': 20138, 'missed': 12179}, {'made': 13793, 'missed': 18096}, {'made': 12875, 'missed': 19017}, {'made': 11099, 'missed': 20872}]
def load_data():
    player_offensive_rating = player_rating("offense",False)
    player_defensive_rating = player_rating("defense",False)
    #print player_defensive_rating
    #print player_offensive_rating
    X_train = []
    Y_train = []
    X_test = []
    Y_test = []
    with open("shot_logs.csv", 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            new_instance  = []
            pid = row['player_id']
            did = row['CLOSEST_DEFENDER_PLAYER_ID']
            gid = int(row['GAME_ID'])
            #new_instance.append(row['LOCATION'])
            new_instance.append(int(row['PERIOD']))
            if row['SHOT_CLOCK'] == '':
                new_instance.append(0)
            else:
                new_instance.append(float(row['SHOT_CLOCK']))
            new_instance.append(int(row['DRIBBLES']))
            new_instance.append(float(row['TOUCH_TIME']))
            new_instance.append(float(row['SHOT_DIST']))
            new_instance.append(int(row['PTS_TYPE']))
            new_instance.append(float(row['CLOSE_DEF_DIST']))

            if (row['PTS_TYPE'] == str(2)):
                player_shot_pct, y = player_offensive_rating[pid]
                defender_defensive_pct, y = player_defensive_rating[pid]
            else:
                if pid in player_defensive_rating:
                    #print pid,player_defensive_rating[pid]
                    y, defender_defensive_pct = player_defensive_rating[pid]
                else:
                    defender_defensive_pct = 0.65
                y, player_shot_pct = player_offensive_rating[pid]

            new_instance.append(player_shot_pct)
            new_instance.append(defender_defensive_pct)

            if gid <= 21400615:
                X_train.append(new_instance)
                Y_train.append(row['SHOT_RESULT'])
            else:
                X_test.append(new_instance)
                Y_test.append(row['SHOT_RESULT'])

    return X_train, Y_train, X_test, Y_test

def classify(use_probabilty=True):

    dtclassifier1 = DecisionTreeClassifier(max_depth=2)
    dtclassifier2 = DecisionTreeClassifier (criterion=  "entropy", max_depth=7)

    X_train, Y_train, X_test, Y_test = load_data()
    dtclassifier2.fit(X_train ,Y_train)

    # predict made or miss
    if not use_probabilty:
        predictions = dtclassifier2.predict(X_test)

    #print predictions
    #return predictions

    #ploting, requires graphviz and pydotplus
        '''dot_data = tree.export_graphviz(dtclassifier2, out_file=None, feature_names =
        ['Period','Shot Clock', 'Dribbles', 'Touch Time','Shot Distance', 'PTS Type', 'Defense Distance', 'Player Shot','Defender'])
        graph = pydotplus.graph_from_dot_data(dot_data)
        graph.write_pdf("iris.pdf")'''


        wrongPredictions = 0
        for index, val in enumerate(predictions):
            if Y_test[index] != val:
                wrongPredictions = wrongPredictions + 1
        print ("Correctly predicted %s out of %s instances."
               % ((len(Y_test) - wrongPredictions), len(Y_test))), "The accuracy is " + str(float(len(Y_test) - wrongPredictions)/len(Y_test)) + "."

        predictions = dtclassifier2.predict(X_train)
        wrongPredictions = 0
        for index, val in enumerate(predictions):
            if Y_train[index] != val:
                wrongPredictions = wrongPredictions + 1
        print ("Correctly predicted %s out of %s instances."
               % ((len(Y_train) - wrongPredictions), len(Y_train))), "The accuracy is " + str(
            float(len(Y_train) - wrongPredictions) / len(Y_train)) + "."
    else:
    #predict probability, uncomment the next lane
        predictions = dtclassifier2.predict_proba(X_test)

    return predictions


create_new_file(True)
classify(False)