from bs4 import BeautifulSoup
import requests
import os
import base64
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_image_from_url(url, filename):
    try:
        image_content = requests.get(url).content
        with open(filename, 'wb') as f:
            f.write(image_content)
        print(f"Downloaded image {filename}")
    except Exception as e:
        print(f"Failed to download image {filename}: {e}")

def save_base64_image_from_data_url(data_url, filename):
    try:
        
        img_format, img_data = data_url.split(';base64,')
        ext = img_format.split('/')[-1]  # Extract image extension

     
        img_data = base64.b64decode(img_data)

        # Create a PIL image object from the decoded image data
        img = Image.open(BytesIO(img_data))

        # Save the image to file
        img.save(filename)
        print(f'Saved image {filename}')

    except Exception as e:
        print(f'Failed to save base64 image {filename}: {str(e)}')

# Function to extract image details and write them to CSV
def extract_image_details(images, download_directory):
    image_details = []
    for idx, img in enumerate(images):
        image_link = img.get_attribute('src')
        alt_text = img.get_attribute('alt')
        if image_link:
            if image_link.startswith('data:image/'):
                filename = f"{download_directory}image_{idx+1}.jpg"
                save_base64_image_from_data_url(image_link, filename)
            else:
                filename = f"{download_directory}image_{idx+1}.jpg"
                download_image_from_url(image_link, filename)
            image_details.append([idx + 1, filename, image_link, alt_text])
    return image_details

# Main code
url = "https://www.gettyimages.com/photos/human-finger-print"


driver = webdriver.Chrome() 

driver.get(url)

wait = WebDriverWait(driver, 10)
images = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.BLA_wBUJrga_SkfJ8won')))

download_directory = 'downloaded_images/'
create_directory(download_directory)

image_details = extract_image_details(images, download_directory)

with open('image_details.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['S.No', 'Image Location', 'Image Link', 'Image Description'])
    for row in image_details:
        writer.writerow(row)

driver.quit()