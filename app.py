import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

url='https://www.airspaceonline.com/PDList.asp?pp1=02&gad_source=1&gclid=CjwKCAiA9IC6BhA3EiwAsbltOMO98DtIW3UrlYgEL7WnfP88sLphGJo6obxyGGmjT_y0zKux-vCsCRoCB-MQAvD_BwE.com'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

response=requests.get(url,headers=headers)
if response.status_code==200:
    print("success connect!!")
    soup=BeautifulSoup(response.text,'html.parser')

    datas = []
    items=soup.select('.item-main>ul>li')
    
    for data in items:
        pdlink=data.select('img')[0]['src']
        pdsize=data.find('div',class_='pdtext').select('p:nth-child(1)')[0].text
        pdname=data.find('div',class_='pdtext').select('p:nth-child(2)')[0].text
        pdprice=data.find('div',class_='pdtext').select('p.pdprice')[0].text
        datas.append({
            "Name" :pdname,
            "Link":pdlink,
            "Size":pdsize,
            "Price":pdprice,
        })
  

# connect mongodb database
client=MongoClient('mongodb://localhost:27017')
db=client['onlineshop']
collection=db['airspace']

if datas:
    collection.insert_many(datas)
    print(f"{len(datas)}插入數據成功")
else:
    print("插入數據失敗")