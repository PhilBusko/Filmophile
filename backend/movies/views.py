"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILMOPHILE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from rest_framework.decorators import api_view
from rest_framework.response import Response

import app_proj.utility as UT
import movies.models.models as MM
import movies.models.analysis as NL


# general views

@api_view(["GET"])
def Genres(request):
   result_ls = MM.Reporter.GetGenres()
   return Response(result_ls)

@api_view(["GET"])
def RecomLevels(request):
   result_ls = MM.Reporter.GetRecomLevels()
   return Response(result_ls)


# statistics page 

@api_view(["GET"])
def TotalsPlot(request):
    json_tx = MM.Reporter.GetTotalsPlot()
    return Response(json_tx)

@api_view(["GET"])
def ScoresPlot(request):
    json_tx = MM.Reporter.GetScoresPlot()
    return Response(json_tx)


# data science page

@api_view(["GET"])
def DataHistory(request):
   result_dx = MM.Reporter.GetDataHistory()
   return Response(result_dx)

@api_view(["GET"])
def VotePlot(request):
    json_tx = MM.Reporter.RunVotePlot()
    return Response(json_tx)

@api_view(["GET"])
def AnalysisLogReg(request):
    json_tx = NL.LogisticRegression.GetHardcodedFigure()
    return Response(json_tx)


# browsing pages

@api_view(["GET"])
def MoviesWatched(request):
    movies_ls = MM.Reporter.GetWatchedMovies()
    return Response(movies_ls)

@api_view(["GET"])
def MoviesToWatch(request):
    movies_ls = MM.Reporter.GetToWatchMovies()
    return Response(movies_ls)

