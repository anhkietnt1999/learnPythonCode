import requests
import re
import unicodedata
import json
from bs4 import BeautifulSoup

# The function is used to get data from the website, the passed parameter is a soup (lxml)
def crawl_data_tite(
        soup_response_content):

    # The array is used to store data of title from website
    data_all = []
    # The array is used to store rank of article
    data_rank = []
    # The array is used to store storylink (link and content)
    data_storylink = []
    # The array is user to store sitelink and sitestr
    data_site = []

    # Take all of the rank on the web with a rank class
    ranks = soup_response_content.find_all('span', class_='rank')
    # Handle to replace character '.' and save to data_rank
    for rank in ranks:
        tempstr = rank.string.replace('.', '')
        data_rank.append(tempstr)


    # Take all of the Title on the web with class = title
    titles = soup_response_content.find_all('td', class_="title")

    # Process on each line of the title to get necessary data
    for title in titles:
        storylink = title.find('a', class_='storylink')
        sitebit = title.find('span', class_='sitebit comhead')

        # If the article does not have a storylink set its value to None
        # otherwise the data_storylink gets the value from the data obtained from the web
        if (storylink == None):
            data_storylink.append(
                {
                'link': None,
                'story': None
                }
            )
        else:
            data_storylink.append(
                {
                'link': storylink['href'],
                'story': storylink.string
                }
            )

        # If the article does not have a site set its value to None
        # otherwise the data_site gets the value from the data obtained from the web
        if (sitebit == None):
            data_site.append(
                {
                'sitelink': None,
                'sitestr': None
                }
            )
        else:
            data_site.append(
                {
                'sitelink': sitebit.a['href'],
                'sitestr': sitebit.span.string
                }
            )

    # At the end of the loop, we merge the data together to get the first part of the article

    # variable count is used as the run variable to merge the data
    # The number of article is determined by the rank in the page
    count = 0

    while count < len(ranks):
        data_all.append(
            {
            'Rank': data_rank[count],
            'TitleClass': data_storylink[count],
            'SiteComhead': data_site[count]
            }
        )
        count += 1

    # At the end of the function we get the data from the first part of the article
    return data_all
















