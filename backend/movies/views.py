"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
FILMOPHILE VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from rest_framework.decorators import api_view
from rest_framework.response import Response

import app_proj.utility as UT
import movies.models.models as MM
import movies.models.analysis as NL


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

    