import html
import json
import unicodedata


import requests
import	MySQLdb

from bs4 import  BeautifulSoup



def crawl_data_bds(link):

    # link of website to do get data
    source = "https://alonhadat.com.vn/nha-dat/can-ban/nha-mat-tien/5/can-tho.html"
    url = link
    response = requests.get(url)



    # use the bs4 library to get the entire html page content

    soup = BeautifulSoup(unicodedata.normalize("NFKD",response.text), "lxml")

    # find element contains title and posting date

    title = soup.find('div',class_='title')


    # find element contains detail text content of post

    detail_content = soup.find('div',class_="detail text-content")
    breakline = ""
    temp = breakline.join(detail_content.string.splitlines())
    # find class = price contains price value

    price_class = soup.find('span',class_='price')
    price = price_class.find('span',class_='value')


    # find the square, area and address of the property
    # find element contains square

    square_class = soup.find('span',class_='square')
    square = square_class.find('span',class_='value')


    # find class = addres contains addres of the property
    addr_class = soup.find('div',class_='address')
    addr = addr_class.find('span',class_='value')

   # find the list of images contained in the class limage

    listimg = soup.find_all('img',class_='limage')

    # get src each image in listimg
    data_image = []
    for imghide in listimg:
        data_image.append(
            {
             'img_src': imghide['src']
            }
        )


    # find and get all data in table with class = moreinfor1
    more_info_string = " "
    tbl = soup.find_all('tr')

    for tb in tbl:
        tds = tb.find_all('td')
        for td in tds:
            more_info_string += td.getText() +" | "

    # merge all data from the web into a single dict
    data_all = {
        'link': link,
        'title': title.h1.string,
        'post_date': title.span.string,
        'price': price.string,
        'square': square.getText(),
        'address': addr.getText(),
        'content': temp,
        'list-img': data_image,
        'more-info': more_info_string,
        'source': source
    }

    myjson = data_all
    sname = "nhadatcanbanct.txt"
    with open(sname, 'a+') as myfile:
        json.dump(myjson, myfile)
    return data_all

    return data_all
def crawl_data_not_ctbds(link):
    # link of website to do get data

    source ="https://alonhadat.com.vn/nha-dat/can-ban.html"

    url = link
    response = requests.get(url)

    soup = BeautifulSoup(unicodedata.normalize("NFKD",response.text), "lxml")


    title = soup.find('div',class_='title')

    detail_content = soup.find('div',class_="detail")

    content_text = detail_content.findAll('span')
    temp = ""
    breakline =""
    for con in content_text:
        temp+= con.getText()
    new_str = unicodedata.normalize("NFKD", temp)

    data_img = []
    listimg = detail_content.findAll('img')
    for img in listimg:
        data_img.append(
            {
                'img_src': img['src']
            }
        )
        # find class = price contains price value

    price_class = soup.find('span', class_='price')
    price = price_class.find('span', class_='value')

    # find the square, area and address of the property
    # find element contains square

    square_class = soup.find('span', class_='square')
    square = square_class.find('span', class_='value')

    # find class = addres contains addres of the property
    addr_class = soup.find('div', class_='address')
    addr = addr_class.find('span', class_='value')

    more_info_string = " "
    tbl = soup.find_all('tr')

    for tb in tbl:
        tds = tb.find_all('td')
        for td in tds:
            more_info_string += td.getText() + " | "

        # merge all data from the web into a single dict
    data_all = {
            'link': link,
            'title': title.h1.string,
            'post_date': title.span.string,
            'price': price.string,
            'square': square.getText(),
            'address': addr.getText(),
            'content': new_str,
            'list-img': data_img,
            'more-info': more_info_string,
            'source': source
    }

    myjson = data_all
    sname = "nhadatcanban.txt"
    with open(sname, 'a+') as myfile:
        json.dump(myjson, myfile)

    return data_all


def branching_condition(link):
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    branch = soup.find("div", class_="imageview")

    if(branch!= None):
      return crawl_data_bds(link)
    else:
      return crawl_data_not_ctbds(link)



def imp_mysql():
    url = "https://alonhadat.com.vn/dat-binh-chanh-cach-cho-500m-mt-hoang-phan-thai-gia-cuc-soc-7981850.html"
    article =  branching_condition(url)
    link = article['link']
    title = article['title']
    post_date= article['post_date']
    price = article['price']
    square = article['square']
    addr = article['address']
    content = article['content']
    more_info = article['more-info']
    source = article['source']
    listimg = " "
    for i in (article['list-img']):
        listimg += i['img_src'] +" \n "
    db = None
    try:
        db = MySQLdb.connect(host='localhost', user='root', passwd='', db='db_bds_aloha', charset='utf8')
        print('thanh cong ')

    except    MySQLdb.Error:
        print("error")

    if db:
        cur = db.cursor()
        sql = "INSERT INTO alonhadat (link, title, postdate, price, square, address, content, listimg, infor, source) " \
              "VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (link, title, post_date, price, square, addr, content, listimg, more_info, source)
        cur.execute(sql, val)
        db.commit()
    print(cur.rowcount, "record inserted.")



imp_mysql()