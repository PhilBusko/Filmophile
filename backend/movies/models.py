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
    #Studio = models.TextField()
    #Country = models.TextField()
    Director = models.TextField()
    Actor1 = models.TextField()
    Actor2 = models.TextField()
    Actor3 = models.TextField()
    #Budget = models.IntegerField(default=0)
    #GrossDomestic = models.IntegerField(default=0)
    #GrossForeign = models.IntegerField(default=0)


class StreamService(models.Model):
    Movie_ID = models.IntegerField(default=0)
    ServiceName = models.IntegerField(default=0)
    Movie_Service_ID = models.IntegerField(default=0)
    IsActive = models.BooleanField(default=False)
    Genre1 = models.TextField()
    Genre2 = models.TextField()
    Genre3 = models.TextField()
    Keywords = models.TextField()
    Synopsis = models.TextField()


class InfoService(models.Model):
    Movie_ID = models.IntegerField(default=0)
    ServiceName = models.IntegerField(default=0)
    Movie_Service_ID = models.IntegerField(default=0)
    Score = models.IntegerField(default=0)
    ScoreVotes = models.IntegerField(default=0)
    Genre1 = models.TextField()
    Genre2 = models.TextField()
    Genre3 = models.TextField()
    Synopsis = models.TextField()


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
DATABASE CLASSES 
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Reporter(object):


   @staticmethod
   def GetTableSummary():

       pass
