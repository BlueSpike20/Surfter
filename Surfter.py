import requests
import webbrowser
import openai
import GoogleSearcher
import URLSouper2
import html
import time
import URLSouperPIC
import logging
import os
import threading
import sys
import re
from bs4 import BeautifulSoup

# Find URLs from a query string given the following paramaters
QueryString = "What smells the best?"

# Will this run cost money and use ChatGPT?
SpendMoney = False

# Define your prompt to ChatGPT
FrontOfPrompt = "Please analyze the following article for tone, accuracy, bias, and motivation, then summarize it into a no more than 50 word response: " 

# Set the working directory
WorkingDirectory = os.path.dirname(os.path.realpath(__file__))
os.chdir(WorkingDirectory)

#Check for old log and delete if it exists:
log_file_path = WorkingDirectory + '\output.log' 

# Check if the file exists
if os.path.exists(log_file_path):
    # If it exists, delete it
    os.remove(log_file_path)
    print(f"{log_file_path} deleted.")
    #logging.info(f"{log_file_path} deleted.")
else:
    print(f"{log_file_path} does not exist.")
    #logging.info(f"{log_file_path} deleted.")

# Redirect stdout and stderr to a file
log_file = open(log_file_path, 'a')  # 'a' mode appends to the file
#sys.stdout = log_file
sys.stderr = log_file

# Configure the logging
logging.basicConfig(filename='output.log', level=logging.INFO)

# Set up OpenAI API credentials
openai.api_key = 'lol'

class Article:
    def __init__(self, URL, Text, PIC_Array, AItext, QualityArticle):
        # self.name = name TODO
        self.URL = URL
        self.Text = Text
        self.PIC_Array = PIC_Array
        self.AItext = AItext
        self.QualityArticle = QualityArticle
    
    def __repr__(self):
        return repr((self.URL, self.Text, self.PIC_Array, self.AItext, self.QualityArticle))


# Sanitize the QueryString for use as a filename
sanitized_query_string = re.sub(r'[^\w\s]', '_', QueryString)

# Now you can use it in the file_path
file_path = f"{WorkingDirectory}\\SurftArchive\{sanitized_query_string}.html"

def loading_animation():
    animation = "|/-\\"
    for _ in range(10):
        for char in animation:
            yield char
            time.sleep(0.1)

def print_with_animation(text):
    print(text, end='\r')

def discern_good_url(url, timeout=2):
    try:
        if timeout <= 0:
            timeout = 0.1  # Set a minimum positive value for timeout
    
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
            print(f"Warning: {url} returned status code {response.status_code}")
            response.raise_for_status()  # Raise an exception for other errors (e.g., network issues)
            logging.info(f"Warning: {url} returned status code {response.status_code}")
            return None
        return url
        
    except requests.exceptions.Timeout:
        print(f"Timeout while accessing {url}")
        logging.info(f"Timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        logging.info(f"Error accessing {url}: {e}")
        return None
    except ValueError as ve:
        print(f"ValueError: {ve}")
        logging.info(f"ValueError: {ve}")
        return None


def use_soup_with_timeout(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
            print(f"Warning: {url} returned status code {response.status_code}")
            response.raise_for_status()  # Raise an exception for other errors (e.g., network issues)
            pass
        return URLSouper2.use_soup(url)
        
    except requests.exceptions.Timeout:
        print(f"Timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None
        
def use_soup_pic_with_timeout(url, timeout=2):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code >= 400:
            print(f"Warning: {url} returned status code {response.status_code}")
            response.raise_for_status()  # Raise an exception for other errors (e.g., network issues)
            pass
        return URLSouperPIC.get_pic_urls(url, How_Many_Pics_Per_URL)
        
    except requests.exceptions.Timeout:
        print(f"Timeout while accessing {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return None

def process_url_into_text(article, index):
    soup = use_soup_with_timeout(article.URL)
    if soup:
        #article.Text = []
        article.Text = soup
    else:
        #article.Text = []
        article.Text = f" :( See Failure for {article.URL} in log..."
        logging.info(article.URL + ' failed soup into text')
        
def process_url_into_image_url(article, index):
    soup = use_soup_pic_with_timeout(article.URL) 
    if soup:
        # Clear the existing PIC_Array
        article.PIC_Array = []
        
        # Add the first 3 URLs to the PIC_Array
        article.PIC_Array.extend(soup[:How_Many_Pics_Per_URL])
        #article.PIC_Array.extend(url for url in article.PIC_Array)
    else:
        article.PIC_Array.append(":( See Failure in log...")
        logging.info(article.URL + ' failed soup_pic')



def animation_thread_function():
    for char in animation_generator:
        print_with_animation(f'{char} Spinning...')
        time.sleep(0.1)

animation_generator = loading_animation()
    
print("Standby")
logging.info("===Start of the log, enjoy!===")

# Start the animation thread in parallel so there's something to look at while running
animation_thread = threading.Thread(target=animation_thread_function)
animation_thread.start()

#Get all the URLs to do logic on:
URLsGotten = GoogleSearcher.GetArray(QueryString)
URLsGotten = URLsGotten[:2]  # Keep x elements elements
GoodURLs = []
How_Many_Pics_Per_URL = 10



# Create an empty list to store Article objects
ArticleCollection = []

#Go through URLsGotten and get good ones back
for i, url in enumerate(URLsGotten):
    logging.debug("===About to run good_url===")
    good_url = discern_good_url(url, i)
    #good_url = True
    logging.debug("===About to append to GoodURLs===")
    if good_url and good_url not in GoodURLs:
        GoodURLs.append(good_url)
        
#print(GoodURLs)
logging.info(f"URLsGotten Array length: {len(URLsGotten)}")
logging.info(f"URLsGotten Array: {URLsGotten}")
logging.info(f"GoodURLs Array length: {len(GoodURLs)}")
logging.info(f"GoodURLs Array: {GoodURLs}")

# Iterate through URLs and create Article objects
for i, url in enumerate(GoodURLs):
    # For now, let's assume you have some dummy text and PIC_Array for each article
    dummy_text = f"Sample text for article {i+1}"
    dummy_pic_array = [f"pic_url_{j}" for j in range(len(GoodURLs))] # Just a dummy list of pic URLs
    
    # Create an Article object
    article = Article(URL=url, Text=dummy_text, PIC_Array=dummy_pic_array, AItext = "Compwizdom", QualityArticle = False)
    
    # Add the article to the collection
    ArticleCollection.append(article)
    logging.info(f"article {i}'s URL is: {ArticleCollection[i].URL}")
    



print()  # Print a new line after the animation is done


def generate_response(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text.strip()

# Process URLs in the main thread
for i, article in enumerate(ArticleCollection):
    process_url_into_text(ArticleCollection[i], i)
    #logging.info(f"{ArticleCollection[i].URL} is the URL from article {i}") TODO: Make this work with the article's text
    process_url_into_image_url(ArticleCollection[i], i)
    logging.info(f"article {i}'s pics are {ArticleCollection[i].PIC_Array}")
    logging.debug(f'URL from article {i} = {ArticleCollection[i].URL}')
    
    if SpendMoney:
        ArticleCollection[i].AItext = generate_response(FrontOfPrompt + ArticleCollection[i].Text)  # COSTS MONEY
    else:
        ArticleCollection[i].AItext = FrontOfPrompt + ArticleCollection[i].Text


def generate_html():
    title = "My Attempt to understand '" + QueryString + "' with OpenAi:"
    logo_image_url = os.path.join(WorkingDirectory, 'images', 'InfoSorter_thumb.jpg')
    background_image_url = os.path.join(WorkingDirectory, 'Images', 'Background2.jpg')
    # Replace backslashes with forward slashes
    background_image_url = background_image_url.replace('\\', '/')
    logging.debug(logo_image_url + " | Is logo filepath")
    logging.debug(background_image_url + " | Is background filepath")
    
    table_rows = ""
    cell_style1 = "padding: 10px; border: 2px solid black; text-align: left; vertical-align: top; font-family: Arial, sans-serif; font-size: 20px;"
    cell_style2 = "padding: 10px; border: 2px solid black; text-align: left; vertical-align: top; font-family: Arial, sans-serif; font-size: 10px; word-wrap: break-word;"
    header_style1 = "width: 600px; height: 20px; padding: 10px; border: 2px solid black; text-align: center; background-color: #007bff; color: white; font-family: Arial, sans-serif; font-size: 20px;"
    header_style2 = "width: 200px; height: 20px; padding: 10px; border: 2px solid black; text-align: center; background-color: #007bff; color: white; font-family: Arial, sans-serif; font-size: 20px;"

    for i in range(len(GoodURLs)):
        # Build a string with image tags for each image in PIC_Array
        image_tags = ''.join([f'<img src="{pic_url}" alt="Image" style="max-width: 100%; height: auto;">' for pic_url in ArticleCollection[i].PIC_Array])
        
        table_rows += f'''
            <tr>
                <td style="{cell_style1}">
                    {GoodURLs[i]}<br>{image_tags}
                </td>
                <td style="{cell_style1}">
                    {ArticleCollection[i].AItext}
                    
                </td>
                <td style="{cell_style2}">
                    {str(html.escape(ArticleCollection[i].Text))}
                </td>
            </tr>
        '''

    html_test_var = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>BlueSpike's InfoPage</title>
        <style>
            body {{
                background-image: url('{background_image_url}');
                background-size: cover;  /* Adjust as needed */
                background-attachment: fixed;
            }}
        </style>
    </head>
    <body>
        <img src="{logo_image_url}" alt="Image" style="float: left; margin-right: 20px; vertical-align: middle; margin-bottom: 10px;">
        <h1 style="display: inline-block; vertical-align: middle; text-align: center;">{title}</h1>
        
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <th style="{header_style1}">Article URL and Pic</th>
                <th style="{header_style1}"> {FrontOfPrompt} </th>
                <th style="{header_style2}">Raw Text</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    '''
    
    return html_test_var

# Generate the HTML content
html_content = generate_html()

# Write the HTML content to a file
with open(file_path, 'w', encoding='utf-8') as file:
    file.write(html_content)

# Open the HTML file in a web browser
webbrowser.open(file_path)

# Wait for the animation thread to finish
animation_thread.join()

print("Hit Something!")




logging.info("===End of the log, enjoy!===")
#input()

# Close the log file and restore stdout and stderr
log_file.close()
#sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__