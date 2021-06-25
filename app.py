from flask import Flask, render_template
import json
import pandas as pd
import pprint as pp
import numpy as np 
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt 
import matplotlib
import glob
import os
import re

app = Flask(__name__)

# ensure that we can reload when we change the HTML / JS for debugging
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def data():

    seasons_folder = 'data/PremierLeague10Seasons/'

    #TODO: How it should work without absolute paths:
    #player_data = pd.read_csv(loc + r'player data/players_21.csv')

    player_data = pd.read_csv('data/FIFA_player_data/players_21.csv')
    standings_data = pd.read_csv('data/PremierLeague10Seasons/EPLStandings.csv')

    # Get all filenames of seasons
    all_season_files = list(glob.iglob(os.path.join(seasons_folder, 'season*.csv')))
    seasons_map = {
        "season-0910_csv.csv": "2009/10",
        "season-1011_csv.csv": "2010/11",
        "season-1112_csv.csv": "2011/12",
        "season-1213_csv.csv": "2012/13",
        "season-1314_csv.csv": "2013/14",
        "season-1415_csv.csv": "2014/15",
        "season-1516_csv.csv": "2015/16",
        "season-1617_csv.csv": "2016/17",
        "season-1718_csv.csv": "2017/18",
        "season-1819_csv.csv": "2018/19",
        "season-1920_csv.csv": "2019/20",
        "season-2021_csv.csv": "2020/21"
    }
    FTR_map = {
        'H': 1,
        'D': 0,
        'A': -1
    }
    # concat single seasons with additional attribute 'Season'
    seasons_data = pd.DataFrame()
    for file in all_season_files:
        this_season = pd.read_csv(file, parse_dates=True)
        this_season['Season'] = seasons_map[os.path.basename(file)]
        this_season['FTR'] = this_season['FTR'].map(FTR_map)
        seasons_data = pd.concat([seasons_data, this_season], ignore_index=True)

    # just take players which play in english clubs
    english_teams = standings_data['Team']
    player_data = player_data[player_data['club_name'].isin(english_teams)][['sofifa_id', 'short_name', 'nationality', 'club_name', 'age', 'height_cm', 'weight_kg', 'player_positions', 'overall', 'shooting', 'passing', 'dribbling', 'defending', 'team_jersey_number']]
    player_data = player_data.replace('England', 'United Kingdom')


    player_map = player_data.to_json(orient='index')
    standings_map = standings_data.to_json(orient='index')
    seasons_map = seasons_data.to_json(orient='index')
    # return the index file and the data
    return render_template("index.html", seasons=json.dumps(seasons_map), player=json.dumps(player_map), standings=json.dumps(standings_map))


@app.route('/explore')
def explore_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    graph_leaguepos_goals_scor = {}
    graph_leaguepos_goals_conc = {}
    graph_league_diff_goal_diff = {}
    graph_formdiff_goals_diff = {}
    graph_form_diff_pts_diff = {}
    graph_home_goal_diff_goal_scored = {}
    graph_away_goal_diff_goal_scored = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict()

    data1 = {'xa' : stat_map['HomeTeamLP'], 'ya' : stat_map['FTHG']}
    data2 = {'xa' : stat_map['HomeTeamLP'], 'ya' : stat_map['FTAG']}
    data3 = {'xa' : stat_map['DiffLP'], 'ya' : stat_map['DiffFormPts']}
    data4 = {'xa' : stat_map['HTFormPts'], 'ya' : stat_map['FTHG']}
    data5 = {'xa' : stat_map['DiffFormPts'], 'ya' : stat_map['DiffPts']}
    data6 = {'xa' : stat_map['HTGD'], 'ya' : stat_map['FTHG']}


    return render_template("exploratory.html", data1=json.dumps(data1),data2=json.dumps(data2), data3=json.dumps(data3), data4=json.dumps(data4), data5=json.dumps(data5), data6=json.dumps(data6))

@app.route('/additional')
def additional_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    return render_template("additional_data.html", data=json.dumps(stat_map))

@app.route('/heatmap')
def heatmap_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    return render_template("heatmaps.html", data=json.dumps(stat_map))

@app.route('/predictor')
def predictor_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    return render_template("predictor.html", data=json.dumps(stat_map))

@app.route('/regular')
def regular_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    return render_template("regular_exploration.html", data=json.dumps(stat_map))

@app.route('/outcome')
def outcome_data():

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    graph_map_form = {}
    graph_map_3streak = {}
    graph_map_5_streak = {}
    graph_map_form_goals_scored = {}
    graph_map_form_goals_conceded = {} 


    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict()


    data8 = {'xa' : stat_map['HTFormPts'], 'ya' : stat_map['FTR']}
    data9 = {'xa' : stat_map['HTWinStreak3'], 'ya' : stat_map['FTR']}
    data10 = {'xa' : stat_map['HTWinStreak5'], 'ya' : stat_map['FTR']}
    data11 = {'xa' : stat_map['HTFormPts'], 'ya' : stat_map['FTHG']}
    data12 = {'xa' : stat_map['HTFormPts'], 'ya' : stat_map['FTAG']}

    #createVisualisations(data11)

    return render_template("outcome_exploration.html", data8=json.dumps(data8),data9=json.dumps(data9), data10=json.dumps(data10), data11=json.dumps(data11), data12=json.dumps(data12))


def createVisualisations(data):

    # definitions for the axes
    left, width = 0.1, 0.75
    bottom, height = 0.1, 0.75
    spacing = 0.005


    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_axes(rect_scatter)
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    # LOAD THE DATA INTO THE PLOT
    x_axis_data =  list(data['xa'].values())
    y_axis_data = list(data['ya'].values())

    #print(x_axis_data)
    #print(y_axis_data)

    ax.set_xlabel('Home Time Points')
    ax.set_ylabel('FTR')

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x_axis_data, y_axis_data)

    # now determine nice limits by hand:
    #binwidth = 0.25
    #xmax = np.max(x_axis_data)
    #xmin = np.min(x_axis_data)
    #ymax = np.max(y_axis_data)
    #ymin = np.min(y_axis_data)

    #x_bins = np.arange(xmin, xmax  + binwidth, binwidth)
    #y_bins = np.arange(ymin, ymax + binwidth, binwidth)

    #ax_histx.hist(x_axis_data, bins= x_bins)
    #ax_histy.hist(y_axis_data, bins= y_bins, orientation='horizontal')

    #plt.show()

    #plt.savefig("HTPvsFTR.png")

    return 


def createPCA(data):

    countries = data.pop('Country')
    codes = data.pop('LOCATION')

    idmap = []
    indicators = []

    for i in range(0, len(countries)):
        idmap.append([i, countries[i], codes[i]])

    for i in range(0, len(data.columns)):
        indicators.append([i, data.columns[i]])
    #print(data.head)

    scaled_data = preprocessing.scale(data)
 
    matplotlib.pyplot.switch_backend('Agg') 

    pca = PCA()
    pca.fit(scaled_data) # calcualtes loading scores
    pca_data = pca.transform(scaled_data) # generates coordinates for a PCA graph

    ### calucates the percentage of variation each principal component accounts for
    per_var = np.round(pca.explained_variance_ratio_* 100, decimals=1)


    labels = ['PC' + str(x) for x in range(1, len(per_var)+1)]

    #plt.bar(x=range(1,len(per_var)+1), height=per_var, tick_label=labels)
    #plt.ylabel('Percentage of Explained Variance')
    #plt.xlabel('Principal Component')
    #plt.title('Scree Plot')
    #plt.plot()
    #plt.savefig('static/data/plot.png')

    pca_df = pd.DataFrame(pca_data, columns=labels)

    loadings_df = pd.DataFrame(pca.components_.T, columns=labels)

    #pp.pprint(idmap)
    #pp.pprint(indicators)

    #print(pca_df.shape)
    #pp.pprint(pca_df)
    #pp.pprint(loadings_df)

    return (pca_df, loadings_df, idmap, indicators)

if __name__ == '__main__':

    loc = 'data/PremierLeague10Seasons/'

    stat_map = {}

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict()

    
    #data = {'xa' : stat_map['HomeTeamLP'], 'ya' : stat_map['FTHG']}
    #data = {'xa' : stat_map['HomeTeamLP'], 'ya' : stat_map['FTAG']}
    #data = {'xa' : stat_map['DiffLP'], 'ya' : stat_map['DiffFormPts']}
    #data = {'xa' : stat_map['HTFormPts'], 'ya' : stat_map['FTHG']}
    #data = {'xa' : stat_map['DiffFormPts'], 'ya' : stat_map['DiffPts']}
    data = {'xa' : stat_map['HTGD'], 'ya' : stat_map['FTHG']}

    # definitions for the axes
    left, width = 0.1, 0.75
    bottom, height = 0.1, 0.75
    spacing = 0.005


    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom + height + spacing, width, 0.2]
    rect_histy = [left + width + spacing, bottom, 0.2, height]

    # start with a square Figure
    fig = plt.figure(figsize=(8, 8))

    ax = fig.add_axes(rect_scatter)
    ax_histx = fig.add_axes(rect_histx, sharex=ax)
    ax_histy = fig.add_axes(rect_histy, sharey=ax)

    # LOAD THE DATA INTO THE PLOT
    x_axis_data =  list(data['xa'].values())
    y_axis_data = list(data['ya'].values())

    #print(x_axis_data)
    #print(y_axis_data)

    ax.set_xlabel('HTGD')
    ax.set_ylabel('FTGH')

    ax_histx.tick_params(axis="x", labelbottom=False)
    ax_histy.tick_params(axis="y", labelleft=False)

    # the scatter plot:
    ax.scatter(x_axis_data, y_axis_data)

    # now determine nice limits by hand:
    binwidth = 0.25
    xmax = np.max(x_axis_data)
    xmin = np.min(x_axis_data)
    ymax = np.max(y_axis_data)
    ymin = np.min(y_axis_data)

    x_bins = np.arange(xmin, xmax  + binwidth, binwidth)
    y_bins = np.arange(ymin, ymax + binwidth, binwidth)

    ax_histx.hist(x_axis_data, bins= x_bins)
    ax_histy.hist(y_axis_data, bins= y_bins, orientation='horizontal')

    plt.show()

    plt.savefig("static/data/HTPvsFTR.png")


    app.run()
