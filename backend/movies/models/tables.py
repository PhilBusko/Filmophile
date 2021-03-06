"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIE MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import django.db as DB


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
    Keywords = DB.models.TextField(null=True)
    Synopsis = DB.models.TextField(null=True)
    Budget = DB.models.IntegerField(null=True)
    Gross = DB.models.IntegerField(null=True)
    ScoreImdb = DB.models.FloatField(null=True)
    VotesImdb = DB.models.IntegerField(null=True)
    Indeces = DB.models.TextField(null=True)

class StreamService(DB.models.Model):
    Movie_ID = DB.models.IntegerField()
    Service = DB.models.TextField()
    ServiceKey = DB.models.TextField()
    Active = DB.models.BooleanField()


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

