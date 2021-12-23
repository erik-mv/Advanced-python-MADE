#!/usr/bin/env python3

from bs4 import BeautifulSoup

logging_xml = open("resources/stackoverflow_posts_sample.xml")

logging_soup = BeautifulSoup(logging_xml, features="lxml")


all_soup = logging_soup.find_all("row", attrs = {"posttypeid": "1"})
print(len(all_link))


my_soup = all_soup[9]

print(my_soup.attrs["creationdate"][0:4])
print(my_soup.attrs["score"])
print(my_soup.attrs["title"])


documents = {}
for soup in all_soup:
    soup.attrs["creationdate"][0:4]
    documents[int(doc_id)]


# logging_soup.find_all("a", attrs = {"calss": "lox"}) 