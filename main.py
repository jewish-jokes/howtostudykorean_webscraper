import time
import requests
import re
from bs4 import BeautifulSoup
import csv

from unit_1_urls import urls_list as urls

wait_time = 5


def get_data_from_website(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch data from {url}. Status code: {response.status_code}")
        return None


def parse_html_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    data = []
    # try:
    As = soup.find_all("a", href=re.compile("mp3"))
    for a in As:
        meaning = None
        if a.parent.find("span", class_ = 'collapseomatic noarrow'):
            meaning = a.parent.find("span", class_ = 'collapseomatic noarrow')["title"]
        pronunciation = a["href"]
        word = a.text
        print(type(meaning))
        if meaning and pronunciation and word:
            data.append([word, meaning, pronunciation])    
    # except TypeError:
    #     pass
    return data


def save_to_csv(data, output_file):
    with open(output_file, "a", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        # csv_writer.writerow(["word", "meaning", "pronunciation"])
        for word, meaning, pronunciation in data:
            csv_writer.writerow([word, meaning, pronunciation])


def main():
    output_file = "data.csv"
    for url in urls:
        #print(url)
        html_content = get_data_from_website(url)
        if html_content:
            data = parse_html_content(html_content)
            save_to_csv(data, output_file)
            print(f"Data saved to {output_file}")
        # time.sleep(wait_time)


if __name__ == "__main__":
    main()
