"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILMOPHILE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from rest_framework.decorators import api_view
from rest_framework.response import Response

import app_proj.utility as UT
import movies.models.data_manager as DM
import movies.models.exploration as XT
import movies.models.analysis as NL


# browsing pages

@api_view(["GET"])
def Genres(request):
    result_ls = DM.Reporter.GetGenres()
    return Response(result_ls)

@api_view(["GET"])
def RecomLevels(request):
   result_ls = DM.Reporter.GetRecomLevels()
   return Response(result_ls)

@api_view(["GET"])
def MoviesWatched(request):
    movies_ls = DM.Reporter.GetWatchedMovies()
    return Response(movies_ls)

@api_view(["GET"])
def MoviesToWatch(request):
    movies_ls = DM.Reporter.GetToWatchMovies()
    return Response(movies_ls)


# exploration page 

@api_view(["GET"])
def YearPlot(request):
    json_ls = XT.Explore.GetYearPlot()
    return Response(json_ls)

@api_view(["GET"])
def CountriesPlot(request):
    json_ls = XT.Explore.GetCountriesPlot()
    return Response(json_ls)

@api_view(["GET"])
def GenresPlot(request):
    json_ls = XT.Explore.GetGenresPlot()
    return Response(json_ls)

@api_view(["GET"])
def GenresMoviePlot(request):
    json_ls = XT.Explore.GetGenresMoviePlot()
    return Response(json_ls)

@api_view(["GET"])
def RoiPlot(request):
    json_ls = XT.Explore.GetRoiPlot()
    return Response(json_ls)

@api_view(["GET"])
def ScoreProfitPlot(request):
    json_ls = XT.Explore.GetScoreProfitPlot()
    return Response(json_ls)

@api_view(["GET"])
def TotalsPlot(request):
    json_ls = XT.Explore.GetTotalsPlot()
    return Response(json_ls)

@api_view(["GET"])
def ScoresPlot(request):
    json_ls = XT.Explore.GetScoresPlot()
    return Response(json_ls)


# data science page

@api_view(["GET"])
def DataHistory(request):
   result_dx = DM.Reporter.GetDataHistory()
   return Response(result_dx)

@api_view(["GET"])
def VotePlot(request):
    json_tx = DM.Reporter.RunVotePlot()
    return Response(json_tx)

@api_view(["GET"])
def RestrictedClassifiers(request):
    json_tx = NL.FeatureEngineer.GetRestrictedClassifiers()
    return Response(json_tx)

