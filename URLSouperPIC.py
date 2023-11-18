import requests
from bs4 import BeautifulSoup
import logging

def get_pic_urls(url, limit):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    image_tags = soup.find_all('img')
    
    # Limit the number of image_tags before the loop
    image_tags = image_tags[:limit]
    
    image_urls = []  # Use a list instead of a dictionary to store image URLs
    logging.debug("Starting get_pic_urls for loop!")
    
    for img in image_tags:
        if 'src' in img.attrs:
            image_url = img['src']
            image_urls.append(image_url)
            logging.debug(image_url + " In the get_pic_urls loop!")

    if not image_urls:  # Return "nothing found" only if no image URLs were found
        return "nothing found"

    #print(image_urls)
    logging.debug(image_urls)
    logging.debug("Right before 'return image_urls'")
    #input()
    return image_urls