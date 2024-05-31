from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from . import webScraber


@api_view(['POST'])
@csrf_exempt
def scrapdata(request):
    data = request.data
    url = data['data']
    print("URL:", url)
    return JsonResponse({'prediction': 'success'}, status=status.HTTP_200_OK)