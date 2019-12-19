"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
EXPLORATION LOGIC
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, json, time
import pandas as PD
import numpy as NP
import plotly.graph_objects as GO
import plotly.figure_factory as FF
import plotly.subplots as SB

import app_proj.settings as ST
import app_proj.utility as UT
import movies.models.tables as TB
import movies.models.data_manager as DM


class Explore(object):


    @staticmethod
    def GetPlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])


        # run calculations


        # create plot figure


        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    # INDUSTRY 

    @staticmethod
    def GetYearPlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])

        master_df = master_df.loc[master_df['Year']>='1980']

        # run calculations


        # create plot figure

        fig = GO.Figure()
        fig.add_trace(GO.Histogram(x=master_df['Year'], xbins={'size': 1}, marker_color='DarkOliveGreen'))

        fig.update_layout(
            title="Number of Movies Per Year",
            xaxis_title="Year",
            yaxis_title="Movies Count",
            width=600,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=80, pad=0),
            paper_bgcolor="LightSteelBlue",
        )

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetCountriesPlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])

        master_df = master_df.dropna(axis=0, subset=['Country'])
        master_df = master_df.loc[master_df['Country']!='nan'].reset_index().copy()

        # run calculations

        group_df = master_df.groupby('Country').count()['Movie_ID'].sort_values(ascending=False)
        others_df = group_df.loc[group_df.index!='USA']
        primary_x = ['USA', 'All Others']
        primary_y = [group_df[group_df.index=='USA'].values[0], others_df.sum()]
        plot_df = others_df[:12]

        # create plot figure

        COLOR = 'mediumpurple'
        fig = SB.make_subplots(rows=1, cols=2, column_widths=[0.25, 0.75], 
                            subplot_titles=("Top Countries", "Secondary Countries"))

        fig.add_trace(
            GO.Bar(x=primary_x, y=primary_y, marker_color=COLOR, hoverlabel={'namelength': 0}), 
            row=1, col=1)
        fig.add_trace(
            GO.Bar(x=plot_df.index, y=plot_df.values, marker_color=COLOR, hoverlabel={'namelength': 0}), 
            row=1, col=2)

        fig.update_layout(
            title={'text': "Countries That Make Movies", 'x':0.5, 'y':0.99,  
                'xanchor': 'center', 'yanchor': 'top'},
            width=600,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
            showlegend=False,
        )

        # extend annotations so they don't override the subplot titles

        annotations = [a.to_plotly_json() for a in fig["layout"]["annotations"]]
        annotations.append({'font': {'size': 16}, 'showarrow': False, 'text': 'Movie Counts', 
                            'x': -0.08, 'xanchor': 'center', 'xref': 'paper', 
                            'y': 0.4, 'yanchor': 'bottom', 'yref': 'paper', 'textangle':-90})
        fig["layout"]["annotations"] = annotations

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetGenresPlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])

        master_df = master_df.dropna(axis=0, subset=['Genres']).reset_index().copy()
        master_df = master_df.drop(columns=['level_0', 'index'], errors='ignore')

        # run calculations

        genre_dist_ls = []

        for idx, row in master_df.iterrows():
            genres_tx = row['Genres']
            genres_ls = genres_tx.split(', ')
            
            for gnr in genres_ls:
                if gnr.strip() != '':
                    genre_dist_ls.append(gnr)

        # create plot figure

        fig = GO.Figure()
        fig.add_trace(GO.Histogram(x=genre_dist_ls, marker_color='brown', histnorm='probability'))

        fig.update_layout(
            title="Number of Movies With Genre",
            yaxis_title="Percentage",
            width=700,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=10, pad=0),
            paper_bgcolor="LightSteelBlue",
            yaxis_tickformat = '%' 
        )
        fig.update_xaxes(categoryorder="total descending")

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetGenresMoviePlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])

        master_df = master_df.dropna(axis=0, subset=['Genres']).reset_index().copy()
        master_df = master_df.drop(columns=['level_0', 'index'], errors='ignore')

        # run calculations

        genres_dist_ls = []

        for idx, row in master_df.iterrows():
            genres_tx = row['Genres']
            genres_ls = genres_tx.split(', ')
            
            cnt = 0
            for gnr in genres_ls:
                if gnr.strip() != '':
                    cnt += 1
                if cnt > 0 and cnt <= 5:
                    genres_dist_ls.append(cnt)

        # create plot figure

        fig = GO.Figure()
        fig.add_trace( GO.Histogram(x=genres_dist_ls, marker_color='darkslategrey', histnorm='probability') )

        fig.update_layout(
            title="Number of Genres per Movie",
            yaxis_title="Percentage",
            xaxis_title="Number of Genres",
            width=500,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=10, pad=0),
            paper_bgcolor="LightSteelBlue",
            yaxis_tickformat = '%',
            bargap=0.2,
        )

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetRoiPlot():

        # get the data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        roi_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])

        roi_df = roi_df.dropna(axis=0, subset=['Budget', 'Gross'])
        roi_df = roi_df.loc[ (roi_df['Budget']<201e6) ]


        # drop randomly to keep graph from being cluttered

        roi_df = roi_df.reset_index().copy()

        import random as RD
        RD.seed(time.time())
        number_movies = 1500
        random_ls = []

        for mv in range(0, number_movies):
            random_idx = RD.randint(0, roi_df.shape[0]-1)
            random_movie = roi_df.loc[random_idx]
            random_ls.append(random_movie)

        roi_df = PD.DataFrame(random_ls)
        roi_df = roi_df.drop_duplicates(subset=['Movie_ID'])

        # calculate new financial columns

        roi_df['profit'] = (roi_df['Gross'] - roi_df['Budget']) 
        roi_df['roi'] = (roi_df['Gross'] - roi_df['Budget']) / roi_df['Budget']

        roi_df = roi_df.loc[ (roi_df['roi']<5e5) ]
        roi_df = roi_df.loc[ (roi_df['profit']<1e9) ]

        # create new columns for plotting 

        GROUPS = [0, 1, 2, 3]
        NAMES = ['RoI < 0', 'RoI < 2', 'RoI < 10', 'RoI > 10']
        COLORS = ['crimson', 'blue', 'green', 'goldenrod']

        def RoiGroup(row):
            roi = row['roi']
            if roi <= 0:
                return 0
            if roi <= 2: 
                return 1
            if roi <= 10:
                return 2   
            return 3

        roi_df['roi_group'] = roi_df.apply(RoiGroup, axis=1)


        def RoiText(row):
            title = row['Title']
            roi = row['roi']
            hover_tx = f'{title}<br>RoI: <b>{roi : .1f}</b>'
            return hover_tx

        roi_df['roi_text'] = roi_df.apply(RoiText, axis=1)


        # plot the roi

        fig = GO.Figure()

        for g in GROUPS:
            df = roi_df.loc[roi_df['roi_group']==g]
            fig.add_trace(GO.Scatter(x=df['Budget'], y=df['profit'], name=NAMES[g], 
                                    mode='markers', marker={'color': COLORS[g]},  
                                    text=df['roi_text'], hovertemplate ='<span>%{text}</span>', 
                                    hoverlabel={'namelength': 0}))

        fig.update_layout(
            title="Return on Investment",
            xaxis_title="Budget ($ dollars)",
            yaxis_title="Profit ($ dollars)",
            width=700,
            height=400,
            margin=GO.layout.Margin(t=60, r=10, b=50, l=80, pad=0),
            paper_bgcolor="LightSteelBlue",
        )
        fig.update_xaxes(range=(-25e6, 225e6))
        fig.update_yaxes(range=(-100e6, 1e9))

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetScoreProfitPlot():

        # prepare data

        master_ls = list(TB.MasterMovie.objects.values())
        master_df = PD.DataFrame(master_ls)
        master_df = master_df.drop(columns=['id', 'OriginalTitle', 'Poster', 'Synopsis', 'Indeces'])
        scoreprofit_df = master_df.dropna(axis=0, subset=['Budget', 'Gross', 'ScoreImdb'])

        # run calculations

        scoreprofit_df['profit'] = (scoreprofit_df['Gross'] - scoreprofit_df['Budget']) 
        scoreprofit_df = scoreprofit_df.loc[ (scoreprofit_df['profit']<2e8) ]

        def ScoreProfitText(row):
            title = row['Title']
            profit = row['profit']
            score = row['ScoreImdb']
            hover_tx = f'{title}<br><b>{score}</b>  ${profit:.0e}'
            return hover_tx

        scoreprofit_df['sp_text'] = scoreprofit_df.apply(ScoreProfitText, axis=1)
        scoreprofit_df[['Title', 'profit', 'sp_text']][:5]

        # create plot figure

        fig = GO.Figure()
        fig.add_trace(GO.Scatter(x=scoreprofit_df['profit'], y=scoreprofit_df['ScoreImdb'],  
                                mode='markers', marker={'color': 'seagreen'},  
                                text=scoreprofit_df['sp_text'], hovertemplate ='<span>%{text}</span>', 
                                hoverlabel={'namelength': 0}))

        fig.update_layout(
            title="IMDB Score vs Profit",
            xaxis_title="Profit ($ dollars)",
            yaxis_title="IMDB Score",
            width=500,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=60, pad=0),
            paper_bgcolor="LightSteelBlue",
            #xaxis_type="log", 
        )

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    # SERVICES 
 
    @staticmethod
    def GetTotalsPlot():

        # get the data
        # later must filter by active movies

        master_ls = list(TB.MasterMovie.objects.values())
        year_distrib = {'netflix': [], 'amazon': [], 'hulu': []}

        for mov in master_ls:
            year = int(mov['Year'])
            index_dx = json.loads(mov['Indeces'])
            
            for key, val in index_dx.items():
                if key in year_distrib and year >= 1980:
                    year_distrib[key].append(year)

        # create the plot 

        fig = GO.Figure()
        fig.add_trace(GO.Histogram(x= year_distrib['amazon'], xbins={'size': 1}, name='Amazon', 
                                marker_color='darkblue', opacity=0.6))
        fig.add_trace(GO.Histogram(x= year_distrib['netflix'], xbins={'size': 1}, name='Netflix', 
                                marker_color='crimson', opacity=0.7))
        fig.add_trace(GO.Histogram(x= year_distrib['hulu'], xbins={'size': 1}, name='Hulu', 
                                marker_color='green', opacity=0.8))
        fig.update_layout(
            title="Total Movie Count for Each Service",
            xaxis_title="Release Year",
            yaxis_title="Movie Count",
            width=600,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
            barmode='overlay', 
        )

        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetScoresPlot():

        # get the data
        # later must filter by active movies

        master_ls = list(TB.MasterMovie.objects.values())
        score_distrib = {'netflix': [], 'amazon': [], 'hulu': []}
        total_cnt = {'netflix': 0, 'amazon': 0, 'hulu': 0}

        for mov in master_ls:
            score = mov['ScoreImdb']
            if score is None:
                continue
            
            index_dx = json.loads(mov['Indeces'])
            
            # only keep exclusive content to each service 
            
            exclusive = 0
            for key, val in index_dx.items():
                if key in score_distrib:
                    exclusive += 1
                    
            if exclusive > 1:
                continue
            
            year = int(mov['Year'])
            
            for key, val in index_dx.items():
                if key in score_distrib and year >= 1980:
                    score_distrib[key].append(score)
                    total_cnt[key] += 1

        # create the plot 

        hist_data = [score_distrib['hulu'], score_distrib['netflix'], score_distrib['amazon']]
        group_labels = ['Hulu', 'Netflix', 'Amazon']
        colors = ['green', 'crimson', 'darkblue']

        fig = FF.create_distplot(hist_data, group_labels, colors=colors, 
                                bin_size=.1, show_hist=False, show_rug=False )

        fig.update_layout(
            title="IMDB Score for Movies Exclusively in Each Service",
            xaxis_title="IMDB Score",
            yaxis_title="Percentage",
            width=600,
            height=400,
            margin=GO.layout.Margin(t=60, r=10, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
            barmode='overlay', 
            yaxis_tickformat = '%', 
        )
        fig.update_xaxes(tickvals=list(range(0, 10, 1)))
        
        # format and send to frontend

        return DM.Reporter.ConvertFigureToJson(fig)

