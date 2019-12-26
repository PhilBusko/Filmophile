"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILMOPHILE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from rest_framework.decorators import api_view
from rest_framework.response import Response
import app_proj.utility as UT
import movies.models.data_manager as DM
import movies.models.exploration as XT


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


# admin page

@api_view(["GET"])
def TableCounts(request):
   result_dx = DM.Reporter.GetTableCounts()
   return Response(result_dx)

