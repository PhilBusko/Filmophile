"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
RECOMMENDATION VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from rest_framework.decorators import api_view
from rest_framework.response import Response
import app_proj.utility as UT
import recommend.models.analysis as NL


# BROWSING PAGES

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


# DATA SCIENCE PAGE

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


# ADMIN PAGE

@api_view(["GET"])
def TableCounts(request):
    result_dx = NL.General.GetTableCounts()
    return Response(result_dx)

@api_view(["GET"])
def DeleteTables(request):
    NL.General.DeleteTable('All')
    return Response()

# recommendations

@api_view(["GET"])
def SyntheticScores(request):
    NL.FeatureEngineer.CreateSyntheticVotes()
    return Response()

@api_view(["GET"])
def FeaturesFile(request):
    NL.FeatureEngineer.RunFeatures()
    return Response()

@api_view(["GET"])
def TrainPredict(request):
    NL.SvmClassifier.RunRecommendations()
    return Response()

