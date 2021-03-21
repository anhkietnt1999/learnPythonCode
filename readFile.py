import  json
import  unicodedata
import	MySQLdb

db= None
f1	=	open('dearticle-9.txt',	'r')
data	=	f1.read()
line1 = f1.readline()
jsonstr = json.loads(data)


rank = jsonstr['TITLE']['Rank']
link = jsonstr['TITLE']['TitleClass']['link']
content = jsonstr['TITLE']['TitleClass']['content']
sitelink = jsonstr['TITLE']['SiteComhead']['sitelink']
sitestr = jsonstr['TITLE']['SiteComhead']['sitestr']
score = jsonstr['SUBTEXT']['Score']['score']
user =  jsonstr['SUBTEXT']['Users']['user_name']
age =  jsonstr['SUBTEXT']['Ages']['age_string']
hide =  jsonstr['SUBTEXT']['Hides']['hide_string']
comment =  jsonstr['SUBTEXT']['Comments']['comment']
subtext = score+" by "+user +" "+ age +"\| "+hide + comment
print(subtext)
try:
    db =MySQLdb.connect(host='localhost',user='root',passwd='',db='crawldata',charset='utf8')
    print('thanh cong ')

except	MySQLdb.Error:
    print ("error")


if db:
    cur =db.cursor()
    sql = "INSERT INTO dataread (rank,link,title,linksite,titlesite,subtext) VALUES (%s, %s,%s, %s, %s, %s)"
    val = (rank, link, content, sitelink, sitestr ,subtext)
    cur.execute(sql,val)
    db.commit()


print(cur.rowcount, "record inserted.")
