import  requests
import  unicodedata
import  html
import html.parser

import  json

def CrawlDataString(resString,posStart,posEnd):
    # url = "https://news.ycombinator.com/"

    temp_new = resString

    # get content web and covert to string



    #find position start- end  of  Article (only 1)


    # find string contain value rank
    strGetRank = temp_new[posStart:posEnd - 170]
    # get the value of rank
    rank = strGetRank[13:15]

    #  From strGetRank, filter  string Title and children of class Title
    strTitle = 'class="title"><a href='
    strEndTitle = '</a>'
    posStartTitle = strGetRank.find(strTitle)
    posEndTitle = strGetRank.find(strEndTitle, posStartTitle + 1)
    strGetTitle = strGetRank[posStartTitle:posEndTitle]

    #continue get position class storylink
    posClassStory = strGetTitle.find('class="storylink')
    lenStory = len('class="storylink"') + 1
    # get Value link, title
    link = strGetTitle[22:posClassStory]
    Title =unicodedata.normalize("NFKD" ,strGetTitle[posClassStory + lenStory:None])

    # get link site and title site
    posEndSite = strGetRank.find('class="subtext"')

    strSite = strGetRank[posEndTitle:posEndSite - 39]
    postEndLinkSite = strSite.find('sitestr')
    linkSite = strSite[44:postEndLinkSite - 14]

    titleSite = linkSite[11:-1]


    # subtext of article

    # find postions purpose get value subtext

    posSubtextStart = strGetRank.find('class="score"')
    posSubtextEnd = strGetRank.find('comments</a>')

    strSubtext = strGetRank[posSubtextStart:posSubtextEnd]
    postEndPoint = strSubtext.find('</span> by')

    # get values point, hnuser, age, comments

    Point = strSubtext[34:postEndPoint] + " by "
    posStartHNUser = strSubtext.find('class="hnuser"')
    # find position age
    posStartAge = strSubtext.find('<span class="age"')
    poseEndAge = strSubtext.find('</a></span')
    # get username and age
    username = strSubtext[posStartHNUser + 15:posStartAge - 5]
    age = strSubtext[posStartAge + 45:poseEndAge]
    # find position string comment and get value it
    posStartCom = strSubtext.rfind('href=')
    countCom = strSubtext[posStartCom + 24:None] + " comments"

    # remove special character
    # comments = count new Comment
    countCom_new = countCom.replace("&nbsp;", ' ')


    # initialize  Dictionary Aricle and wirte json - save file txt

    # init dict
    article = {
        'rank': rank,
        'link': link,
        'title':Title,
        'linksite': linkSite,
        'titleSite': titleSite,
        'point': Point,
        'username': username,
        'age': age,
        'comments': countCom_new
    }
    # write and save
   # myjson = article
    #sname = "dearticle-.txt"
  #  with open(sname, 'a+') as myfile:
       # json.dump(myjson, myfile)
    return  article




url = "https://news.ycombinator.com/"
response = requests.get(url) #get html from url
temp = html.unescape(response.text)
temp_new = unicodedata.normalize("NFKD", temp)


posCheck =1

posStart = temp_new.find('class="rank"')
posEnd = temp_new.find('class="rank"',posStart+1)
while (posStart>0):

   a=CrawlDataString(temp_new,posStart,posEnd)
   posStart = temp_new.find('class="rank"',posStart+1)
   posEnd = temp_new.find('class="rank"',posStart+1)
   print(a)

