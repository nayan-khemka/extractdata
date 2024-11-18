from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def extract_table(url):


    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Explicitly wait for the table to load (adjust timeout as needed)
    wait = WebDriverWait(driver, 10)
    table = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "table")))  # Adjust the selector as needed

    # Get the rendered HTML content
    html_content = driver.page_source
   
    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find('table')
    print(table)
    table_data = []
    for row in table.find_all('tr'):
        row_data = []
        rowspan = 1  # Initialize rowspan for each row
        for cell in row.find_all(['td', 'th']):
            if cell.has_attr('rowspan'):
                rowspan = int(cell.get('rowspan'))
            if cell.has_attr('colspan'):
                colspan = int(cell.get('colspan'))
                row_data.extend([cell.text.strip()] * colspan)
            else:
                row_data.append(cell.text.strip())
        table_data.extend([row_data] * rowspan)

    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    driver.quit()

    return df


def save_to_excel(df, file_path):
    # Assuming the Excel file is in the same directory as the script
    file_path = os.path.join(os.getcwd(), file_path)

    if not os.path.exists(file_path):
        df.to_excel(file_path, index=False)
    else:
        with pd.ExcelWriter(file_path, mode='a', if_sheet_exists='replace') as writer:
            df.to_excel(writer, sheet_name='Sheet1', index=False)

url = "https://www.snam.it/en/our-businesses/transportation/operational-data-business/phisical-flows-on-the-national-network.html"
filename = "snam_table.xlsx"

df = extract_table(url)
save_to_excel(df, filename)

print(f"Table extracted and saved to {filename}")
