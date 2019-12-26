"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILMOPHILE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from rest_framework.decorators import api_view
from rest_framework.response import Response
import app_proj.utility as UT
import recommend.models.analysis as NL


# browsing pages

@api_view(["GET"])
def Genres(request):
    result_ls = NL.General.GetGenres()
    return Response(result_ls)

@api_view(["GET"])
def RecomLevels(request):
    result_ls = NL.General.GetRecomLevels()
    return Response(result_ls)

@api_view(["GET"])
def MoviesWatched(request):
    movies_ls = NL.General.GetWatchedMovies()
    return Response(movies_ls)

@api_view(["GET"])
def MoviesToWatch(request):
    movies_ls = NL.General.GetToWatchMovies()
    return Response(movies_ls)


# data science page

@api_view(["GET"])
def DataHistory(request):
   result_dx = NL.General.GetDataHistory()
   return Response(result_dx)

@api_view(["GET"])
def ScorePlot(request):
    json_tx = NL.General.GetSyntheticScores()
    return Response(json_tx)

@api_view(["GET"])
def RestrictedClassifiers(request):
    json_tx = NL.General.GetRestrictedClassifiers()
    return Response(json_tx)


# admin page

@api_view(["GET"])
def TableCounts(request):
   result_dx = DM.Reporter.GetTableCounts()
   return Response(result_dx)

