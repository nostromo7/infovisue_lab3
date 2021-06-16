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

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    return render_template("exploratory.html", data=json.dumps(stat_map))

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

    return render_template("predictors.html", data=json.dumps(stat_map))

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

    stat_data = pd.read_csv(loc + 'final_dataset.csv')

    stat_map = stat_data.to_dict(orient = 'index')

    print(str(stat_map))

    return render_template("outcome_exploration.html", data=json.dumps(stat_map))



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
    app.run()
