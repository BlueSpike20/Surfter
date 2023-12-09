from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from .models import Analysis
from googlesearch import search
import html
import requests
import logging
import openai

from bs4 import BeautifulSoup

# Create your views here, and this seems to work when http://127.0.0.1:8000/home called.

#Defining some global style values:
#cell_style1 = "padding: 10px; border: 2px solid black; text-align: left; vertical-align: top; font-family: Arial, sans-serif; font-size: 20px;"

def home(request):
    return render(request, 'home.html', {'name': 'Stranger'})

def GetArray(query, num_results):
    results = []
    # Perform the search
    for result in search(query, num_results):
        results.append(result)
    return results
    print(results)

def register(request):
    return render(request, 'accounts/register.html', {'name': 'BlueSpike'})


### This is the meat of Surfter ###
def SurftResults(request):

    # Will this run cost money and use ChatGPT?
    SpendMoney = True

    # Define your prompt to ChatGPT
    FrontOfPrompt = "Please analyze the following article for tone, accuracy, bias, and motivation, then summarize everything into a no more than 50 word response: " 

    # Set up OpenAI API credentials
    #OpenAi.api_key = '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'
    
    #upon the user's post on the homepage the following data is captured and used:
    queryprompt = str(request.POST["queryprompt"])
    How_many_URLs_to_get = int(request.POST["num2"])

    analysis = Analysis(query = queryprompt)
    analysis.save()

    #Get the raw URLs from GoogleSearcher.GetArray to be Surfted
    URLsGotten = GetArray(queryprompt, How_many_URLs_to_get * 2)
    URLsGotten = URLsGotten[:How_many_URLs_to_get]  # Keep x elements elements
    GoodURLs = []
    
    #TODO: Include the real vetting of URLs
    #Go through URLsGotten and get good ones back
    for i, url in enumerate(URLsGotten):
        #logging.debug("===About to run good_url===")
        good_url = discern_good_url(url, i)
        #good_url = True
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
        print("=   LOTS OF TEXT INCOMING  =")
        print("==  --------------------  ==")
        print(processedtext)
        print("== That was a lot of text! ==")
        print("=   --------------------    =")
        

        if processedtext is not None:
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
        

        

    #ArticleCollection = Article.objects.all()

    #TODO: I removed, <, 'article1': article1> from the following context line till I understand what objects to pass
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
        #article.Text = []
        ArticleCollection[i].Text = soup
        return soup
    else:
        #article.Text = []
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