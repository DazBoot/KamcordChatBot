
import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from config import *


def login( driver, username, password ):
    usernameInput = driver.find_elements_by_name( "username" )[ 1 ]
    usernameInput.send_keys( USERNAME )
    
    passwordInput = driver.find_elements_by_name( "password" )[ 1 ]
    passwordInput.send_keys( PASSWORD )
    passwordInput.submit()

    
def sendMessage( driver, msg ):
    commentInput = driver.find_element_by_class_name( "live-comment-input" )
    commentInput.send_keys( msg )
    commentInput.submit()

def cleanMessage( myMsg ):
    myMsg = myMsg.encode(sys.stdout.encoding, errors='replace')
    myMsg = myMsg.decode(sys.stdout.encoding)
    return myMsg
    
def getMessages( driver ):
    messageClasses = driver.find_elements_by_class_name( "live-comment" )
    authorClasses = driver.find_elements_by_class_name( "live-comment--author" )
    systemMessages = driver.find_elements_by_class_name( "live-comment__system")
    
    messageList = []
    
    #iterate through all the messages
    for idx in range(0, len(messageClasses)):
      
        if messageClasses[idx] in systemMessages:
            authorClasses.insert(idx, "system")
            author = authorClasses[idx]
            message = cleanMessage(messageClasses[idx].text)
        
        else:
            #find the username of the message
            author = cleanMessage(authorClasses[idx].text)
            # finds the entire contents of live-comment, includes username
            fullMessage = messageClasses[idx].text
            # strip username from the front of the message
            message = cleanMessage(fullMessage[len(author):])
    
        messageList.append([author, message ])

    return messageList
    
if __name__ == "__main__":
    driver = webdriver.Firefox()
    driver.get( "https://www.kamcord.com/live/DazBoot/chat" )
    
    #Send a dummy message to trigger the login prompt
    sendMessage( driver, "DummyMessage" )
    
    #TODO: Ideally we would wait for this to be visable instead of using a sleep
    '''
    try:
        WebDriverWait( driver, 10 ).until( EC.presence_of_element_located(( By.XPATH, "//*[@id='username']" )) )
    finally:
        print( "Timed out waiting for the login popup to appear!" )
        driver.quit()
    '''
    
    time.sleep( 1 )
    
    login( driver, USERNAME, PASSWORD )
    
    time.sleep( 1 )
    
    print(getMessages(driver))
    
    #Send a dummy message to trigger the login prompt
    sendMessage( driver, "This is a test message from DazBoot!" )
