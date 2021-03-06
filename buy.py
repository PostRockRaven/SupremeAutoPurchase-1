#Created by Colin Cowie
import timeit
import time
import sys
import requests
import ConfigParser
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

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
countryfield = Config.get('Info', 'Countryfield')
city = Config.get('Info','City')
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
category = Config.get('Product','Category')
mainUrl = mainUrl + category
start = timeit.default_timer()
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
        #buyprd(prdurl)
        phantombuy(prdurl)
    #print('Product:'+product_Name+', Color:'+product_Color+', Link:'+Link)

def phantombuy(u):
    driver = webdriver.PhantomJS(port=8910, service_args=['--load-images=no'])
    driver.get(u)
    print('Phantom launched page: '+driver.current_url)
    #check what type selectOption is
    try:
        int(selectOption)
        select = Select(driver.find_element_by_xpath("//select[./option[contains(@value,%s)]]"%selectOption))
        print('selectOption is an int')
    except ValueError:
        select = Select(driver.find_element_by_xpath("//*[@id='size']"))
        print('selectOption is an string')

    #choose selectOption
    select.select_by_visible_text(selectOption)
    #add to cart
    driver.find_element_by_xpath("//*[@id='add-remove-buttons']/input").send_keys(Keys.ENTER)
    items_count = driver.find_element_by_xpath("//*[@id='items-count']")

    while items_count.text != '1 item':
        print('Loading...')
    if items_count.text == '1 item':
        print(items_count.text+ ' was added to cart!')
        driver.get(checkoutUrl)
        print(driver.current_url)
    else:
        print('Error')
    print("Filling Out Billing Info")
    driver.find_element_by_xpath('//*[@id="order_billing_name"]').send_keys(namefield)
    driver.find_element_by_xpath('//*[@id="order_email"]').send_keys(emailfield)
    driver.find_element_by_xpath('//*[@id="order_tel"]').send_keys(phonefield)

    print("Filling Out Address")
    driver.find_element_by_xpath('//*[@id="bo"]').send_keys(addressfield)
    driver.find_element_by_xpath('//*[@id="order_billing_zip"]').send_keys(zipfield)
    #Country Select
    country_select = Select(driver.find_element_by_xpath('//*[@id="order_billing_country"]'))
    country_select.select_by_value(countryfield)
    print("Filling Out Credit Card Info")
    #Type Select
    cctype_select = Select(driver.find_element_by_xpath('//*[@id="credit_card_type"]'))
    cctype_select.select_by_value(cctypefield)
    driver.find_element_by_xpath('//*[@id="cnb"]').click()
    driver.find_element_by_xpath('//*[@id="cnb"]').send_keys(ccnumfield)
    ##CC month and year select value
    ccmonth_select = Select(driver.find_element_by_xpath('//*[@id="credit_card_month"]'))
    ccmonth_select.select_by_value(ccmonthfield)
    ccyear_select = Select(driver.find_element_by_xpath('//*[@id="credit_card_year"]'))
    ccyear_select.select_by_value(ccyearfield)
    driver.find_element_by_xpath('//*[@id="vval"]').send_keys(cccvcfield)
    #TODO Fix
    if(countryfield=='USA'):
        driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p[2]/label/div/ins').click()
    else:
        driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
        driver.find_element_by_xpath('//*[@id="order_billing_city"]').send_keys(city)
    print("Submitting Info")
    driver.find_element_by_xpath('//*[@id="pay"]/input').send_keys(Keys.ENTER)
    #TODO CHECK FOR erors
    print("Done!")

    #driver.quit()
    stop = timeit.default_timer()
    print(str(stop-start) + ' Seconds')
    time.sleep(1)
    try:
        print('\n\n~~~ERROR~~~\n\n'+driver.find_element_by_xpath("//div[@id='cart-cc']//div[contains(@class,'errors')]").text+'\n')
    except Exception as e:
        print ('no payments errors found.')
    try:
        print('\n\n~~~ERROR~~~\n\n'+driver.find_element_by_xpath("//div[@id='cart-address']//div[contains(@class,'errors')]").text)
    except Exception as e:
        print ('no address errors found!')
    sys.exit(0)

i = 1
while (True):
    print("On try number " + str(i))
    main()
    i = i + 1
    time.sleep(3)
