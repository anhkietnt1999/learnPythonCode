from bs4 import BeautifulSoup
import  requests
import  unicodedata
import re
import  json


def CrawlDataPage(soup):

    dataAll = []
    dataStory = []
    dataSite = []
    dataRank = []
    Ranks = soup.find_all('span',class_='rank')
    for rank in Ranks:
        tempstr = rank.string.replace('.','')
        dataRank.append(tempstr)
        print(tempstr)
    Titles = soup.find_all('td',class_="title")
    for title in Titles:
        storylink = title.find('a', class_='storylink')
        if (storylink == None):
            dataStory.append({
                'link': None,
                'story': None
            })
        else:

            dataStory.append({
                'link': storylink['href'],
                'story': storylink.string
            })
        sitebit = title.find('span', class_='sitebit comhead')
        if (sitebit == None):
            dataSite.append({
                'sitelink': None,
                'sitestr': None
            })
        else:
           dataSite.append({
               'sitelink': sitebit.a['href'],
               'sitestr': sitebit.span.string
           })

    count = 0

    while (count < len(Ranks)):
        dataAll.append({
            'Rank': dataRank[count],
            'TitleClass': dataStory[count],
            'SiteComhead': dataSite[count]

        })
        count += 1

    return dataAll

def CrawlDataSubtext(soup):
    dataAll = []
    dataScore =[]
    dataUser = []
    dataAge =[]
    dataHide =[]
    dataCom = []
    subtexts = soup.find_all('td',class_='subtext')
    i=1
    for sub in subtexts:

        scores = sub.find('span',class_='score')
        if (scores == None):
            dataScore.append({
                'id_score': None,
                'score': None
            })
        else:
            dataScore.append({
                'id_score': scores['id'],
                'score': scores.string
            })



        user = sub.find('a', class_="hnuser")
        if ( user == None):
           dataUser.append({
            'user_link': None,
            'user_name': None
           })
        else:
            dataUser.append({
                'user_link': user['href'],
                'user_name': user.string
            })
        age = sub.find('span', class_='age')
        if (age == None):
            dataAge.append({
                'user_link': None,
                'user_name': None

            })
        else:
          dataAge.append({
              'age_link': age.a['href'],
              'age_string': age.a.string
          })

        hide = sub.find("a", href=re.compile("hide?"))
        if(hide == None):
            dataHide.append({
                'hide_link': None,
                'hide_string':None
            })


        else:
            dataHide.append({
                'hide_link': hide['href'],
                'hide_string': hide.string
            })
        preComment = hide.next_sibling
        comment =preComment.next_sibling
        if (comment == None):
            dataCom.append({
                'comment_link': None,
                'comment': None
            })
        else:
            dataCom.append({
                'comment_link': comment['href'],
                'comment': unicodedata.normalize("NFKD", comment.string)
            })
        count = 0
        while (count < len(dataHide)):
            dataAll.append({
                'Score': dataScore[count],
                'Users': dataUser[count],
                'Ages': dataAge[count],
                'Hides': dataHide[count],
                'Comments': dataCom[count]

            })

            count += 1

    return dataAll


page = 2

while (page <3):

    url ="https://news.ycombinator.com/news?p="+str(page)
    response =  requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    Titles = CrawlDataPage(soup)
    Subtexts = CrawlDataSubtext(soup)
    count = 1
    dataTotals = []
    while(count<len(Titles)):
        dataTotals.append({
            'TITLE' :Titles[count],
            'SUBTEXT': Subtexts[count]
        })
        count+=1



    for total in dataTotals:
        print('--------')
        print(total)
        print('\n')
        print('------------')
        myjson = total
        sname = "rearticle-"+ (total['TITLE'])['Rank']+".txt"
        with open(sname, 'a+') as myfile:
        json.dump(myjson, myfile)

    page+=1
