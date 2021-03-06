"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
RECOMMENDATION ANALYSIS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import os, re
import pandas as PD
import numpy as NP
import django.db as DB
import plotly.graph_objects as GO
import plotly.figure_factory as FF

import sklearn.impute as IM
import sklearn.preprocessing as PP
import sklearn.decomposition as DC
import sklearn.linear_model as LM

import app_proj.utility as UT
import movies.models.tables as MT
import movies.extract.moviedb_helper as MH
import recommend.models.tables as RT

FEATURE_PATH = 'recommend/data/clean_feature.csv'


class General(object):


    # BROWSING PAGES

    @staticmethod
    def GetGenres():
        genres = [
            {'key': 1, 'value': 'Action'},
            {'key': 2, 'value': 'Adventure'},
            {'key': 3, 'value': 'Animation'},
            {'key': 4, 'value': 'Biography'},
            {'key': 5, 'value': 'Comedy'},
            {'key': 6, 'value': 'Crime'},
            {'key': 7, 'value': 'Documentary'},
            {'key': 8, 'value': 'Drama'},
            {'key': 9, 'value': 'Family'},
            {'key': 10, 'value': 'Fantasy'},
            {'key': 11, 'value': 'History'},
            {'key': 12, 'value': 'Horror'},
            {'key': 13, 'value': 'Music'},
            {'key': 14, 'value': 'Mystery'},
            {'key': 15, 'value': 'Romance'},
            {'key': 16, 'value': 'Sci-Fi'},
            {'key': 17, 'value': 'Sport'},
            {'key': 18, 'value': 'Thriller'},
            {'key': 19, 'value': 'War'},
            {'key': 20, 'value': 'Western'},
        ]
        return genres


    @staticmethod
    def GetRecomLevels():
        recom_ls = [
            {'key': 3, 'value': 'Love It'},
            {'key': 2, 'value': 'Maybe'},
            {'key': 1, 'value': 'Don\'t Bother'}
        ]
        return recom_ls


    @staticmethod
    def GetWatchedMovies():
        watched_ids = RT.UserScores.objects.all().values_list('Movie_ID', flat=True)
        movies_ls = MT.MasterMovie.objects.filter(Movie_ID__in=watched_ids
                                        ).order_by('-ScoreImdb').values()

        # hack until FK is up 

        votes_ls = RT.UserScores.objects.all().values()
        for mov in movies_ls:
            for vt in votes_ls:
                if mov['Movie_ID'] == vt['Movie_ID']:
                    mov['Score'] = vt['Score']
                    break

        thumb_url = MH.MovieDBHelper.GetPosterThumbUrl()
        for mov in movies_ls:
            poster_url = mov['Poster']
            if 'http' not in poster_url:
                mov['Poster'] = f"{thumb_url}{poster_url}"

        return movies_ls


    @staticmethod
    def GetToWatchMovies():

        # select_related will load movies from db also, which speeds up the function

        recom_ls = list(RT.UserRecommendations.objects.filter(User='main')
                        .select_related('Movie_FK').all())
        thumb_url = MH.MovieDBHelper.GetPosterThumbUrl()

        movie_ls = []
        for rec in recom_ls:
            movie_dx = rec.Movie_FK.__dict__
            state = movie_dx.pop('_state', None)
            mid = movie_dx.pop('id', None)
            movie_dx['RecomLevel'] = rec.RecomLevel

            poster_url = movie_dx['Poster']
            if 'http' not in poster_url:
                movie_dx['Poster'] = f"{thumb_url}{poster_url}"

            movie_ls.append(movie_dx)
        
        movie_ls = sorted(movie_ls, key=lambda mv: (-1)*mv['ScoreImdb'] if mv['ScoreImdb'] else 0)

        return movie_ls


    # DATA SCIENCE PAGE

    @staticmethod
    def GetDataHistory():
        history_ls = []
        tmdb_total = MT.MovieDB_Load.objects.count()
        imdb_total = MT.IMDB_Load.objects.count()
        reelgood_total = MT.Reelgood_Load.objects.count() 
        master_total = MT.MasterMovie.objects.count()

        new_dx = {
            'Feature': 'Title',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Year',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Rating',
            'TMDB': 0,
            'IMDB': MT.IMDB_Load.objects.filter(Rating__isnull=False).
                    exclude(Rating__in=['Not Rated', 'Unrated', 'Approved', 'Passed']).count(),
            'Reelgood': MT.Reelgood_Load.objects.filter(Rating__isnull=False).count(),
            'Union-All': MT.MasterMovie.objects.filter(Rating__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Companies',
            'TMDB': MT.MovieDB_Load.objects.filter(Companies__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Companies__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Companies__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Country',
            'TMDB': MT.MovieDB_Load.objects.filter(Country__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Country__isnull=False).count(),
            'Reelgood': MT.Reelgood_Load.objects.filter(Country__isnull=False).count(),
            'Union-All': MT.MasterMovie.objects.filter(Country__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Language',
            'TMDB': MT.MovieDB_Load.objects.filter(Language__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Language__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Language__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'RunTime',
            'TMDB': MT.MovieDB_Load.objects.filter(RunTime__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Duration__isnull=False).count(),
            'Reelgood': MT.Reelgood_Load.objects.filter(Duration__isnull=False).count(),
            'Union-All': MT.MasterMovie.objects.filter(RunTime__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Crew*',
            'TMDB': MT.MovieDB_Load.objects.filter(Crew__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Directors__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Crew__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Cast*',
            'TMDB': MT.MovieDB_Load.objects.filter(Cast__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Actors__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Cast__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Genres*',
            'TMDB': MT.MovieDB_Load.objects.filter(Genres__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Genres__isnull=False).count(),
            'Reelgood': MT.Reelgood_Load.objects.filter(Genres__isnull=False).count(),
            'Union-All': MT.MasterMovie.objects.filter(Genres__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Budget',
            'TMDB': MT.MovieDB_Load.objects.filter(Budget__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(Budget__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Budget__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'Gross',
            'TMDB': MT.MovieDB_Load.objects.filter(Gross__isnull=False).count(),
            'IMDB': MT.IMDB_Load.objects.filter(GrossWorldwide__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(Gross__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'ImdbScore',
            'TMDB': 0,
            'IMDB': MT.IMDB_Load.objects.filter(Score__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MT.MasterMovie.objects.filter(ScoreImdb__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Feature': 'StreamingId',
            'TMDB': 0,
            'IMDB': 0,
            'Reelgood': MT.Reelgood_Load.objects.filter(Services__isnull=False).count(),
            'Union-All': MT.MasterMovie.objects.filter(Indeces__isnull=False).count(),
        }
        history_ls.append(new_dx)

        # normalize the values, done here to simplify the above code

        for row in history_ls:
            row['TMDB'] = round(row['TMDB'] / tmdb_total * 100, 1)
            row['IMDB'] = round(row['IMDB'] / imdb_total * 100, 1)
            row['Reelgood'] = round(row['Reelgood'] / reelgood_total * 100, 1)
            row['Union-All'] = round(row['Union-All'] / master_total * 100, 1)

        return history_ls


    @staticmethod
    def GetSyntheticScores():
        # this is just for data science blog, so keep a constant figure

        return '{"data": [{"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [574, 231, 76], "type": "bar"}], "layout": {"template": {"data": {"barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "User Movie Scores"}, "xaxis": {"title": {"text": "Number of Stars"}, "tickvals": [1, 2, 3]}, "yaxis": {"title": {"text": "Movie Count"}, "tickvals": [0, 100, 200, 300, 400, 500, 600, 700, 800, 900]}, "width": 400, "height": 300, "margin": {"b": 50, "l": 70, "pad": 0, "r": 20, "t": 50}, "paper_bgcolor": "LightSteelBlue"}}'


    @staticmethod
    def GetRestrictedClassifiers():
        # this is a complex plot with 6 different classifers, so hardcoding makes sense

        return '{"data": [{"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16787], "type": "bar", "xaxis": "x", "yaxis": "y"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [2762, 2496, 11529], "type": "bar", "xaxis": "x2", "yaxis": "y2"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [14617, 1986, 184], "type": "bar", "xaxis": "x3", "yaxis": "y3"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16160, 584, 43], "type": "bar", "xaxis": "x4", "yaxis": "y4"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [10507, 3989, 2291], "type": "bar", "xaxis": "x5", "yaxis": "y5"}, {"marker": {"color": ["crimson", "seagreen", "gold"]}, "x": [1, 2, 3], "y": [16787], "type": "bar", "xaxis": "x6", "yaxis": "y6"}], "layout": {"annotations": [{"font": {"size": 16}, "showarrow": false, "text": "Logistic Regression", "x": 0.14444444444444446, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Naive Bayes", "x": 0.5, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Nearest Neighbor", "x": 0.8555555555555556, "xanchor": "center", "xref": "paper", "y": 1.0, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Random Forest", "x": 0.14444444444444446, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "SVM", "x": 0.5, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "XGBoost", "x": 0.8555555555555556, "xanchor": "center", "xref": "paper", "y": 0.45, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "User Votes", "x": 0.5, "xanchor": "center", "xref": "paper", "y": -0.1, "yanchor": "bottom", "yref": "paper"}, {"font": {"size": 16}, "showarrow": false, "text": "Predicted Movies Count", "textangle": -90, "x": -0.07, "xanchor": "center", "xref": "paper", "y": 0.22, "yanchor": "bottom", "yref": "paper"}], "xaxis": {"anchor": "y", "domain": [0.0, 0.2888888888888889], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis": {"anchor": "x", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis2": {"anchor": "y2", "domain": [0.35555555555555557, 0.6444444444444445], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis2": {"anchor": "x2", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis3": {"anchor": "y3", "domain": [0.7111111111111111, 1.0], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis3": {"anchor": "x3", "domain": [0.55, 1.0], "range": [0, 17000]}, "xaxis4": {"anchor": "y4", "domain": [0.0, 0.2888888888888889], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis4": {"anchor": "x4", "domain": [0.0, 0.45], "range": [0, 17000]}, "xaxis5": {"anchor": "y5", "domain": [0.35555555555555557, 0.6444444444444445], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis5": {"anchor": "x5", "domain": [0.0, 0.45], "range": [0, 17000]}, "xaxis6": {"anchor": "y6", "domain": [0.7111111111111111, 1.0], "tickvals": [1, 2, 3], "range": [0.4, 3.6]}, "yaxis6": {"anchor": "x6", "domain": [0.0, 0.45], "range": [0, 17000]}, "template": {"data": {"barpolar": [{"marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "barpolar"}], "bar": [{"error_x": {"color": "#2a3f5f"}, "error_y": {"color": "#2a3f5f"}, "marker": {"line": {"color": "#E5ECF6", "width": 0.5}}, "type": "bar"}], "carpet": [{"aaxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "baxis": {"endlinecolor": "#2a3f5f", "gridcolor": "white", "linecolor": "white", "minorgridcolor": "white", "startlinecolor": "#2a3f5f"}, "type": "carpet"}], "choropleth": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "choropleth"}], "contourcarpet": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "contourcarpet"}], "contour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "contour"}], "heatmapgl": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmapgl"}], "heatmap": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "heatmap"}], "histogram2dcontour": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2dcontour"}], "histogram2d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "histogram2d"}], "histogram": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "histogram"}], "mesh3d": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "type": "mesh3d"}], "parcoords": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "parcoords"}], "pie": [{"automargin": true, "type": "pie"}], "scatter3d": [{"line": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter3d"}], "scattercarpet": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattercarpet"}], "scattergeo": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergeo"}], "scattergl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattergl"}], "scattermapbox": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scattermapbox"}], "scatterpolargl": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolargl"}], "scatterpolar": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterpolar"}], "scatter": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatter"}], "scatterternary": [{"marker": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "type": "scatterternary"}], "surface": [{"colorbar": {"outlinewidth": 0, "ticks": ""}, "colorscale": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "type": "surface"}], "table": [{"cells": {"fill": {"color": "#EBF0F8"}, "line": {"color": "white"}}, "header": {"fill": {"color": "#C8D4E3"}, "line": {"color": "white"}}, "type": "table"}]}, "layout": {"annotationdefaults": {"arrowcolor": "#2a3f5f", "arrowhead": 0, "arrowwidth": 1}, "coloraxis": {"colorbar": {"outlinewidth": 0, "ticks": ""}}, "colorscale": {"diverging": [[0, "#8e0152"], [0.1, "#c51b7d"], [0.2, "#de77ae"], [0.3, "#f1b6da"], [0.4, "#fde0ef"], [0.5, "#f7f7f7"], [0.6, "#e6f5d0"], [0.7, "#b8e186"], [0.8, "#7fbc41"], [0.9, "#4d9221"], [1, "#276419"]], "sequential": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]], "sequentialminus": [[0.0, "#0d0887"], [0.1111111111111111, "#46039f"], [0.2222222222222222, "#7201a8"], [0.3333333333333333, "#9c179e"], [0.4444444444444444, "#bd3786"], [0.5555555555555556, "#d8576b"], [0.6666666666666666, "#ed7953"], [0.7777777777777778, "#fb9f3a"], [0.8888888888888888, "#fdca26"], [1.0, "#f0f921"]]}, "colorway": ["#636efa", "#EF553B", "#00cc96", "#ab63fa", "#FFA15A", "#19d3f3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"], "font": {"color": "#2a3f5f"}, "geo": {"bgcolor": "white", "lakecolor": "white", "landcolor": "#E5ECF6", "showlakes": true, "showland": true, "subunitcolor": "white"}, "hoverlabel": {"align": "left"}, "hovermode": "closest", "mapbox": {"style": "light"}, "paper_bgcolor": "white", "plot_bgcolor": "#E5ECF6", "polar": {"angularaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "radialaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "scene": {"xaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "yaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}, "zaxis": {"backgroundcolor": "#E5ECF6", "gridcolor": "white", "gridwidth": 2, "linecolor": "white", "showbackground": true, "ticks": "", "zerolinecolor": "white"}}, "shapedefaults": {"line": {"color": "#2a3f5f"}}, "ternary": {"aaxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "baxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}, "bgcolor": "#E5ECF6", "caxis": {"gridcolor": "white", "linecolor": "white", "ticks": ""}}, "title": {"x": 0.05}, "xaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}, "yaxis": {"automargin": true, "gridcolor": "white", "linecolor": "white", "ticks": "", "title": {"standoff": 15}, "zerolinecolor": "white", "zerolinewidth": 2}}}, "title": {"text": "Predicted Movie Counts for Each Algorithm", "x": 0.5, "y": 0.98, "xanchor": "center", "yanchor": "top"}, "width": 800, "height": 500, "margin": {"b": 50, "l": 70, "pad": 0, "r": 20, "t": 50}, "paper_bgcolor": "LightSteelBlue", "showlegend": false}}'


    # ADMIN

    @staticmethod
    def GetTableCounts():

        count_ls = []

        # get the tables

        table_ls = [ table for table, clss in RT.__dict__.items() if isinstance(clss, type) ]

        for tbl in table_ls:
            command = f'RT.{tbl}.objects.count()'
            count = eval(command)
            new_dx ={
                'Table': tbl,
                'Count': count,
            }
            count_ls.append(new_dx)

        # get file count

        file_cnt = 0
        feature_path = os.path.join(UT.BASE_DIR, FEATURE_PATH)
        if os.path.exists(feature_path):
            file_cnt = 1

        new_dx ={
            'Table': 'Features (File)',
            'Count': file_cnt,
        }
        count_ls.append(new_dx)
        
        return count_ls


    @staticmethod
    def DeleteTable(table_name):
        if table_name == 'UserScores' or table_name == 'All':
            RT.UserScores.objects.all().delete()
        if table_name == 'UserRecommendations' or table_name == 'All':
            RT.UserRecommendations.objects.all().delete()

        # delete features file

        feature_path = os.path.join(UT.BASE_DIR, FEATURE_PATH)
        if os.path.exists(feature_path):
            os.remove(feature_path)


class FeatureEngineer(object):


    @staticmethod
    def GetFullDataframe():
        master_ls = MT.MasterMovie.objects.values()
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

        total_obs = RT.UserScores.objects.all().count()
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
        save_path = os.path.join(UT.BASE_DIR, FEATURE_PATH)
        feature_df.to_csv(save_path, index=False)


    @staticmethod
    def RunFeatures():

        # this is the same call sequence as in the development notebook

        master_df = FeatureEngineer.GetFullDataframe()

        identity_df, numeric_df, onehot_df, multihot_df = FeatureEngineer.GetTypeDataframes(master_df)
        del master_df

        max_companies, max_crew, max_cast = FeatureEngineer.GetSingularMaximums()

        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Companies', max_companies)
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Crew', max_crew)
        onehot_df = FeatureEngineer.SingularColumn(onehot_df, 'Cast', max_cast)
        onehot_dummy_df = PD.get_dummies(onehot_df, columns=['Rating', 'Country', 'Language', 'Companies_sng',
            'Crew_sng', 'Cast_sng'], drop_first=True, dummy_na=False)

        multihot_dummy_df = FeatureEngineer.MultiHotEncode(multihot_df, 'Genres')

        feature_df = PD.concat([identity_df, numeric_df, onehot_dummy_df, multihot_dummy_df], axis=1)

        FeatureEngineer.OutputCSV(feature_df)


    @staticmethod
    def GetTargetNFeatures():
        feature_path = os.path.join(UT.BASE_DIR, FEATURE_PATH)
        feature_all_df = PD.read_csv(feature_path)

        target_ls = RT.UserScores.objects.values()
        target_df = PD.DataFrame(target_ls).drop(columns=['id'])
        feature_wtarget_df = feature_all_df.loc[feature_all_df['Movie_ID'].isin(target_df['Movie_ID'])==True]
        feature_topred_df = feature_all_df.loc[feature_all_df['Movie_ID'].isin(target_df['Movie_ID'])==False]

        feature_wtarget_df = feature_wtarget_df.drop(columns=['Movie_ID', 'Title'])
        target_df = target_df['Score']

        return (feature_wtarget_df, target_df, feature_topred_df)


    @staticmethod
    def CreateSyntheticVotes():
        
        import random as RD
        RD.seed(2)
        number_votes = 900
        RT.UserScores.objects.all().delete()

        # assume all movies in master table have a streaming index

        master_query = MT.MasterMovie.objects.filter(ScoreImdb__isnull=False).filter(Genres__isnull=False)
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
                bias += 20

            if any(g in genres for g in ['Comedy', 'Music', 'Biography']):
                bias -= 10

            if any(g in genres for g in ['Family', 'Documentary', 'Sport']):
                bias -= 25

            if year <= 1980:
                bias -= 30
            elif year <= 2000:
                bias -= 10
            elif year >= 2010:
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
                'Score': vote,
            }
            vote_ls.append(new_dx)

        data_obj_ls = [RT.UserScores(**r) for r in vote_ls]
        RT.UserScores.objects.bulk_create(data_obj_ls)


class SvmClassifier(object):


    @staticmethod
    def RunRecommendations():

        feature_wtarget_df, target_df, feature_topred_df = FeatureEngineer.GetTargetNFeatures()

        svm = SvmClassifier.TrainSvm(feature_wtarget_df, target_df)

        predict_ls = SvmClassifier.PredictUnwatched(svm, feature_wtarget_df, feature_topred_df)

        # insert to db

        RT.UserRecommendations.objects.all().delete()
        data_obj_ls = [RT.UserRecommendations(**r) for r in predict_ls]
        RT.UserRecommendations.objects.bulk_create(data_obj_ls)


    @staticmethod
    def TrainSvm(feature_wtarget_df, target_df):
        X_np = NP.array(feature_wtarget_df)
        y_np = NP.array(target_df)

        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        X_impute = imputer.fit_transform(X_np)
        scaler = PP.StandardScaler()
        X_scale = scaler.fit_transform(X_impute)

        LEARNING = 'invscaling'
        ETA0 = 0.01
        POWERT = None
        MAX_ITER = 200
        LOSS = 'epsilon_insensitive'
        PENALTY= None
        CLASS = None

        svm = LM.SGDClassifier(learning_rate=LEARNING, eta0=ETA0, max_iter=MAX_ITER, loss=LOSS)
        svm.fit(X_scale, y_np)

        return svm


    @staticmethod
    def PredictUnwatched(svm, feature_wtarget_df, feature_topred_df):

        # preprocess the features and make predictions

        X_np = NP.array(feature_wtarget_df)
        imputer = IM.SimpleImputer(missing_values=NP.nan, strategy='mean')
        X_impute = imputer.fit_transform(X_np)
        scaler = PP.StandardScaler()
        scaler.fit(X_impute)

        X_pred = NP.array(feature_topred_df.drop(columns=['Movie_ID', 'Title']))
        X_pred_impute = imputer.transform(X_pred)
        X_pred_scale = scaler.transform(X_pred_impute)
        predict_np = svm.predict(X_pred_scale)

        # append the movie-id to the predictions

        feature_tpreset_df = feature_topred_df.reset_index()

        predict_ls = []
        for idx, row in feature_tpreset_df.iterrows():
            movie_id = int(row['Movie_ID'])
            # get movie by Movie_ID, since features aren't part of db yet, though Movie_ID is unique
            movie_md = MT.MasterMovie.objects.get(Movie_ID=movie_id)
            new_dx = {
                'Movie_FK': movie_md,
                'User': 'main',
                'RecomLevel': predict_np[idx],
            }
            predict_ls.append(new_dx)

        return predict_ls

