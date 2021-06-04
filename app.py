from flask import Flask, render_template
import json
import pandas as pd
import pprint as pp
import numpy as np 
from sklearn.decomposition import PCA
from sklearn import preprocessing
import matplotlib.pyplot as plt 
import matplotlib 

app = Flask(__name__)

# ensure that we can reload when we change the HTML / JS for debugging
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def data():
    loc = r'./static/data/'

    map_data = pd.read_csv(loc + r'oecdTable.csv')

    player_data = pd.read_csv(loc + r'player data/players_21.csv')

    season_21_data = pd.read_csv(loc + r'English Premier League (football) 10 Seasons/season-2021_csv.csv')

    player_map = player_data.to_dict()
    season_21_map = season_21_data.to_dict()

    # return the index file and the data
    return render_template("index.html", player=json.dumps(player_map), season_21=json.dumps(season_21_map))


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
