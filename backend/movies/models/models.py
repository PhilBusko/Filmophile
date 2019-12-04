"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, csv, re, json
import pandas as PD
import numpy as NP
import plotly.graph_objects as GO
import plotly.figure_factory as FF
import django.db as DB

import app_proj.utility as UT
import movies.models.moviedb_helper as MH


class MasterMovie(DB.models.Model):
    Movie_ID = DB.models.IntegerField(unique=True)
    Title = DB.models.TextField()
    OriginalTitle = DB.models.TextField()
    Year = DB.models.TextField()
    Rating = DB.models.TextField(null=True)
    Companies = DB.models.TextField(null=True)
    Country = DB.models.TextField(null=True)
    Language = DB.models.TextField(null=True)
    RunTime = DB.models.IntegerField(null=True)
    Crew = DB.models.TextField(null=True)
    Cast = DB.models.TextField(null=True)
    Poster = DB.models.TextField(null=True)
    Genres = DB.models.TextField(null=True)
    #Collection = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.IntegerField(null=True)
    Gross = DB.models.IntegerField(null=True)
    ScoreImdb = DB.models.FloatField(null=True)
    VotesImdb = DB.models.IntegerField(null=True)
    Indeces = DB.models.TextField(null=True)


class MovieDB_Load(DB.models.Model):
    TmdbId = DB.models.IntegerField(unique=True, default=-1)
    Title = DB.models.TextField()
    OriginalTitle = DB.models.TextField()
    Year = DB.models.TextField()
    #Rating = DB.models.TextField()
    Companies = DB.models.TextField(null=True)
    Country = DB.models.TextField(null=True)
    Language = DB.models.TextField(null=True)
    RunTime = DB.models.FloatField(null=True)
    Crew = DB.models.TextField(null=True)
    Cast = DB.models.TextField(null=True)
    Poster = DB.models.TextField(null=True)
    Genres = DB.models.TextField(null=True)
    Collection = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.FloatField(null=True)
    Gross = DB.models.FloatField(null=True)
    Score = DB.models.TextField(null=True)
    Votes = DB.models.TextField(null=True)
    ImdbId = DB.models.TextField(null=True)


class Reelgood_Load(DB.models.Model):
    class Meta:
        unique_together = [['Title', 'Year']]
    #Reelgood_Id = DB.models.TextField()
    Title = DB.models.TextField()
    #OriginalTitle = DB.models.TextField()
    Year = DB.models.TextField()
    Rating = DB.models.TextField(null=True)
    #Companies = DB.models.TextField()
    Country = DB.models.TextField(null=True)
    #Language = DB.models.TextField()
    Duration = DB.models.FloatField(null=True)
    #Crew = DB.models.TextField()
    #Cast = DB.models.TextField()
    Poster = DB.models.TextField()
    Genres = DB.models.TextField(null=True)
    Tags = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField()
    #Budget = DB.models.IntegerField(default=0)
    #Gross = DB.models.IntegerField(default=0)
    ImdbScore = DB.models.FloatField(null=True)
    RtScore = DB.models.TextField(null=True)
    Services = DB.models.TextField()


class IMDB_Load(DB.models.Model):
    ImdbId = DB.models.TextField(unique=True, default='tt')
    Title = DB.models.TextField()
    OriginalTitle = DB.models.TextField(null=True)
    Year = DB.models.TextField()
    Rating = DB.models.TextField(null=True)
    Companies = DB.models.TextField(null=True)
    Country = DB.models.TextField(null=True)
    Language = DB.models.TextField(null=True)
    Duration = DB.models.IntegerField(null=True)
    Directors = DB.models.TextField(null=True)
    Writers = DB.models.TextField(null=True)
    Actors = DB.models.TextField(null=True)
    #Poster = DB.models.TextField()
    Genres = DB.models.TextField(null=True)
    #Collection = DB.models.TextField()
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.TextField(null=True)
    GrossUs = DB.models.TextField(null=True)
    GrossWorldwide = DB.models.TextField(null=True)
    Score = DB.models.FloatField(null=True)
    Votes = DB.models.IntegerField(null=True)


class StreamService(DB.models.Model):
    Movie_ID = DB.models.IntegerField()
    Service = DB.models.TextField()
    ServiceKey = DB.models.TextField()
    Active = DB.models.BooleanField()


class UserVotes(DB.models.Model):
    class Meta:
        unique_together = [['Movie_ID', 'User']]
    Movie_ID = DB.models.IntegerField()     # if not a foreign key, can reload master table
    User = DB.models.TextField()            # should be foreign key to user
    Vote = DB.models.IntegerField()


class UserRecommendations(DB.models.Model):
    class Meta:
        unique_together = [['Movie_FK', 'User']]
    Movie_FK = DB.models.ForeignKey(MasterMovie, on_delete=DB.models.CASCADE) 
    User = DB.models.TextField()            
    RecomLevel = DB.models.IntegerField()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASE CLASSES 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Editor(object):


    @staticmethod
    def DeleteTable(table_name):
        if table_name == 'MasterMovie' or table_name == 'All':
            MasterMovie.objects.all().delete()
        if table_name == 'MovieDB_Load' or table_name == 'All':
            MovieDB_Load.objects.all().delete()
        if table_name == 'Reelgood_Load' or table_name == 'All':
            Reelgood_Load.objects.all().delete()
        if table_name == 'IMDB_Load' or table_name == 'All':
            IMDB_Load.objects.all().delete()


    @staticmethod
    def InsertDictToTable(data_ls, table):
        # data_obj_ls = [MovieDB_Load(**r) for r in data_ls]
        # MovieDB_Load.objects.bulk_create(data_obj_ls)
        data_obj_ls = eval(f"[{table}(**r) for r in data_ls]")
        exec(f"{table}.objects.bulk_create(data_obj_ls, ignore_conflicts=True)")

        # for debugging input data
        # bulk insert is faster

        # for dt in data_ls:
        #     try:
        #         new_mv = IMDB_Load(**dt)
        #         new_mv.save()
        #     except Exception as ex:
        #         print(ex)
        #         print(dt)
        #         print('')
        #         continue


    @staticmethod
    def ToDBColumns(header_ls):
        new_ls = []
        for hdr in header_ls:
            new_col = hdr.replace('_', ' ').title().replace(' ', '')
            new_ls.append(new_col)
        return new_ls


    @staticmethod
    def CSVtoDict(file_path):
        
        if not os.path.isfile(file_path):
            raise Exception(f"CSV file not found: {file_path}")
        
        fhandle = open(file_path, 'r')
        reader = csv.reader(fhandle)
        header_ls = next(reader)            
        header_ls = Editor.ToDBColumns(header_ls)
        data_ls = []

        for row in reader:
            new_dx = {}
            for idx, col in enumerate(header_ls):
                try:
                    new_dx[col] = row[idx] if row[idx] else None
                except Exception as ex:
                    print(ex)
                    print(f'title: {row[0]} error-col: {col}')
                    print('')
                    break
            data_ls.append(new_dx)
  
        fhandle.close()
        return data_ls


    @staticmethod
    def RunMasterMovies():

        # apparently django ORM can only join tables if there is a foreign key relation
        # but these 3 tables are from disparate sources, the relation comes from outside of them
        # so use pandas to join, though it will be expensive to create copies of all 3 tables
        # pandas is better than sql because this join requires tokenizing the titles

        # create and join dataframes
        # joining imdb on id is better than on the token, though the token in 100% for tmdb and reelgood

        moviedb_df = PD.DataFrame(list(MovieDB_Load.objects.values()))
        reelgood_df = PD.DataFrame(list(Reelgood_Load.objects.values()))
        imdb_df = PD.DataFrame(list(IMDB_Load.objects.values()))

        def GetJoinToken(row):
            title = row['Title']
            year = row['Year']
            token = re.sub(r'[#,:"/=&¡!?\-\.\'\(\)\s]', '', title).lower()
            token = token[:12] if len(token) > 12 else token
            token = f'{token}_{year}'
            return token

        moviedb_df['join_token'] = moviedb_df.apply(GetJoinToken, axis=1)
        reelgood_df['join_token'] = reelgood_df.apply(GetJoinToken, axis=1)
        #return moviedb_df[['Title', 'Year', 'join_token']]

        moviedb_df.columns = [f'{c}_tmdb' for c in moviedb_df.columns]
        reelgood_df.columns = [f'{c}_rlgd' for c in reelgood_df.columns]
        imdb_df.columns = [f'{c}_imdb' for c in imdb_df.columns]

        merge_df = PD.merge(moviedb_df, reelgood_df, how='left', left_on='join_token_tmdb', right_on='join_token_rlgd')
        merge_df = PD.merge(merge_df, imdb_df, how='left', left_on='ImdbId_tmdb', right_on='ImdbId_imdb')
        merge_df = merge_df.drop(columns=['id_tmdb', 'Collection_tmdb', 'ImdbId_tmdb', 'join_token_tmdb',
                    'id_rlgd', 'Tags_rlgd', 'join_token_rlgd', 'id_imdb', 'GrossUs_imdb'])
        #return merge_df

        master_ls = []
        for idx, row in merge_df.iterrows():
            master_dx = Editor.GetMasterMovie(row)
            master_ls.append(master_dx)

        return master_ls


    @staticmethod
    def GetMasterMovie(row):
        
        def best_rating(row):
            rlgd_raw = row['Rating_rlgd']
            imdb_raw = row['Rating_imdb']
            rlgd = 0
            imdb = 0

            if rlgd_raw in ['18+ (R)', '16+']: rlgd = 4
            if rlgd_raw == '13+ (PG-13)': rlgd = 3
            if rlgd_raw == '7+ (PG)': rlgd = 2
            if rlgd_raw == 'All (G)': rlgd = 1
            
            if imdb_raw in ['R', 'TV-MA']: imdb = 4
            if imdb_raw in ['PG-13', 'PG', 'TV-14', 'TV-PG', 'GP']: imdb = 3
            if imdb_raw in ['TV-Y7']: imdb = 2
            if imdb_raw in ['G', 'TV-G']: imdb = 1
            if imdb_raw in ['Not Rated', 'Unrated', 'Approved', 'Passed']: imdb = 0

            final = max([rlgd, imdb])

            if final == 4: return 'R'
            if final == 3: return 'PG-13'
            if final == 2: return 'PG'
            if final == 1: return 'G'
            return None

        def best_companies(row):
            tmdb = row['Companies_tmdb']
            imdb = row['Companies_imdb']

            companies = None
            if tmdb and type(tmdb)==str: companies = tmdb
            elif imdb and type(imdb)==str: companies = imdb

            # 'The' in company name is problematic for analysis - remove them all

            if companies is None or type(companies)==float:
                return None

            companies = re.sub(r', The$', '', companies)
            companies = companies.replace(', The ', ', ').replace('The ', ' ')
            companies = companies.replace(', Ltd.', '').replace(', Inc.', '')
            companies = companies.replace('Asylum', 'The Asylum')

            companies = companies.replace('Lions Gate Films', 'Lionsgate')
            companies = companies.replace('Star Cinema – ABS-CBN Film Productions', 'ABS-CBN Films')
            companies = companies.replace('HBO Films', 'HBO').replace('HBO', 'HBO Films')
            companies = companies.replace('BBC Films', 'BBC').replace('BBC', 'BBC Films')
            companies = re.sub(r'\([^)]*\)', '', companies).strip()

            return companies

        def best_country(row):
            # this one is tied between IMDB and TMDB
            tmdb = row['Country_tmdb']
            rlgd = row['Country_rlgd']
            imdb = row['Country_imdb']

            if imdb: return imdb
            if tmdb: return tmdb
            return None

        def best_runtime(row):
            tmdb_raw = row['RunTime_tmdb']
            rlgd_raw = row['Duration_rlgd']
            imdb_raw = row['Duration_imdb']

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: rlgd = int(rlgd_raw)
            except: rlgd = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0
            
            rt_max = max([tmdb, rlgd, imdb])
            if rt_max: return rt_max
            return None

        def best_crew(row):
            tmdb = row['Crew_tmdb'] 
            imdb1 = row['Directors_imdb'] 
            imdb2 = row['Writers_imdb'] 

            crew_full_ls = tmdb.split(', ') if type(tmdb)==str else []
            crew_full_ls += imdb1.split(', ') if type(imdb1)==str else []
            crew_full_ls += imdb2.split(', ') if type(imdb2)==str else []
            
            series = PD.Series(crew_full_ls)
            counts = series.value_counts()
            crew_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    crew_ls.append(idx)
            return ', '.join(crew_ls) if len(crew_ls) >= 1 else None

        def best_cast(row):
            tmdb = row['Cast_tmdb']
            imdb = row['Actors_imdb']

            if tmdb and imdb == '':
                return tmdb
            if tmdb == '' and imdb:
                return imdb

            cast_full_ls = tmdb.split(', ') if type(tmdb)==str else []
            cast_full_ls += imdb.split(', ') if type(imdb)==str else []
            series = PD.Series(cast_full_ls)
            counts = series.value_counts()
            cast_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    cast_ls.append(idx)
            return ', '.join(cast_ls) if len(cast_ls) >= 1 else None

        def best_poster(row):
            # poster seem very similar from both sources, they are tall
            tmdb = row['Poster_tmdb'] or ''
            rlgd = row['Poster_rlgd'] or ''

            if tmdb: return tmdb
            if rlgd: return rlgd
            return None

        def best_genres(row):
            tmdb = row['Genres_tmdb']
            rlgd = row['Genres_rlgd']
            imdb = row['Genres_imdb']

            if type(tmdb)==float or tmdb is None: tmdb = ''
            if type(rlgd)==float or rlgd is None: rlgd = ''
            if type(imdb)==float or imdb is None: imdb = ''
            
            tmdb = tmdb.replace('Science Fiction', 'Sci-Fi')
            rlgd = rlgd.replace('Action & Adventure', 'Action, Adventure').replace('Science-Fiction', 'Sci-Fi').replace('Musical', 'Music')
            imdb = imdb.replace('Musical', 'Music')

            genre_full_ls = tmdb.split(', ') + rlgd.split(', ') + imdb.split(', ') 
            series = PD.Series(genre_full_ls)
            counts = series.value_counts()
            genre_ls = []
            for idx, val in counts.items():
                if val >= 2:
                    genre_ls.append(idx)
            return ', '.join(genre_ls) if len(genre_ls) >= 1 else None

        def best_synopsis(row):
            tmdb = row['Synopsis_tmdb'] 
            rlgd = row['Synopsis_rlgd'] 
            imdb = row['Synopsis_imdb'] 
            return rlgd

        def best_budget(row):
            tmdb_raw = row['Budget_tmdb'] 
            imdb_raw = row['Budget_imdb'] 

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0

            money_max = max([tmdb, imdb])
            if money_max: return money_max
            return None

        def best_gross(row):
            tmdb_raw = row['Gross_tmdb'] 
            imdb_raw = row['GrossWorldwide_imdb'] 

            try: tmdb = int(tmdb_raw)
            except: tmdb = 0

            try: imdb = int(imdb_raw)
            except: imdb = 0

            money_max = max([tmdb, imdb])
            if money_max: return money_max
            return None

        def aggregate_scores(row):
            # the number of votes on TMDb is 2 orders of magnitude less than IMDB
            # so just keep IMDB scores and votes
            pass

        def aggregate_indeces(row):
            index_dx = json.loads(row['Services_rlgd'])
            imdb_id = row['ImdbId_imdb']
            index_dx['imdb'] = imdb_id
            return json.dumps(index_dx)
            
        master_dx = {
            'Movie_ID': row['TmdbId_tmdb'],
            'Title': row['Title_tmdb'],
            'OriginalTitle': row['OriginalTitle_tmdb'],
            'Year': row['Year_tmdb'],
            'Rating': best_rating(row),
            'Companies': best_companies(row),
            'Country': best_country(row),
            'Language': row['Language_tmdb'],
            'RunTime': best_runtime(row),
            'Crew': best_crew(row),
            'Cast': best_cast(row),
            'Poster': best_poster(row),
            'Genres': best_genres(row),
            'Synopsis': best_synopsis(row),
            'Budget': best_budget(row),
            'Gross': best_gross(row),
            'ScoreImdb': float(row['Score_imdb']) if NP.isnan(row['Score_imdb'])==False else None,
            'VotesImdb': int(row['Votes_imdb']) if NP.isnan(row['Votes_imdb'])==False else None,
            'Indeces': aggregate_indeces(row),
        }

        return master_dx


    @staticmethod
    def CreateSyntheticVotes():
        
        import random as RD
        RD.seed(666)
        number_votes = 900
        UserVotes.objects.all().delete()

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


class Reporter(object):


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
    def ConvertToHistogramSeries(data_ls):
        """
        Takes a list of dictionaries with 2 items and converts them to 2 lists.
        """
        x_ls = []
        y_ls = []

        for dt in data_ls:
            x = dt[list(dt.keys())[0]]
            y = dt[list(dt.keys())[1]]

            x_ls.append(x)
            y_ls.append(y)
        
        return (x_ls, y_ls)


    @staticmethod
    def ConvertFigureToJson(figure):
        from plotly.utils import PlotlyJSONEncoder

        redata = json.loads(json.dumps(figure.data, cls=PlotlyJSONEncoder))
        relayout = json.loads(json.dumps(figure.layout, cls=PlotlyJSONEncoder))
        fig_json=json.dumps({'data': redata,'layout': relayout})

        return fig_json


    @staticmethod
    def GetDataHistory():
        history_ls = []
        tmdb_total = MovieDB_Load.objects.count()
        imdb_total = IMDB_Load.objects.count()
        reelgood_total = Reelgood_Load.objects.count() 
        master_total = MasterMovie.objects.count()

        new_dx = {
            'Column': 'Title',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Year',
            'TMDB': tmdb_total,
            'IMDB': imdb_total,
            'Reelgood': reelgood_total,
            'Union-All': master_total,

        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Rating',
            'TMDB': 0,
            'IMDB': IMDB_Load.objects.filter(Rating__isnull=False).
                    exclude(Rating__in=['Not Rated', 'Unrated', 'Approved', 'Passed']).count(),
            'Reelgood': Reelgood_Load.objects.filter(Rating__isnull=False).count(),
            'Union-All': MasterMovie.objects.filter(Rating__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Companies',
            'TMDB': MovieDB_Load.objects.filter(Companies__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Companies__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Companies__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Country',
            'TMDB': MovieDB_Load.objects.filter(Country__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Country__isnull=False).count(),
            'Reelgood': Reelgood_Load.objects.filter(Country__isnull=False).count(),
            'Union-All': MasterMovie.objects.filter(Country__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Language',
            'TMDB': MovieDB_Load.objects.filter(Language__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Language__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Language__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'RunTime',
            'TMDB': MovieDB_Load.objects.filter(RunTime__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Duration__isnull=False).count(),
            'Reelgood': Reelgood_Load.objects.filter(Duration__isnull=False).count(),
            'Union-All': MasterMovie.objects.filter(RunTime__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Crew*',
            'TMDB': MovieDB_Load.objects.filter(Crew__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Directors__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Crew__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Cast*',
            'TMDB': MovieDB_Load.objects.filter(Cast__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Actors__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Cast__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Genres*',
            'TMDB': MovieDB_Load.objects.filter(Genres__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Genres__isnull=False).count(),
            'Reelgood': Reelgood_Load.objects.filter(Genres__isnull=False).count(),
            'Union-All': MasterMovie.objects.filter(Genres__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Budget',
            'TMDB': MovieDB_Load.objects.filter(Budget__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(Budget__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Budget__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'Gross',
            'TMDB': MovieDB_Load.objects.filter(Gross__isnull=False).count(),
            'IMDB': IMDB_Load.objects.filter(GrossWorldwide__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(Gross__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'ImdbScore',
            'TMDB': 0,
            'IMDB': IMDB_Load.objects.filter(Score__isnull=False).count(),
            'Reelgood': 0,
            'Union-All': MasterMovie.objects.filter(ScoreImdb__isnull=False).count(),
        }
        history_ls.append(new_dx)

        new_dx = {
            'Column': 'StreamingId',
            'TMDB': 0,
            'IMDB': 0,
            'Reelgood': Reelgood_Load.objects.filter(Services__isnull=False).count(),
            'Union-All': MasterMovie.objects.filter(Indeces__isnull=False).count(),
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
    def RunVotePlot():
        vote_md_ls = Reporter.GetVoteCounts()
        vote_xy = Reporter.ConvertToHistogramSeries(vote_md_ls)
        figure = Reporter.GetVoteFigure(vote_xy)
        json = Reporter.ConvertFigureToJson(figure)
        return json


    @staticmethod
    def GetVoteCounts():
        vote_hist = list(   UserVotes.objects.all().values('Vote').
                            annotate(total=DB.models.Count('Vote')).
                            order_by('Vote') )
        return vote_hist


    @staticmethod
    def GetVoteFigure(vote_xy):

        fig = GO.Figure()
        fig.add_trace(
            GO.Bar(
                x= vote_xy[0],
                y= vote_xy[1],
                marker_color=['crimson', 'seagreen', 'gold']
            ))
        fig.update_layout(
            title="User Movie Votes",
            xaxis_title="Number of Stars",
            yaxis_title="Movie Count",
            width=500,
            height=400,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
        )
        fig.update_xaxes(tickvals=vote_xy[0])
        fig.update_yaxes(tickvals=list(range(0, 500, 100)))

        return fig


    @staticmethod
    def GetWatchedMovies():
        watched_ids = UserVotes.objects.all().values_list('Movie_ID', flat=True)
        movies_ls = MasterMovie.objects.filter(Movie_ID__in=watched_ids
                                        ).order_by('-ScoreImdb').values()

        # hack until FK is up 

        votes_ls = UserVotes.objects.all().values()
        for mov in movies_ls:
            for vt in votes_ls:
                if mov['Movie_ID'] == vt['Movie_ID']:
                    mov['Vote'] = vt['Vote']
                    break

        thumb_url = MH.MovieDBHelper.GetPosterThumbUrl()
        for mov in movies_ls:
            poster_url = mov['Poster']
            if 'http' not in poster_url:
                mov['Poster'] = f"{thumb_url}{poster_url}"

        return movies_ls


    @staticmethod
    def GetToWatchMovies():

        # select_related will load movies from db, which speeds up the function

        recom_ls = list(UserRecommendations.objects.filter(User='main')
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


    @staticmethod
    def GetTotalsPlot():

        # get the data
        # later must filter by active movies

        master_ls = list(MasterMovie.objects.values())
        year_distrib = {'netflix': [], 'amazon': [], 'hulu': []}

        for mov in master_ls:
            year = int(mov['Year'])
            index_dx = json.loads(mov['Indeces'])
            
            for key, val in index_dx.items():
                if key in year_distrib and year >= 1980:
                    year_distrib[key].append(year)

        # create the plot 

        fig = GO.Figure()
        fig.add_trace(GO.Histogram(x= year_distrib['amazon'], name='Amazon', marker_color='darkblue', opacity=0.6))
        fig.add_trace(GO.Histogram(x= year_distrib['netflix'], name='Netflix', marker_color='crimson', opacity=0.7))
        fig.add_trace(GO.Histogram(x= year_distrib['hulu'], name='Hulu', marker_color='green', opacity=0.8))
        fig.update_layout(
            title="Total Movie Count for Each Service",
            xaxis_title="Year",
            yaxis_title="Movie Count",
            width=700,
            height=500,
            margin=GO.layout.Margin(t=50, r=20, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
            barmode='overlay', 
        )

        # format and send to frontend

        return Reporter.ConvertFigureToJson(fig)


    @staticmethod
    def GetScoresPlot():

        # get the data
        # later must filter by active movies

        master_ls = list(MasterMovie.objects.values())
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
            width=700,
            height=500,
            margin=GO.layout.Margin(t=60, r=10, b=50, l=70, pad=0),
            paper_bgcolor="LightSteelBlue",
            barmode='overlay', 
            yaxis_tickformat = '%', 
        )
        fig.update_xaxes(tickvals=list(range(0, 10, 1)))
        
        # format and send to frontend

        return Reporter.ConvertFigureToJson(fig)

