"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
RECOMMENDATION MODELS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import django.db as DB
import movies.models.tables as MT


class UserScores(DB.models.Model):
    class Meta:
        unique_together = [['Movie_ID', 'User']]
    Movie_ID = DB.models.IntegerField()     # if not a foreign key, can reload master table
    User = DB.models.TextField()            # should be foreign key to user
    Score = DB.models.IntegerField()


class UserRecommendations(DB.models.Model):
    class Meta:
        unique_together = [['Movie_FK', 'User']]
    Movie_FK = DB.models.ForeignKey(MT.MasterMovie, on_delete=DB.models.CASCADE) 
    User = DB.models.TextField()            
    RecomLevel = DB.models.IntegerField()

