"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIES VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from rest_framework.decorators import api_view
from rest_framework.response import Response
import app_proj.utility as UT
import movies.models.data_manager as DM
import movies.models.exploration as XT


# EXPLORATION PAGE 

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


# ADMIN PAGE

@api_view(["GET"])
def TableCounts(request):
    result_dx = DM.Reporter.GetTableCounts()
    return Response(result_dx)

@api_view(["GET"])
def DeleteTables(request):
    DM.Editor.DeleteTable('All')
    return Response()

@api_view(["GET"])
def LoadCsvs(request):
    DM.Editor.LoadBaseCsvs()
    return Response()

@api_view(["GET"])
def MasterMovies(request):
    master_ls = DM.Editor.RunMasterMovies()
    DM.Editor.InsertDictToTable(master_ls, 'MasterMovie')
    return Response()


# extract data 


@api_view(["GET"])
def ExtractMovieDb(request):

    print("ExtractMovieDb")
    # join websocket group ?



    return Response()

@api_view(["GET"])
def ExtractReelgood(request):

    print("ExtractReelgood")
    # join websocket group ?



    return Response()

@api_view(["GET"])
def ExtractImdb(request):

    print("ExtractImdb")
    # join websocket group ?



    return Response()
