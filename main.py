import time
import requests
from bs4 import BeautifulSoup as Soup
from loader import printProgressBar
from cookies_headers import cookies, headers, url
import pandas as pd


def fetchNewTopics():
    response = requests.get(url=url, cookies=cookies, headers=headers)
    soup = Soup(response.text, "html.parser")
    table = soup.find(lambda tag: tag.name == 'table' and tag.has_attr('id') and tag['id'] == "table_1")
    rows = table.findAll(lambda tag: tag.name == 'tr')
    updated_topics = [row.get_text(strip=True)
                      for row in soup.select("table#table_1 tr > td:nth-of-type(3)")]
    updated_supervisors = [row.get_text(strip=True)
                           for row in soup.select("table#table_1 tr > td:nth-of-type(4)")]

    outdated_topics = getOutdatedTopics()
    new_topics = dict()
    printProgressBar(0, len(updated_topics), prefix='Checking topics:', suffix='Complete', length=50)
    for i in range(len(updated_topics)):
        time.sleep(0.01)
        printProgressBar(i + 1, len(updated_topics), prefix='Checking topics:', suffix='Complete', length=50)
        if updated_topics[i] not in outdated_topics:
            new_topics[updated_topics[i]] = updated_supervisors[i]

    showNewTopics(new_topics)
    save_to_csv(updated_topics, updated_supervisors)
    return True


def save_to_csv(topics, supervisors):
    with open("topics_fei_api.csv", "w", encoding="ansi") as file:
        file.write("topic;supervisor \n")
        for i in range(len(topics)):
            file.write(topics[i] + ";" + supervisors[i] + "\n")


def save_to_txt(topics, supervisors):
    with open("output.txt", "w") as txt_file:
        for topic in topics:
            txt_file.write(topic + "\n")


def getOutdatedTopics():
    csv = pd.read_csv("topics_fei_api.csv", delimiter=";", encoding="ansi")
    topics_arr = csv["topic"]
    out_top = dict()
    for i in range(len(topics_arr)):
        out_top[topics_arr[i]] = i
    return out_top


def showNewTopics(dic):
    if len(dic) > 0:
        print("New topics found:")
        for key, value in dic.items():
            print(key, value)
    else:
        print("No new topics found! \n ")


if __name__ == '__main__':
    print("Check started! \n")
    fetchNewTopics()
    print("Check done!")
