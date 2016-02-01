import time
from config import *
from kamcordchat import *

USERNAME_INDEX = 0
MESSAGE_INDEX = 1

def compareMessages( firstMessage, secondMessage ):
    return firstMessage[ USERNAME_INDEX ] == secondMessage[ USERNAME_INDEX ] and firstMessage[ MESSAGE_INDEX ] == secondMessage[ MESSAGE_INDEX ]

class DazBot( object ):
    def __init__( self, streamUrl ):
        
        #Create the driver
        self.driver = webdriver.Firefox()
        self.driver.get( streamUrl )
        
        
        self.messageLog = []
        self.lastMessageScrape = []     
        
    def parseMessage( self, message ):
        print( message[ USERNAME_INDEX ] + ": " + message[ MESSAGE_INDEX ] )
        
    def checkForMessages( self ):
        
        #Grab all of the messages from the site
        currentMessages = getMessages( self.driver )
        
        matchPos = 0
        
        newMessages = []
        
        #Find find the index to current message match point, start by iterating backwards through the log
        for logIdx in range( len( self.messageLog ) - 1, -1, -1 ):
            
            #Compare against the messages in the last grab
            for msgIdx in range( 0, len( currentMessages ) ):
                
                #If the username and message are the same, we have a tentative match
                if( compareMessages( self.messageLog[ logIdx ], currentMessages[ msgIdx ] ) ):
                    matchPos = msgIdx
                    
                    #Iterate backwards through the last scrape to confirm
                    for testMsgIdx in range( msgIdx, -1, -1 ):
                        logMessage = self.messageLog[ logIdx - ( testMsgIdx - msgIdx ) ]
                        scrapeMessage = currentMessages[ testMsgIdx ]
                        if( compareMessages( logMessage, scrapeMessage ) == False ):
                            matchPos = 0
                            break
                            
        for msgIdx in range( matchPos, len( currentMessages ) ):
            self.parseMessage( currentMessages[ msgIdx ] )
    
if __name__ == "__main__":
    dazBot = DazBot( "https://www.kamcord.com/live/DazBoot/chat" )
    time.sleep( 1 ) #Wait 1 second for the page to load before we continue
    sendMessage( dazBot.driver, "Test message from DazBot" )
    time.sleep( 1 ) #Wait 1 second for the login prompt before we continue
    login( dazBot.driver, USERNAME, PASSWORD )
    time.sleep( 1 ) #Wait 1 second for login to complete before we continue
    
    while( True ):
        dazBot.checkForMessages()
        time.sleep( 0.5 )