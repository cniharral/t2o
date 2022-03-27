from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.db import models
from django.core import serializers
from django.conf import settings
#from django.utils import simplejson
#import json as simplejson
from django.template import Context, loader
from django.core.files import File
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from blockchain.blockchain import Blockchain_L3
import io
import pprint

api_token = "e3b35a91-ec09-40b1-a2ef-f09f66e1f8d7"

@csrf_exempt
def get_info (request):
    """
    """

    return render( request, 'get_info.html', context={}, )


@csrf_exempt
def index (request):
    """
    """

    return render( request, 'index.html', context={}, )

@csrf_exempt
def get_stats_general (request):
    """
    """

    crypto = request.GET.get('crypto')
    realmoney = request.GET.get('realmoney')

    bc = Blockchain_L3(api_token)
    bc.get_info(crypto, realmoney)
    stats = bc.get_stats_general()

    return JsonResponse(stats)

@csrf_exempt
def get_stats_bids (request):
    """
    """

    crypto = request.GET.get('crypto')
    realmoney = request.GET.get('realmoney')

    bc = Blockchain_L3(api_token)
    bc.get_info(crypto, realmoney)
    stats = bc.get_stats_bids_asks("bids")

    return JsonResponse(stats)

@csrf_exempt
def get_stats_asks (request):
    """
    """

    crypto = request.GET.get('crypto')
    realmoney = request.GET.get('realmoney')

    bc = Blockchain_L3(api_token)
    bc.get_info(crypto, realmoney)
    stats = bc.get_stats_bids_asks("asks")

    return JsonResponse(stats)

