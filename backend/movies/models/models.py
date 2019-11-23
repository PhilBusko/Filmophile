"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os, csv
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
        
