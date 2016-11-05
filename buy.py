#Created by Colin Cowie
import time
import sys
import requests
import ConfigParser
from bs4 import BeautifulSoup
from splinter import Browser

mainUrl = "http://www.supremenewyork.com/shop/all/"
baseUrl = "http://supremenewyork.com"
checkoutUrl = "https://www.supremenewyork.com/checkout"
# Randomly Generated Data (aka, this isn't mine)


Config = ConfigParser.ConfigParser()
Config.read('config.ini')
#Info
namefield = Config.get('Info','Name')
emailfield = Config.get('Info','Email')
phonefield = Config.get('Info','Phone')
addressfield = Config.get('Info','Address')
zipfield = Config.get('Info','Zipfield')
statefield = Config.get('Info','statefield')
#CreditCard
cctypefield = Config.get('CreditCard','cctype')
ccnumfield = Config.get('CreditCard','ccnum')
ccmonthfield = Config.get('CreditCard','ccmonth')
ccyearfield = Config.get('CreditCard','ccyear')
cccvcfield = Config.get('CreditCard','cvc')
#Product
product_name = Config.get('Product','Keyword')
product_color = Config.get('Product','Color')
selectOption = Config.get('Product','SelectOption')
Size = Config.get('Product','Size')
mainUrl = mainUrl+Config.get('Product','Category')

print("Information loaded from config.inin....\nChecking for product")


def main():
    r = requests.get(mainUrl).text
    if product_name in r:
        print("Product Found")
        parse(r)
    else:
        print("Product not found.")

def parse(r):
    soup = BeautifulSoup(r, "html.parser")
    for div in soup.find_all('div', { "class" : "inner-article" }):
        product = ""
        color = ""
        link = ""
        for a in div.find_all('a', href=True, text=True):
            link = a['href']
        for a in div.find_all(['h1','p']):
            if(a.name=='h1'):
                product = a.text
            elif(a.name=='p'):
                color = a.text
        checkproduct(link,product,color)

def checkproduct(Link,product_Name,product_Color):
    if(product_name in product_Name and product_color in product_Color):
        prdurl = baseUrl + Link
        print('\nTARGETED PRODUCT FOUND\n')
        print('Product: '+product_Name+'\n')
        print('Color: '+product_Color+'\n')
        print('Link: '+prdurl+'\n')
        print('Moving to next phase of purchase...\n')
        buyprd(prdurl)
    #print('Product:'+product_Name+', Color:'+product_Color+', Link:'+Link)

def buyprd(u):
    #executable_path = {'executable_path':'</Applications/Google Chrome.app>'}
    browser = Browser('firefox')
    url = u
    browser.visit(url)
    # 10|10.5
    browser.find_option_by_text(selectOption).first.click()
    browser.find_by_name('commit').click()
    if browser.is_text_present('item'):
        print("Added to Cart!")
    else:
        print("Error, most likely out of stock.")
        return
    print("checking out")
    browser.visit(checkoutUrl)
    print("Filling Out Billing Info")
    browser.fill("order[billing_name]", namefield)
    browser.fill("order[email]", emailfield)
    browser.fill("order[tel]", phonefield)

    print("Filling Out Address")
    browser.fill("order[billing_address]", addressfield)
    browser.fill("order[billing_zip]", zipfield)
    browser.select("order[billing_state]", statefield)
    print("Filling Out Credit Card Info")

    browser.select("credit_card[type]", cctypefield)
    browser.fill("credit_card[cnb]", ccnumfield)
    browser.select("credit_card[month]", ccmonthfield)
    browser.select("credit_card[year]", ccyearfield)
    browser.fill("credit_card[vval]", cccvcfield)
    browser.find_by_css('.terms').click()
    print("Submitting Info")
    browser.find_by_name('commit').click()
    sys.exit(0)




i = 1
while (True):
    print("On try number " + str(i))
    main()
    i = i + 1
    time.sleep(2)
