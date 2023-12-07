from django.shortcuts import render
from django.http import HttpResponse
from .models import Article
from googlesearch import search
import html

# Create your views here, and this seems to work when http://127.0.0.1:8000/home called.
def home(request):
    return render(request, 'home.html', {'name': 'Stranger'})

def GetArray(query):
    results = []
    # Perform the search
    for result in search(query, num_results=5):
        results.append(result)
    return results
    print(results)

def register(request):
    return render(request, 'accounts/register.html', {'name': 'BlueSpike'})

def SurftResults(request):

    # Will this run cost money and use ChatGPT?
    SpendMoney = False

    # Define your prompt to ChatGPT
    FrontOfPrompt = "Please analyze the following article for tone, accuracy, bias, and motivation, then summarize it into a no more than 50 word response: " 

    #TODO: Putting in temp data to get the object working. Need to come back and make real with process_url_into_soup
    #article1 = Article("url", "text_value", "pic_array_value", "aitext_value", "quality_article_value")

    #article1.URL = "soup"
    #article1.Text = "soup"
    #article1.PIC_Array = []
    #article1.AItext = "AItext"
    #article1.QualityArticle = "QualityArticle"

    
    table_rows = ""
    cell_style1 = "padding: 10px; border: 2px solid black; text-align: left; vertical-align: top; font-family: Arial, sans-serif; font-size: 20px;"
    cell_style2 = "padding: 10px; border: 2px solid black; text-align: left; vertical-align: top; font-family: Arial, sans-serif; font-size: 10px; word-wrap: break-word;"
    header_style1 = "width: 600px; height: 20px; padding: 10px; border: 2px solid black; text-align: center; background-color: #007bff; color: white; font-family: Arial, sans-serif; font-size: 20px;"
    header_style2 = "width: 200px; height: 20px; padding: 10px; border: 2px solid black; text-align: center; background-color: #007bff; color: white; font-family: Arial, sans-serif; font-size: 20px;"

    queryprompt = str(request.POST["queryprompt"])
    How_many_URLs_to_get = int(request.POST["num2"])

    #Get the raw URLs from GoogleSearcher.GetArray to be Surfted
    URLsGotten = GetArray(queryprompt)
    URLsGotten = URLsGotten[:How_many_URLs_to_get]  # Keep x elements elements
    
    #TODO: Include the real vetting of URLs
    GoodURLs = URLsGotten

    # Create an empty list to store Article objects
    ArticleCollection = []
    
    # Iterate through URLs and create Article objects
    #for i, url in enumerate(GoodURLs):
        # For now, let's assume you have some dummy text and PIC_Array for each article
        #dummy_text = f"Sample text for article {i+1}"
        #dummy_pic_array = [f"pic_url_{j}" for j in range(len(GoodURLs))] # Just a dummy list of pic URLs
        #dummy_aitext = f"Compwizdom for article {i+1}"
        
        # Create an Article object
        #article = Article(URL=url, Text=dummy_text, AItext = dummy_aitext, QualityArticle = False)
        
        # Add the article to the collection
        #ArticleCollection.append(article)
        #logging.info(f"article {i}'s URL is: {ArticleCollection[i].URL}")

    ArticleCollection = Article.objects.all()

    #TODO: change this to use GoodURLs
    #for i in range(How_many_URLs_to_get):
        # Build a string with image tags for each image in PIC_Array
        # TODO: image_tags = ''.join([f'<img src="{pic_url}" alt="Image" style="max-width: 100%; height: auto;">' for pic_url in ArticleCollection[i].PIC_Array])

        #table_rows += f'''
            #<tr>
                #<td style="{cell_style1}">{GoodURLs[i]}</td>
                #<td style="{cell_style1}">{ArticleCollection[i].AItext}</td>
                #<td style="{cell_style1}">{(ArticleCollection[i].Text)}</td>
            #</tr>
        #'''

    #TODO: I removed, <, 'article1': article1> from the following context line till I understand what objects to pass
    context = {'tablehtml': table_rows, 'query': queryprompt, 'depth': How_many_URLs_to_get, 'goodurls':GoodURLs, 'articlecollection': ArticleCollection, 'cellstyle1': cell_style1}
    return render(request, 'results.html', context)
