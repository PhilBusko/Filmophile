"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import os
from django.db import models
import app_proj.utility as UT


class Movie(models.Model):
    Movie_ID = models.IntegerField(default=0)
    Title = models.TextField()
    OriginalTitle = models.TextField()
    Year = models.TextField()
    Rating = models.TextField()
    Companies = models.TextField()
    Country = models.TextField()
    Language = models.TextField()
    RunTime = models.IntegerField(default=0)
    Crew = models.TextField()
    Cast = models.TextField()
    Poster = models.TextField()
    Genres = models.TextField()
    Collection = models.TextField()
    Synopsis = models.TextField()
    Budget = models.IntegerField(default=0)
    Gross = models.IntegerField(default=0)
    Scores = models.TextField()
    Indeces = models.TextField()


class MovieDB_Load(models.Model):
    Movie_ID = models.IntegerField(default=0)
    Title = models.TextField()
    OriginalTitle = models.TextField()
    Year = models.TextField()
    #Rating = models.TextField()
    Companies = models.TextField()
    Country = models.TextField()
    Language = models.TextField()
    RunTime = models.IntegerField(default=0)
    Crew = models.TextField()
    Cast = models.TextField()
    Poster = models.TextField()
    Genres = models.TextField()
    Collection = models.TextField()
    Synopsis = models.TextField()
    Budget = models.IntegerField(default=0)
    Gross = models.IntegerField(default=0)
    Score = models.TextField()
    Votes = models.TextField()
    ImdbID = models.TextField()


class Reelgood_Load(models.Model):
    Reelgood_ID = models.TextField()
    Title = models.TextField()
    #OriginalTitle = models.TextField()
    Year = models.TextField()
    Rating = models.TextField()
    #Companies = models.TextField()
    Country = models.TextField()
    #Language = models.TextField()
    RunTime = models.IntegerField(default=0)
    #Crew = models.TextField()
    #Cast = models.TextField()
    Poster = models.TextField()
    Genres = models.TextField()
    Tags = models.TextField()
    Synopsis = models.TextField()
    #Budget = models.IntegerField(default=0)
    #Gross = models.IntegerField(default=0)
    ImdbScore = models.FloatField(default=0)
    RTScore = models.IntegerField(default=0)
    Services = models.TextField()


class IMDB_Load(models.Model):
    Imdb_ID = models.IntegerField(default=0)
    Title = models.TextField()
    OriginalTitle = models.TextField()
    Year = models.TextField()
    Rating = models.TextField()
    Companies = models.TextField()
    Country = models.TextField()
    Language = models.TextField()
    RunTime = models.IntegerField(default=0)
    Crew = models.TextField()
    Cast = models.TextField()
    #Poster = models.TextField()
    Genres = models.TextField()
    #Collection = models.TextField()
    Synopsis = models.TextField()
    Budget = models.IntegerField(default=0)
    Gross_US = models.IntegerField(default=0)
    Gross = models.IntegerField(default=0)
    Score = models.FloatField()
    Votes = models.IntegerField(default=0)


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
    def InsertMovieDB(movie_ls):

        # player_m, created = FT.Player.objects.get_or_create(
        #     FirstName = firstName, LastName = lastName,
        #     Nationality = nation, DateOfBirth = dob,
        # )
        
        # # insert player squad data 
        
        # club_m = FT.Club.objects.get(Club=squadClub)
        # plClub_m, created = FT.PlayerInClub.objects.get_or_create(
        #     SeasonFK = season_m, ClubFK = club_m,
        #     PlayerFK = player_m, PositionDef = posDef, ShirtNo = shirt, 
        # )

        pass


    @staticmethod
    def CSVtoDict(file_path):
        
        if not os.path.isfile(file_path):
            raise Exception(f"CSV file not found: {file_path}")
        
        with open(inputPath) as fhandle:
            reader = csv.reader(fhandle)
            next(reader)  # skip header row
            
            for row in reader:
                
                season = row[0]
                squadClub = row[1]
                firstName = row[2]
                lastName = row[3]
                nation = row[4]
                dob = row[5]
                posDef = row[6]
                shirt = row[7]
                
        
