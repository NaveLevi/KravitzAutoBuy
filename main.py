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
#    https://api.telegram.org/bot1080960104:AAGZXaVIX--d5xR7D3d_hqXuA4OED_9Iz_0/sendMessage?chat_id=47976441&text=reeee
   return True
# telegramNotify(telegramToken, telegramIdToNotify, 'reeeee')

def waitAndClick(element):
   time.sleep(5)
   for x in range(150):
      print(x)
      try:
         driver.find_element_by_xpath(element).click()
      except:
         time.sleep (0.1)
         continue
      print("clicking clickme!")
      return True
   return False

#----------------------------------------------- MAIN
while True: #todo: move everything to try
   driver = webdriver.Chrome(chromeDriverPath)
   driver.get(productUrl)

   waitAndClick('//*[@id="product-addtocart-button"]')
   telegramNotify("I've added a product to the cart!")
   driver.get("https://www.kravitz.co.il/edea/cart/")
   #todo: add check that cart has 1 item
   waitAndClick('//*[@id="cart-summary"]/div[1]/ul/li/button')
   time.sleep(5)
   driver.find_element_by_xpath('//*[@id="customer-email"]').send_keys(data['email'])
   
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[1]/div/input').send_keys(data['name'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[3]/div/input').send_keys(data['city'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[1]/div/input').send_keys(data['street'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[2]/div/input').send_keys(data['homeNumber'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/fieldset/div/div[3]/div/input').send_keys(data['aptNumber'])
   driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[1]/div[2]/form[2]/div/div[7]/div/input').send_keys(data['phoneNumber'])
   waitAndClick('//*[@id="checkout-shipping-method-load"]/div/div/input')
   # driver.find_elements_by_xpath

   #payment
   waitAndClick('html/body/div[2]/main/div/div/div[2]/div[2]/div[4]/ol/li[2]/div/div[3]/form/div[3]/div/button')
   time.sleep(15)
   driver.switch_to.frame(0)
   print("switched frames!!!")
   driver.find_element_by_xpath('//*[@id="id_number_input"]').send_keys(data['taz'])
   driver.find_element_by_xpath('//*[@id="credit_card_number_input"]').send_keys(data['creditCard'])
   driver.find_element_by_xpath('//*[@id="cvv_input"]').send_keys(data['ccv'])
   driver.find_element_by_xpath('//*[@id="submitBtn"]').click()
   # waitAndClick('//*[@id="id_number_input"]')
   # driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[1]/div[1]/div/div/input').send_keys(data['creditCard'])
   # driver.find_element_by_xpath('/html/body/div[1]/div[4]/div/div/div[2]/div[2]/div/div/input').send_keys(data['ccv'])
   # <input autocomplete="off" class="required form-control" id="id_number_input" inputmode="text" maxlength="9" name="CreditCardHoldIder" type="text" value="">
   # waitAndClick('//*[@id="id_number_input"]')
   # WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'//*[@id="credit_card_number_input"]')))
   # WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='number' and @id='credit-card-number']"))).send_keys("1234567890987654")

   time.sleep(5)
   # find_all_iframes(driver)
   # iframes = driver.find_elements_by_xpath("//iframe")
   # print(iframes)
   # driver.switch_to.frame(iframes[0])
   

   time.sleep(20)

   

   time.sleep(100)
   exit()
