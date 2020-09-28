import yaml
import webbrowser
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

with open('creds.yaml',encoding="utf8") as file:
    data = yaml.load(file, Loader=yaml.SafeLoader)
    productUrl=(data['productUrl'])
    chromeDriverPath=(data['chromeDriverPath'])

print (productUrl)

def telegramNotify(msg):
   token=data['telegramToken']
   userId=data['telegramIdToNotify']
   msgUrl = "https://api.telegram.org/bot"+token+"/sendMessage?chat_id="+userId+"&text="+msg
   requests.get(msgUrl)
   print(msgUrl)
   return True

def waitAndClick(element,driver, sleep=0):
   time.sleep(sleep)
   for x in range(150):
      try:
         print("Looking for {} for the {} time".format(element, x))
         driver.find_element_by_xpath(element).click()
      except:
         time.sleep (0.1)
         if x == 100: #if tried 100 times and didn't find the button, refresh the page
            driver.refresh()
            time.sleep(5)
         continue
      print("clicking! "+element )
      return True
   exit()
   return False



def sendImage(img,userId,token):
    url = "https://api.telegram.org/bot"+token+"/sendPhoto"
    files = {'photo': open(img , 'rb')}
    data = {'chat_id' : userId}
    r= requests.post(url, files=files, data=data)
    print('Image sent')

def Main(driver):
   driver.get(productUrl)
   waitAndClick('//*[@id="product-addtocart-button"]', driver, 5)
   telegramNotify("I've added a product to the cart!")
   driver.get("https://www.kravitz.co.il/edea/cart/")
   #todo: add check that cart has 1 item
   # time.sleep(5)
   # print("trying to get text from box")
   # text = driver.find_element_by_xpath('/html/body/div[3]/main/div/div[2]/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[4]/div/div/input').getText("my text")
   # print("The text I got is:{}".format(text))

   waitAndClick('//*[@id="cart-summary"]/div[1]/ul/li/button', driver)
   time.sleep(5)
   waitAndClick('//*[@id="checkout-shipping-method-load"]/div/div/input', driver)
   driver.find_element_by_xpath('//*[@id="customer-email"]').send_keys(data['email'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[1]/div/input').send_keys(data['name'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[3]/div/input').send_keys(data['city'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[1]/div/input').send_keys(data['street'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[2]/div/input').send_keys(data['homeNumber'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[3]/div/input').send_keys(data['aptNumber'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[7]/div/input').send_keys(data['phoneNumber'])
   # driver.find_elements_by_xpath

   #payment
   waitAndClick('html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[3]/div/button', driver)
   time.sleep(15)
   driver.switch_to.frame(0)
   print("switched frames!!!")
   waitAndClick('//*[@id="date_month_input"]/option[{}]'.format(data['expiryMonth']), driver)
   waitAndClick('//*[@id="date_year_input"]/option[{}]'.format(data['expiryYear']), driver) #2019 is option1, going up. = year - 2018
   driver.find_element_by_xpath('//*[@id="id_number_input"]').send_keys(data['taz'])
   driver.find_element_by_xpath('//*[@id="credit_card_number_input"]').send_keys(data['creditCard'])
   driver.find_element_by_xpath('//*[@id="cvv_input"]').send_keys(data['ccv'])
   driver.find_element_by_xpath('//*[@id="submitBtn"]').click()
   
   with open('status.txt', 'w') as statusFile:
      statusFile.write('done')
   currentTime = time.strftime("%H.%M.%S", time.localtime())
   imgPath = currentTime+".png"
   time.sleep(15) # sleep in order to acount for purchesing time before screenshot
   driver.save_screenshot(imgPath)
   print('Taking screenshot')
   sendImage(imgPath,data['telegramIdToNotify'],data['telegramToken'])
   return True    


#----------------------------------------------- MAIN
tryCounter=1
# driver = webdriver.Chrome(chromeDriverPath)
while True:
   print("Trying to run the script for  the {}nd time".format(tryCounter))
   with open('status.txt') as f:
      statusLine = f.readline()
   if statusLine != 'done':
      try:
         driver = webdriver.Chrome(chromeDriverPath)
         Main(driver)
         print("Done! Hopefully you got the product you wanted")
      except:
         driver.quit()
         tryCounter+=1
         continue
      exit(0)
   else:
      print("You already got the product! Exiting")
      exit(0)
         
