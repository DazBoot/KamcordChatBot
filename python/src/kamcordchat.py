import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from config import *

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get( "https://www.kamcord.com/live/evolution590/chat" )
    
    #Send a dummy message to trigger the login prompt
    inputElement = driver.find_element_by_class_name("live-comment-input")
    inputElement.send_keys('DummyMessage')
    inputElement.submit()
   
    time.sleep( 5 )
    
    print( "Test message" )
    
    #Enter the username and password
    usernameInput = driver.find_element_by_id( "username" )
    usernameInput.send_keys( USERNAME )
    
    passwordInput = driver.find_element_by_id( "password" )
    passwordInput.send_keys( PASSWORD )
    passwordInput.submit()
    
    #Send a dummy message to trigger the login prompt
    inputElement = driver.find_element_by_class_name("live-comment-input")
    inputElement.send_keys('This is a test message from DazBot!')
    inputElement.submit()