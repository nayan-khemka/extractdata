import requests
import pandas as pd
from bs4 import BeautifulSoup
import openpyxl

def fetch_and_extract_tables(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')

    data_frames = []
    for table in tables:
        df = pd.read_html(str(table))[0]
        data_frames.append(df)

    return data_frames

def save_to_excel(data_frames, filename):
    with pd.ExcelWriter(filename) as writer:
        if data_frames:  # Check if there's at least one DataFrame
            for i, df in enumerate(data_frames):
                df.to_excel(writer, sheet_name=f'Table_{i+1}')
        else:
            # Create at least one empty sheet if there are no data frames
            pd.DataFrame().to_excel(writer, sheet_name='Empty')

def main():
    url = 'https://www.snam.it/en/our-businesses/transportation/operational-data-business/phisical-flows-on-the-national-network.html'
    data_frames = fetch_and_extract_tables(url)
    save_to_excel(data_frames, 'tables.xlsx')

if __name__ == '__main__':
    main()
