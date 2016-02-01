import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import *

def sendMessage( driver, msg ):
    commentInput = driver.find_element_by_class_name( "live-comment-input" )
    commentInput.send_keys( msg )
    commentInput.submit()

if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get( "https://www.kamcord.com/live/DazBoot/chat" )
    
    #Send a dummy message to trigger the login prompt
    sendMessage( driver, "DummyMessage" )
    
    '''
    try:
        WebDriverWait( driver, 10 ).until( EC.presence_of_element_located(( By.XPATH, "//*[@id='username']" )) )
    finally:
        print( "Timed out waiting for the login popup to appear!" )
        driver.quit()
    '''
    
    time.sleep( 1 )
    
    #Enter the username and password
    usernameInput = driver.find_elements_by_name( "username" )[ 1 ]
    usernameInput.send_keys( USERNAME )
    
    passwordInput = driver.find_elements_by_name( "password" )[ 1 ]
    passwordInput.send_keys( PASSWORD )
    passwordInput.submit()
    
    time.sleep( 1 )
    
    #Send a dummy message to trigger the login prompt
    inputElement = driver.find_element_by_class_name("live-comment-input")
    inputElement.send_keys('This is a test message from DazBot!')
    inputElement.submit()