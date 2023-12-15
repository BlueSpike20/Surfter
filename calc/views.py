from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
from googlesearch import search
import html
import requests
import logging
import openai
import time
import pika
from .models import SurftStatus
from bs4 import BeautifulSoup
from celery import shared_task
from .models import Article, Analysis
from celery.result import AsyncResult
from django.http import JsonResponse
from django.contrib import messages
from calc.tasks import SurftResults
from calc.tasks import CeleryTest
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here:

# Global variable to check if the process is running
is_running = False



def home(request):
    return render(request, 'home.html', {'name': 'Stranger'})
  
def surfting(request):
    
    if "queryprompt" in request.POST:
        queryprompt = str(request.POST["queryprompt"])
    else:
        # Handle the case where there's no "queryprompt" in the POST data
        # For example, you might want to set queryprompt to a default value
        queryprompt = "default value"

    if "num2" in request.POST:
        try:
            How_many_URLs_to_get = int(request.POST["num2"])
        except ValueError:
            # Handle the case where num2 is not a valid integer
            How_many_URLs_to_get = 3
    else:
        How_many_URLs_to_get = "default value"

    #messages.info(request, 'Past the queryprompt setting the surfting function')
    messages.info(request, f'queryprompt =  {queryprompt}, {How_many_URLs_to_get} deep')
    # Store queryprompt and How_many_URLs_to_get in the session
    request.session['queryprompt'] = queryprompt
    request.session['How_many_URLs_to_get'] = How_many_URLs_to_get
    
    # Get the task ID I hopefully passed in from the redirect
    dummy_surfter_task_id = request.POST.get('surfter_task_id', default=666)
    if dummy_surfter_task_id == 666:
        #task = SurftResults.delay(queryprompt, How_many_URLs_to_get)
        task = SurftResults.delay(queryprompt, How_many_URLs_to_get)
        surfter_task_id = task.id
        messages.info(request, f'queryprompt = {task.status}')

        messages.info(request, f'surfter_task_id has been promoted from 666 to: {task.id}')
    else:
        messages.info(request, f'surfter_task_id already exists as {surfter_task_id}')
    
    
    
    # if task.status == 'SUCCESS':
    #     messages.info(request, 'Task is done')
    #     messages.info(request, f'task.result = {task.result}')
    #     return render(request, 'results.html')

    #return render(request, 'surfting.html', {'task_id': task_id})
    time.sleep(1)
    messages.info(request, f'In the hard to understand surfting function')
    #return redirect('/surfting/?task_id=' + task_id)
    #return redirect('surfting', {'task_id': task_id})
    return render(request, 'surfting.html', {'surfter_task_id': surfter_task_id, 'queryprompt': queryprompt, 'How_many_URLs_to_get': How_many_URLs_to_get})

    #Redirect to check_task_status with surfter_task_id as a GET parameter
    # check_task_status_url = reverse('check_task_status') + '?surfter_task_id=' + str(surfter_task_id)
    # return HttpResponseRedirect(check_task_status_url)


def register(request):
    return render(request, 'accounts/register.html', {'name': 'BlueSpike'})

# def get_task_info(request):
#     task_id = request.GET.get('task_id', None)
#     if task_id is None:
#         return JsonResponse({'error': 'Task ID not provided'})

#     task = AsyncResult(task_id)
#     response_data = {
#         'task_status': task.status,
#         'task_result': task.result,
#     }
#     return JsonResponse(response_data)

def check_task_status(request):
    check_task_id = request.GET.get('surfter_task_id')
    if check_task_id is None:
        return JsonResponse({'error': 'Missing task_id parameter'})

    task = AsyncResult(check_task_id)
    response = {
        'task_status': task.status,
        'task_result': str(task.result),  # Convert task.result to a string
        'task_id' : task.id,
    }

    return JsonResponse(response)  # Return the response as a JsonResponse

def results(request):
    queryprompt = request.session.get('queryprompt', 'default value')
    How_many_URLs_to_get = request.session.get('How_many_URLs_to_get', 'default value')
    article_collection = Article.objects.filter(query=queryprompt)
    return render(request, 'results.html', {'articlecollection': article_collection, 'queryprompt': queryprompt, 'How_many_URLs_to_get': How_many_URLs_to_get})