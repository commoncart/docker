#####IMPORING LIBRARIES######
'''
	sudo apt-get install python3-pip
	sudo pip3 install urllib3
	sudo apt-get install python3-bs4
	sudo pip3 install pymongo


	#importing data into mongodb server#
	mongoimport --db production --collection products --type csv --headerline --file /var/data/products.csv
	mongod --repair # for reparing the mongo db server

	mongod --fork --logpath /var/log/mongodb.log

	sudo rm /var/lib/mongodb/mongod.lock #remove lock file
	mongod --repair 	#repair mongo
	sudo service mongodb start #restart service

	mongo production --eval "db.dropDatabase();" # drop database
'''
#####IMPORING LIBRARIES######
#imporing files starts

#connect multiple sockets connections
import urllib3

#creates pool for multi process
import multiprocessing as mp

#make HTML into a structure to parse
from bs4 import BeautifulSoup

#execute CSV import and export
import csv

#Basic System Commands
import sys

#Execute JSON data
import json

#Use time library
import time

#Mongo database connection library
#import pymongo

#from pymongo import MongoClient

#imporing Files ends here


#set up connection pool using socket
http = urllib3.PoolManager()

#########DEFINING MONGO DB CONNECTION VALUES################
'''
HOST = 'localhost'
PORT = 27017
DATABASE = 'production'
COLLECTION = 'products'
#########DEFINING MONGO DB CONNECTION VALUES################
client = MongoClient()
client = MongoClient(HOST,PORT)
db = client.DATABASE
collection = db.COLLECTION


for data in db.collection.find().limit(2):
    print(data)
sys.exit()
'''
BASE_URL = 'http://www.snapdeal.com/'
PIN_CODE = '110001'
AFFILIATE_ID = '?utm_source=aff_prog&utm_campaign=afts&offer_id=17&aff_id=8121'
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'en-US,en;q=0.5',
    'Connection':'keep-alive',
    'Host':'www.snapdeal.com',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0'
    }

# call this method to execut the call of each product URL's#
def callEachProductsWithURL(url):
    with open('/snapdealout/processedurls.csv', 'wb') as myFile:
        myFile.write(url)
        myFile.write('\n')
    with open('/snapdir/processedurls.csv', 'wb') as myFile:
        myFile.write(url)
        myFile.write('\n')
    r = http.request('GET',url,headers=headers)
    print(r.status)
    if(r.status == 200):
        time_stmp = time.strftime('%Y-%m-%d %H:%M:%S')
        bread_crumb = ''
        product_name= ''
        product_description= ''
        mrp= ''
        selling_price= ''
        in_stock= ''
        product_id= ''
        brandName= ''
        codValidOnCategory= ''
        shippingCharges= ''
        shippingDays= ''
        product_url= ''
        image_url= ''

        soup = BeautifulSoup(r.data.decode('utf-8'),"lxml")
        mainList = {}
        bc_list = list()
        if soup.find('div',{'id':'breadCrumbWrapper2'}) is not None:
            bread_crumb = soup.find('div',{'id':'breadCrumbWrapper2'})
            for crumbs in bread_crumb.find_all('a',{'class','bCrumbOmniTrack'}):
                cc = crumbs.text
                cc = cc.strip()
                bc_list.append(cc)
            bread_crumb = " > ".join(bc_list)

        if soup.find('input',{'id':'productNamePDP'}).attrs['value'] is not None:
            product_name =  soup.find('input',{'id':'productNamePDP'}).attrs['value'].strip()

        if soup.find('div',{'class':'detailssubbox'}) is not None:
            product_description = soup.find('div',{'class':'detailssubbox'}).text.strip()

        if soup.find('input',{'id':'productPrice'}).attrs['value'] is not None:
            selling_price = soup.find('input',{'id':'productPrice'}).attrs['value'].strip()

        if soup.find('input',{'id':'soldOut'}).attrs['value'] is not None:
            in_stock = soup.find('input',{'id':'soldOut'}).attrs['value'].strip()

        if in_stock == 'false':
            if soup.find('input',{'id':'productMrpForFbt'}) is not None:
                  mrp = soup.find('input',{'id':'productMrpForFbt'}).attrs['value'].strip()
            else:
                  mrp = selling_price

            #CALLING SHIPPING DETAILS
            supc = soup.find('div',{'id':'defaultSupc'}).text.strip()
            catId = soup.find('input',{'id':'catId'}).attrs['value'].strip()
            catUrl = soup.find('input',{'id':'catUrl'}).attrs['value'].strip()
            bn = soup.find('input',{'id':'brandName'}).attrs['value'].strip()
            url_shipping = BASE_URL+'/acors/json/v2/gvbps?supc='+supc+'&catId='+catId+'&pc='+PIN_CODE+'&catUrl='+catUrl+'&bn='+bn+'&start=0&count=1'
            url_shipping = re.sub(' ', '%20', url_shipping)
            r = http.request('GET',url_shipping,headers=headers)
            data = json.loads(r.data.decode('utf-8'))
            try:
                  shippingCharges = str(data['primaryVendor']['shippingCharges'])
                  shippingDays = str(data['primaryVendor']['otoDRange']['min'])+' to '+str(data['primaryVendor']['otoDRange']['max'])+' Days'
            except KeyError:
                  shippingCharges = 0
                  shippingDays = ''
        else:
            mrp = selling_price
            shippingCharges = 0
            shippingDays = ''
        #average_rating = soup.find('input',{'id':'avgRating'}).attrs['value'].strip()
        #no_of_rating = soup.find('input',{'id':'noOfRatings'}).attrs['value'].strip()

        if(in_stock =='false'):
            in_stock = 1
        else:
            in_stock = 0

        if soup.find('input',{'id':'pogId'}).attrs['value'] is not None:
            product_id = soup.find('input',{'id':'pogId'}).attrs['value'].strip()

        if soup.find('input',{'id':'brandName'}).attrs['value'] is not None:
            brandName = soup.find('input',{'id':'brandName'}).attrs['value'].strip()

        if soup.find('input',{'id':'codValidOnCategory'}).attrs['value'] is not None:
            codValidOnCategory = soup.find('input',{'id':'codValidOnCategory'}).attrs['value'].strip()

        if soup.find('input',{'id':'productPageUrl'}).attrs['value'] is not None:
            product_url = BASE_URL+soup.find('input',{'id':'productPageUrl'}).attrs['value'].strip()
            product_url = product_url+AFFILIATE_ID

        if soup.find('div',{'class','left-panel-carousel'}) is not None:
            image_url_div = soup.find('div',{'class','left-panel-carousel'})
            image_url = image_url_div.find_all('img')
            image_url = image_url[0].attrs['src'].strip()

        print(product_id)

        mainList['bread_crumb'] = str(bread_crumb)
        mainList['product_name'] = str(product_name)
        mainList['product_description'] = str(product_description)
        mainList['mrp'] = str(mrp)
        mainList['selling_price'] = str(selling_price)
        mainList['in_stock'] = str(in_stock)
        mainList['product_id'] = str(product_id)
        mainList['brandName'] = str(brandName)
        mainList['codValidOnCategory'] = str(codValidOnCategory)
        mainList['shippingCharges'] = str(shippingCharges)
        mainList['shippingDays'] = str(shippingDays)
        mainList['product_url'] = str(product_url)
        mainList['image_url'] = str(image_url)
        mainList['time_stmp'] = str(time_stmp)
        if product_id :
            storeDataIntoDB(mainList,product_id)


def storeDataIntoDB(mainList,product_id):
    print(mainList)
    with open('/snapdir/'+product_id+'.csv', 'wb') as myFile:
        myFile.write(mainList)

# call this method at the initial time for fetching data from the mysql#
def callInitProducts():
    if __name__ == '__main__':
        pool = mp.Pool()
        with open('/snapdir/' + sys.argv[1], 'r') as csvfile:
            urls = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for url in urls:
                try:
                    url_name = url[0]
                    print(url_name)
                    pool.apply_async(callEachProductsWithURL, args=(url_name,))
                except Exception as inst:
                    print(inst)
        pool.close()
        pool.join()
        print('end')


                      
callInitProducts()




