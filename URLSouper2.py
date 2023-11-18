#Turns the paragragh text at the given URL into readable text. Other messy use examples below.
import requests

from bs4 import BeautifulSoup

def use_soup(url):
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # soup_text = soup.get_text()
    # soup_clipped = soup_text[:1000] 

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all paragraph tags in the soup
    paragraphs = soup.find_all('p')
        
    # Extract text from each paragraph and concatenate
    paragraph_text = ""
    for paragraph in paragraphs:
        paragraph_text += paragraph.get_text() + " "

    return paragraph_text.strip()    


    
    #Paragraph = soup.find('div').find('p').text.strip()
    #Paragraph = soup.prettify()
    
    
    
    #Paragraph_clipped = Paragraph[:5000] 
    #print(Paragraph_clipped + "<- Should be the paragraph")
    #return(soup_clipped)
    #return(Paragraph_clipped)