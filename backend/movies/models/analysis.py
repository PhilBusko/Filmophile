"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE ANALYSIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, re
import pandas as PD
import numpy as NP
import plotly.graph_objects as GO

import sklearn.impute as IM
import sklearn.preprocessing as PP
import sklearn.decomposition as DC
import sklearn.linear_model as LM

import app_proj.settings as ST
import app_proj.utility as UT
import movies.models.tables as TB

FEATURE_PATH = 'movies/data/clean_feature.csv'


class FeatureEngineer(object):


    @staticmethod
    def GetFullDataframe():
        master_ls = TB.MasterMovie.objects.values()
        master_df = PD.DataFrame(master_ls).drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])
        master_df['Year'] = master_df['Year'].astype('int')
        master_df['RunTime'] = master_df['RunTime'].astype('Int64')
        master_df['Budget'] = master_df['Budget'].astype('Int64')
        master_df['Gross'] = master_df['Gross'].astype('Int64')
        master_df['VotesImdb'] = master_df['VotesImdb'].astype('Int64')
        return master_df


    @staticmethod
    def GetTypeDataframes(master_df):
        identity_df = master_df[['Movie_ID', 'Title']].copy()
        numeric_df = master_df[['Year', 'RunTime', 'Budget', 'Gross', 'ScoreImdb', 'VotesImdb']].copy()
        onehot_df = master_df[['Rating', 'Companies', 'Country', 'Language', 'Crew', 'Cast']].copy()
        multihot_df = master_df[['Genres']].copy()
        del master_df
        return (identity_df, numeric_df, onehot_df, multihot_df)


    @staticmethod
    def GetSingularMaximums():
        # ok to match total obs because will pca later

        total_obs = TB.UserVotes.objects.all().count()
        total_obs -= 220                        # subtract for country, language, genres, etc
        max_companies = int(total_obs / 2)
        max_crew = int(total_obs / 4)
        max_cast = int(total_obs / 4)
        return max_companies, max_crew, max_cast

    @staticmethod
    def SingularColumn(onehot_df, column, keep_max):

        # get the most frequent values of the column's lists

        full_ls = []
        for idx, row in onehot_df.iterrows():
            entry = row[column]
            if entry is None or entry == 'nan':
                continue
            
            full_ls += entry.split(', ')

        counts = PD.Series(full_ls).value_counts()

        keep_ls = []
        number_items = 0
        for val, cnt in counts.items():
            keep_ls.append(val.strip())
            number_items += 1
            if number_items > keep_max:
                break

        #print(keep_ls)

        # keep only the highest frequency entry found, if any

        def get_keep_only(entries):
            for kp in keep_ls:
                if entries is not None and kp in entries:
                    return kp
            return 'Other'

        onehot_df[column + '_sng'] = onehot_df[column].apply(get_keep_only)
        onehot_df = onehot_df.drop(columns=[column])

        return onehot_df


    @staticmethod
    def MultiHotEncode(multihot_df, column):

        import sklearn.preprocessing as PP
        mlb = PP.MultiLabelBinarizer()

        array_column = column + '_ls'
        multihot_df[array_column] = multihot_df[column].apply(lambda x: x.split(', ') if x else ['None'])
        array_out = mlb.fit_transform( multihot_df[array_column] )

        df_out = PD.DataFrame(data=array_out, columns=mlb.classes_)
        multihot_df = PD.merge(multihot_df, df_out, left_index=True, right_index=True)
        multihot_df = multihot_df.drop(columns=[column, array_column])

        return multihot_df        


    @staticmethod
    def OutputCSV(feature_df):
        save_path = os.path.join(ST.BASE_DIR, FEATURE_PATH)
        feature_df.to_csv(save_path, index=False)


    @staticmethod
    def RunFeatures():

        # this is the same call sequence as in the development notebook

        master_df = FeatureEngineer.GetFullDataframe()

        identity_df, numeric_df, onehot_df, multihot_df = FeatureEngineer.GetTypeDataframes(master_df)
        del master_df

        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Companies')
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Crew')
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Cast')
        onehot_dummy_df = PD.get_dummies(onehot_df, columns=['Rating', 'Country', 'Language', 'Companies_sng',
            'Crew_sng', 'Cast_sng'], drop_first=True, dummy_na=False)

        multihot_dummy_df = FeatureEngineer.MultiHotEncode(multihot_df, 'Genres')

        feature_df = PD.concat([identity_df, numeric_df, onehot_dummy_df, multihot_dummy_df], axis=1)

        FeatureEngineer.OutputCSV(feature_df)


    @staticmethod
    def GetTargetNFeatures():
        FEATURE_FILE = os.path.join(ST.BASE_DIR, FEATURE_PATH)
        feature_full_df = PD.read_csv(FEATURE_FILE)

        target_ls = TB.UserVotes.objects.values()
        target_full_df = PD.DataFrame(target_ls).drop(columns=['id'])

        full_df = PD.merge(target_full_df, feature_full_df, how='left', left_on='Movie_ID', right_on='Movie_ID')
        feature_df = full_df.drop(columns=['Movie_ID', 'Title', 'User', 'Vote'])
        target_df = target_full_df.drop(columns=['Movie_ID', 'User'])

        return (feature_df, target_df)


    @staticmethod
    def CreateSyntheticVotes():
        
        import random as RD
        RD.seed(666)
        number_votes = 900
        TB.UserVotes.objects.all().delete()

        # assume all movies in master table have a streaming index

        master_query = MasterMovie.objects.filter(ScoreImdb__isnull=False).filter(Genres__isnull=False)
        master_total = master_query.count()
        vote_ls = []
        unique_id_ls = []

        for vt in range(0, number_votes):
            random_idx = RD.randint(0, master_total-1)
            random_movie = master_query.values()[random_idx]

            movie_id = random_movie['Movie_ID']

            if movie_id in unique_id_ls:
                continue

            unique_id_ls.append(movie_id)

            score = random_movie['ScoreImdb']
            genres = random_movie['Genres']
            year = int(random_movie['Year'])
            bias = 0

            # set bias based on score, genre, year

            if score < 3:
                bias -= 40
            elif score < 5:
                bias -= 20
            elif score < 6:
                bias -= 10
            elif score < 7:
                bias += 0
            elif score < 8:
                bias += 5
            elif score < 9:
                bias += 15
            else:
                bias += 20

            if any(g in genres for g in ['Thriller', 'Fantasy', 'Sci-Fi', 'Mystery', 'Crime']):
                bias += 10

            if any(g in genres for g in ['Comedy', 'Family', 'Documentary', 'Music', 'Biography', 'Sport']):
                bias -= 10

            if year <= 1980:
                bias -= 10
            elif year <= 2000:
                bias += 0
            else:
                bias += 5

            # should be 10% of 3, 30% of 2, 60% of 1

            random_100 = RD.randint(1, 100) + bias

            if random_100 <= 60:
                vote = 1
            elif random_100 <= 90:
                vote = 2
            else:
                vote = 3

            #print(f"{random_movie['Title']} ({year}) {score} {genres} : {vote}")

            new_dx = {
                'Movie_ID': movie_id,
                'User': 'main',
                'Vote': vote,
            }
            vote_ls.append(new_dx)

        data_obj_ls = [UserVotes(**r) for r in vote_ls]
        UserVotes.objects.bulk_create(data_obj_ls)


    @staticmethod
    def GetRestrictedClassifiers():
        # this is a complex plot with 6 different classifers, so hardcoding makes sense

        return '{"data": [{"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16787], "type": "bar", "xaxis": "x", "yaxis": "y"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [2762, 2496, 11529], "type": "bar", "xaxis": "x2", "yaxis": "y2"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [14617, 1986, 184], "type": "bar", "xaxis": "x3", "yaxis": "y3"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16160, 584, 43], "type": "bar", "xaxis": "x4", "yaxis": "y4"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [10507, 3989, 2291], "type": "bar", "xaxis": "x5", "yaxis": "y5"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16787], "type": "bar", "xaxis": "x6", "yaxis": "y6"}], "layout": {"annotations": [{"font": {"size": 16}, "showarrow": false, "text": "Logistic Regression", "x": 0.14444444444444446, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Naive Bayes", "x": 0.5, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Nearest Neighbor", "x": 0.8555555555555556, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Random Forest", "x": 0.14444444444444446, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "SVM", "x": 0.5, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "XGBoost", "x": 0.8555555555555556, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "User Votes", "x": 0.5, "xanchor": "center", "xref": "paper", "y": -0.1, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Predicted Movies Count", "textangle": -90, "x": -0.07, "xanchor": "center", "xref": "paper", "y": 0.22, "yanchor": "bottom", "yref": "paper"}], "xaxis": {"anchor": "y", "domain": [0.0, 0.2888888888888889], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis": {"anchor": "x", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis2": {"anchor": "y2", "domain": [0.35555555555555557, 0.6444444444444445], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis2": {"anchor": "x2", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis3": {"anchor": "y3", "domain": [0.7111111111111111, 1.0], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis3": {"anchor": "x3", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis4": {"anchor": "y4", "domain": [0.0, 0.2888888888888889], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis4": {"anchor": "x4", "domain": [0.0, 0.45], "range": [0, 17000]}, "xaxis5": {"anchor": "y5", "domain": [0.35555555555555557, 0.6444444444444445], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis5": {"anchor": "x5", "domain": [0.0, 0.45], "range": [0, 17000]}, "xaxis6": {"anchor": "y6", "domain": [0.7111111111111111, 1.0], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis6": {"anchor": "x6", "domain": [0.0, 0.45], "range": [0, 17000]}, "template": {"data": {"barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Predicted Movie Counts for Each Algorithm", "x": 0.5, "y": 0.98, "xanchor": "center", "yanchor": "top"}, "width": 800, "height": 500, "margin": {"b": 50, "l": 70, "pad": 0, "r": 20, "t": 50}, "paper_bgcolor": "LightSteelBlue", "showlegend": false}}'


class LogisticRegression(object):


    @staticmethod
    def RunLogReg():

        pass



