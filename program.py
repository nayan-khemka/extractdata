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
        if df.applymap(lambda x: isinstance(x, (int, float))).any().any():
            data_frames.append(df)

    return data_frames

def save_to_excel(data_frames, filename):
    with pd.ExcelWriter(filename) as writer:
        for i, df in enumerate(data_frames):
            df.to_excel(writer, sheet_name=f'Table_{i+1}')

def main():
    url = 'https://teams.microsoft.com/l/message/19:02af48fa-f7ab-4f7a-9063-146672972066_6e9bbcc8-378d-464a-be47-9fb6b06c76f8@unq.gbl.spaces/1731919250519?context=%7B%22contextType%22%3A%22chat%22%7D'
    data_frames = fetch_and_extract_tables(url)
    save_to_excel(data_frames, 'tables.xlsx')

if __name__ == '__main__':
    main()
