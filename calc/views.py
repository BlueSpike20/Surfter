from django.shortcuts import render
from django.core.management import call_command
from django.http import HttpResponse
from .models import Article
from .models import Analysis
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

# Create your views here:

# Global variable to check if the process is running
is_running = False



def home(request):
    return render(request, 'home.html', {'name': 'Stranger'})
  
def surfting(request):
    data = request.POST.dict()
    print(data)
    messages.info(request, 'In the surfting function')
    task = SurftResults.delay(data)
    return render(request, 'surfting.html', {'task_id': task.id})


def register(request):
    return render(request, 'accounts/register.html', {'name': 'BlueSpike'})

def GetArray(query, num_results):
    results = []
    # Perform the search
    for result in search(query, num_results):
        results.append(result)
    return results
    print(results)

def get_task_info(request):
    task_id = request.GET.get('task_id', None)
    if task_id is None:
        return JsonResponse({'error': 'Task ID not provided'})

    task = AsyncResult(task_id)
    response_data = {
        'task_status': task.status,
        'task_result': task.result,
    }
    return JsonResponse(response_data)

@shared_task
### This is the meat of Surfter ###
def SurftResults(request):
    is_running = True
    messages.info(request, 'Starting SurftResults')

    # Will this run cost money and use ChatGPT?
    SpendMoney = False

    # Am I in trouble with google?
    GoogleTrouble = True

    # Define your prompt to ChatGPT
    FrontOfPrompt = "Please analyze the following article for tone, accuracy, bias, and motivation, then summarize everything into a no more than 50 word response: " 

    # Set up OpenAI API credentials
    #OpenAi.api_key = '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'
    
    #upon the user's post on the homepage the following data is captured and used:
    queryprompt = str(request.POST["queryprompt"])
    How_many_URLs_to_get = int(request.POST["num2"])

    analysis = Analysis(query = queryprompt)
    analysis.save()


     
    #Have the ability to turn off reliance on google to continue dev:
    if GoogleTrouble == True:
       TroubledURLsGotten = ["https://en.wikipedia.org/wiki/Internet_censorship_in_the_United_States"] * How_many_URLs_to_get

    else:
        #Get the raw URLs from GoogleSearcher.GetArray to be Surfted
        URLsGotten = GetArray(queryprompt, How_many_URLs_to_get * 2)

    GoodURLs = []
    
    #Check to see if I'm in trouble...
    if GoogleTrouble:
        GoodURLs = TroubledURLsGotten
        
    else:
        #Go through URLsGotten and get good ones back
        for i, url in enumerate(URLsGotten):
            #logging.debug("===About to run good_url===")
            good_url = discern_good_url(url, i)
            #logging.debug("===About to append to GoodURLs===")

            if good_url and good_url not in GoodURLs:
                GoodURLs.append(good_url)

    # Create an empty list to store Article objects
    ArticleCollection = []
    
    # Iterate through URLs and create article objects before pumping data into them:
    for i, url in enumerate(GoodURLs):
        # For now, let's assume you have some dummy text and PIC_Array for each article
        dummyText = "Placeholder article text"
        #process_url_into_image_url(ArticleCollection[i], i)
        #dummy_pic_array = [f"pic_url_{j}" for j in range(len(GoodURLs))] # Just a dummy list of pic URLs
        dummy_aitext = f"Compwizdom for article {i+1}"
        
        # Create an Article object
        article = Article(query = queryprompt, URL = url, Text = dummyText, AItext = dummy_aitext, QualityArticle = False)
        article.save()
        
        # Add the article to the collection
        ArticleCollection.append(article)
        #logging.info(f"article {i}'s URL is: {ArticleCollection[i].URL}")

        processedtext = process_url_into_text(url, i, ArticleCollection)
        # print("=   LOTS OF TEXT INCOMING  =")
        # print("==  --------------------  ==")
        # print(processedtext)
        # print("== That was a lot of text! ==")
        # print("=   --------------------    =")
        

        if processedtext is not None:
            #TODO Surface this value for clipping the huge articles
            processedtext[:1000] 
            article.save()
        else:
            # Handle the case where processedtext is None
            print(f"Skipping article {i+1} due to None processedtext")
            logging.debug(f"Skipping article {i+1} due to None processedtext")
        

        if is_this_url_a_dupe(url, ArticleCollection):
            pass
        else:
            # Fetch the existing article from the collection
            article = ArticleCollection[i]

            # Generate AI text response
            ai_text_response = generate_response(FrontOfPrompt + article.Text)

            # Update the AItext field
            if ai_text_response is not None:
                article.AItext = ai_text_response
            else:
                article.AItext = "Default AI text or any appropriate handling"
        
            print("=   LOTS OF TEXT INCOMING  =")
            print("==  --------------------  ==")
            print(ai_text_response)
            print("== That was a lot of text! ==")
            print("=   --------------------    =")
            
            article.save()
            
            # Assuming taskId is defined somewhere
            taskId = "your-task-id"

            response = requests.post('/get_task_info/', data={'task_id': taskId})

            # Ensure the request was successful
            if response.status_code == 200:
                data = response.json()
                if data['task_status'] == 'SUCCESS':
                    # Do something here
                    pass

            return JsonResponse({'status': 'done'})

    context = {'query': queryprompt, 'depth': How_many_URLs_to_get, 'goodurls':GoodURLs, 'articlecollection': ArticleCollection}
    return render(request, 'results.html', context)

#Turns the paragragh text at the given URL into readable text.
def use_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all paragraph tags in the soup
    paragraphs = soup.find_all('p')
        
    # Extract text from each paragraph and concatenate
    paragraph_text = ""
    for paragraph in paragraphs:
        paragraph_text += paragraph.get_text() + " "

    return paragraph_text.strip()

def use_soup_with_timeout(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
            print(f"Warning: {url} returned status code {response.status_code}")
            response.raise_for_status()  # Raise an exception for other errors (e.g., network issues)
            pass
        return use_soup(url)
        
    except requests.exceptions.Timeout:
        print(f"Timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None
    
def process_url_into_text(url, i, ArticleCollection):
    soup = use_soup_with_timeout(url)
    if soup:
        ArticleCollection[i].Text = soup
        
        time.sleep(1)
        
        return soup
    else:
        ArticleCollection[i].Text = f" :( See Failure for {url} in log..."
        return None

def discern_good_url(url, timeout=2):
    try:
        if timeout <= 0:
            timeout = 0.1  # Set a minimum positive value for timeout
    
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
            print(f"Warning: {url} returned status code {response.status_code}")
            response.raise_for_status()  # Raise an exception for other errors (e.g., network issues)
            #logging.info(f"Warning: {url} returned status code {response.status_code}")
            return None
        return url
        
    except requests.exceptions.Timeout:
        print(f"Timeout while accessing {url}")
        #logging.info(f"Timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        #logging.info(f"Error accessing {url}: {e}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        #logging.info(f"ValueError: {ve}")
        return None
    
def generate_response(combinedprompt):
    openai.api_key = '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'
    #client = openai(api_key=api_key)

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "You are a helpful assistant with the subtle personality of an enlightned and wise surfer."},
            {"role": "user", "content": "I would you you to summarize the following article and comment using your personality: "},
            {"role": "assistant", "content": "Fo' sho"},
            {"role": "user", "content": "And please limit your total response to 50 words"},
            {"role": "user", "content": combinedprompt},
        ],
    )

    #print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def is_this_url_a_dupe(url, ArticleCollection):
    # Fetch all articles from the database
    #TODO This seems grossly unoptimized. How to improve?
    all_articles = Article.objects.all()

    for i, article in enumerate(all_articles):
        
        # Check if the URL already exists in the database
        URL_exists_in_database = any(other_article.URL == article.URL for other_article in all_articles if other_article.id != article.id)

        if URL_exists_in_database:
            
            # Check if the URL exists in the current ArticleCollection
            URL_exists_in_collection = any(other_article.URL == article.URL for other_article in ArticleCollection)

            if URL_exists_in_collection:
                return True  # query is a duplicate in both the database and the current ArticleCollection

    return False  # query is not a duplicate