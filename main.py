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



def screenshotAndSend():
   currentTime = time.strftime("%H.%M.%S", time.localtime())
   imgPath = 'screenshot-'+currentTime+".png"
   driver.save_screenshot(imgPath)
   print('Taking screenshot')

   url = "https://api.telegram.org/bot"+data['telegramToken']+"/sendPhoto"
   files = {'photo': open(imgPath , 'rb')}
   dataToSend = {'chat_id' : data['telegramIdToNotify']}
   requests.post(url, files=files, data=dataToSend)
   print('Image sent')


def Main(driver):
   driver.get(productUrl)
   waitAndClick('//*[@id="product-addtocart-button"]', driver, 5)
   telegramNotify("I've added a product to the cart!")
   driver.get("https://www.kravitz.co.il/edea/cart/")
   time.sleep(10)
   #checking if the price is right
   print("trying chartSum")
   #todo: dinamically wait for the element to load and remove sleep from above (order sum box)
   chartSum = driver.find_element_by_xpath('/html/body/div[2]/main/div/div[2]/div/div[2]/div[1]/div[2]/div[1]/div[1]/div/div/div[4]/div[2]/strong/span').text
   chartSum = ''.join(filter(str.isdigit, chartSum))[:-2]
   print("The chart sum is:{}, vailidating that it's the expected price".format(chartSum))
   if chartSum == data['expectedPrice']:
      print("Expected price of {} was matched! continueing".format(data['expectedPrice']))
      telegramNotify("Expected price of {} was matched! continueing".format(data['expectedPrice']))
   else:
      print("Expected price was not matched. expected:{}, actual price:{}".format(data['expectedPrice'], chartSum))
      telegramNotify("Expected price was not matched. expected:{}, actual price:{}".format(data['expectedPrice'], chartSum))
      screenshotAndSend()
      exit(1)
   

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
   telegramNotify("Congratz! you got the product and will most likely get a picture of the purchase in 15 seconds")
   time.sleep(15) # sleep in order to acount for purchesing time before screenshot
   screenshotAndSend()
   return True    


#----------------------------------------------- MAIN
tryCounter=1
while True:
   print("Trying to run the script for  the {}nd time".format(tryCounter))
   with open('status.txt') as f:
      statusLine = f.readline()
   if statusLine != 'done':
      try:
         #todo: we might want to open in the background every time
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
         
