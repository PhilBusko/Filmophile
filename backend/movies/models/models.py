"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, csv, re
import pandas as PD
import django.db as DB
import app_proj.utility as UT


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
    Collection = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.IntegerField(null=True)
    Gross = DB.models.IntegerField(null=True)
    Scores = DB.models.TextField(null=True)
    Indeces = DB.models.TextField(null=True)


class MovieDB_Load(DB.models.Model):
    TmdbId = DB.models.IntegerField(unique=True)
    Title = DB.models.TextField()
    OriginalTitle = DB.models.TextField()
    Year = DB.models.TextField()
    #Rating = DB.models.TextField()
    Companies = DB.models.TextField(null=True)
    Country = DB.models.TextField(null=True)
    Language = DB.models.TextField()
    RunTime = DB.models.FloatField(null=True)
    Crew = DB.models.TextField(null=True)
    Cast = DB.models.TextField(null=True)
    Poster = DB.models.TextField(null=True)
    Genres = DB.models.TextField(null=True)
    Collection = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.FloatField(null=True)
    Gross = DB.models.FloatField(null=True)
    Score = DB.models.TextField()
    Votes = DB.models.TextField()
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
    ImdbId = DB.models.TextField(unique=True)
    Title = DB.models.TextField()
    OriginalTitle = DB.models.TextField(null=True)
    Year = DB.models.TextField()
    Rating = DB.models.TextField(null=True)
    Companies = DB.models.TextField(null=True)
    Country = DB.models.TextField(null=True)
    Language = DB.models.TextField(null=True)
    Duration = DB.models.FloatField(null=True)
    Directors = DB.models.TextField()
    Writers = DB.models.TextField(null=True)
    Actors = DB.models.TextField(null=True)
    #Poster = DB.models.TextField()
    Genres = DB.models.TextField()
    #Collection = DB.models.TextField()
    Synopsis = DB.models.TextField()
    Budget = DB.models.TextField(null=True)
    GrossUs = DB.models.IntegerField(null=True)
    GrossWorldwide = DB.models.IntegerField(null=True)
    Score = DB.models.FloatField(null=True)
    Votes = DB.models.IntegerField(null=True)


class StreamService(DB.models.Model):
    Movie_ID = DB.models.IntegerField()
    Service = DB.models.TextField()
    ServiceKey = DB.models.TextField()
    Active = DB.models.BooleanField()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASE CLASSES 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


class Editor(object):


    @staticmethod
    def DeleteTable(table_name):
        if table_name == 'Movie' or table_name == 'All':
            Movie.objects.all().delete()
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
                new_dx[col] = row[idx] if row[idx] else None
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
        return merge_df

        master_ls = []
        for idx, row in merge_df.iterrows():
            master_dx = Editor.GetMasterMovie(row)
            master_ls.append(master_dx)

        return master_ls

    
    @staticmethod
    def GetMasterMovie(row):
        
        def function(row):
            return None




        master_dx = {
            'Movie_ID': row['TmdbId_tmdb'],
            'Title': row['Title_tmdb'],
            'OriginalTitle': row['OriginalTitle_tmdb'],
            'Year': row['Year_tmdb'],
            'Rating': function(row),
            'Companies': function(row),
            'Country': function(row),
            'Language': row['Language_tmdb'],
            'RunTime': function(row),
            'Crew': function(row),
            'Cast': function(row),
            'Poster': function(row),
            'Genres': function(row),
            'Collection': function(row),
            'Synopsis': function(row),
            'Budget': function(row),
            'Gross': function(row),
            'Scores': function(row),
            'Indeces': function(row),
        }

        return master_dx

