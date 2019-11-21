"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
GAME-RULES VIEWS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from rest_framework.decorators import api_view
from rest_framework.response import Response

import app_proj.utility as UT
import game_rules.models as GM


@api_view(["GET"])
def TableSummary(request):
   result_dx = GM.Reporter.GetTableSummary()
   return Response(result_dx)

@api_view(["POST"])
def LoadGameRules(request):
   GM.Editor.DeleteAll()
   GM.Editor.LoadGameRules()
   result_dx = GM.Reporter.GetTableSummary()
   return Response(result_dx)


@api_view(["GET"])
def RuleBooksPath(request):
   result_dx = GM.Reporter.RuleBooksPath()
   return Response(result_dx)

@api_view(["POST"])
def CreateRuleBooks(request):
   #UT.prog_lg.debug('GV.CreateRuleBooks')
   GM.PdfMaker.CreateRuleBookPDF()
   result_dx = GM.Reporter.RuleBooksPath()
   return Response(result_dx)

@api_view(["GET"])
def TestPDF(request):
   result_dx = GM.PdfMaker.CreateFontTest()
   return Response(result_dx)
