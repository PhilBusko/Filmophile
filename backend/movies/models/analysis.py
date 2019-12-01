"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE ANALYSIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, re
import pandas as PD
import numpy as NP
import plotly.graph_objects as GO

import app_proj.settings as ST
import app_proj.utility as UT
import movies.models.models as MD

FEATURE_PATH = 'movies/data/clean_feature.csv'


class FeatureEngineer(object):


    @staticmethod
    def GetFullDataframe():
        master_ls = MD.MasterMovie.objects.values()
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

        total_obs = MD.UserVotes.objects.all().count()
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

        target_ls = MD.UserVotes.objects.values()
        target_full_df = PD.DataFrame(target_ls).drop(columns=['id'])

        full_df = PD.merge(target_full_df, feature_full_df, how='left', left_on='Movie_ID', right_on='Movie_ID')
        feature_df = full_df.drop(columns=['Movie_ID', 'Title', 'User', 'Vote'])
        target_df = target_full_df.drop(columns=['Movie_ID', 'User'])

        return (feature_df, target_df)


class LogisticRegression(object):


    @staticmethod
    def GetAlgorithms():

        MAX_ITER = 2000
        ALPHA = NP.array([1e-3, 1e-2, 1e-1, 1e0, 1e1, 1e2, 1e3, 1e4])
        algorithms = []

        feature_df, target_df = FeatureEngineer.GetTargetNFeatures()
        X_np = NP.array(feature_df)
        y_np = NP.array(target_df['Vote'])

        # liblinear with L1

        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        scaler = PP.StandardScaler()
        #pca = DC.PCA(n_components=)
        logreg = LM.LogisticRegression(solver='liblinear', penalty='l1', multi_class='auto', max_iter=MAX_ITER)
        pipeline = PL.Pipeline([('imputer', imputer), ('scaler', scaler), ('estimator', logreg)])
        param_dx = {
            'estimator__C': 1 / ALPHA,
            }

        searcher = MS.GridSearchCV(pipeline, param_dx, scoring='accuracy', cv=5)
        searcher.fit(X_np, y_np)

        new_dx = {
            'algorithm': 'liblinear-L1',
            'test_scores': list(searcher.cv_results_['mean_test_score']),
        }
        algorithms.append(new_dx)

        # liblinear with L2

        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        scaler = PP.StandardScaler()
        #pca = DC.PCA(n_components=)
        logreg = LM.LogisticRegression(solver='liblinear', penalty='l2', multi_class='auto', max_iter=MAX_ITER)
        pipeline = PL.Pipeline([('imputer', imputer), ('scaler', scaler), ('estimator', logreg)])
        param_dx = {
            'estimator__C': 1 / ALPHA,
            }

        searcher = MS.GridSearchCV(pipeline, param_dx, scoring='accuracy', cv=5)
        searcher.fit(X_np, y_np);

        new_dx = {
            'algorithm': 'liblinear-L2',
            'test_scores': list(searcher.cv_results_['mean_test_score']),
        }
        algorithms.append(new_dx)

        # saga with L1

        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        scaler = PP.StandardScaler()
        #pca = DC.PCA(n_components=)
        logreg = LM.LogisticRegression(solver='saga', penalty='l1', multi_class='auto', max_iter=MAX_ITER)
        pipeline = PL.Pipeline([('imputer', imputer), ('scaler', scaler), ('estimator', logreg)])
        param_dx = {
            'estimator__C': 1 / ALPHA,
            }

        searcher = MS.GridSearchCV(pipeline, param_dx, scoring='accuracy', cv=5)
        searcher.fit(X_np, y_np)

        # saga with L2

        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        scaler = PP.StandardScaler()
        #pca = DC.PCA(n_components=)
        logreg = LM.LogisticRegression(solver='saga', penalty='l2', multi_class='auto', max_iter=MAX_ITER)
        pipeline = PL.Pipeline([('imputer', imputer), ('scaler', scaler), ('estimator', logreg)])
        param_dx = {
            'estimator__C': 1 / ALPHA,
            }

        searcher = MS.GridSearchCV(pipeline, param_dx, scoring='accuracy', cv=5)
        searcher.fit(X_np, y_np)

        new_dx = {
            'algorithm': 'saga-L2',
            'test_scores': list(searcher.cv_results_['mean_test_score']),
        }
        algorithms.append(new_dx)

        return algorithms


    @staticmethod
    def InsertAlgorithms(algorithms):

        pass
    

    @staticmethod
    def GetPlot():

        # get the data


        # create the plot in memory

        fig = GO.Figure()
        colors = ['orange', 'red', 'darkcyan', 'green']

        for idx, alg in enumerate(algorithms):
            fig.add_trace(
                GO.Scatter(x = ALPHA, y = alg['test_scores'],
                    name=alg['algorithm'], marker={'color': colors[idx]}, mode='lines+markers'))

        fig.update_layout(
            title="Logistic Regression CV-Test Scores",
            xaxis_title="lambda",
            yaxis_title="Accuracy",
            width=600,
            height=400,
            margin=GO.layout.Margin(t=50, r=10, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
        )
        fig.update_xaxes(tickvals=ALPHA, type="log")
        fig.update_yaxes(range=[0.52, 0.66])


    @staticmethod
    def GetHardcodedFigure():
        # quick and dirty way of getting analysis graph up to front end
        # better way is to store algorithm results in db, then run figure and encode it
        return '{"data": [{"marker": {"color": "orange"}, "mode": "lines+markers", "name": "liblinear-L1", "x": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0], "y": [0.545, 0.545, 0.545, 0.56, 0.6266666666666667, 0.6383333333333333, 0.6383333333333333, 0.6383333333333333], "type": "scatter"}, {"marker": {"color": "red"}, "mode": "lines+markers", "name": "liblinear-L2", "x": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0], "y": [0.5433333333333333, 0.545, 0.54, 0.5416666666666666, 0.5433333333333333, 0.5533333333333333, 0.545, 0.5333333333333333], "type": "scatter"}, {"marker": {"color": "darkcyan"}, "mode": "lines+markers", "name": "saga-L1", "x": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0], "y": [0.5416666666666666, 0.5483333333333333, 0.5516666666666666, 0.56, 0.6283333333333333, 0.6383333333333333, 0.6383333333333333, 0.6383333333333333], "type": "scatter"}, {"marker": {"color": "green"}, "mode": "lines+markers", "name": "saga-L2", "x": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0], "y": [0.5416666666666666, 0.5416666666666666, 0.5483333333333333, 0.5466666666666666, 0.55, 0.6083333333333333, 0.6383333333333333, 0.6383333333333333], "type": "scatter"}], "layout": {"template": {"data": {"barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Logistic Regression CV-Test Scores"}, "xaxis": {"title": {"text": "lambda"}, "tickvals": [0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0], "type": "log"}, "yaxis": {"title": {"text": "Accuracy"}, "range": [0.52, 0.66]}, "width": 600, "height": 400, "margin": {"b": 50, "l": 70, "pad": 0, "r": 10, "t": 50}, "paper_bgcolor": "LightSteelBlue"}}'




