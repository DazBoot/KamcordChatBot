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
        
        self.authUsers = []
        self.commands = {}
        
        self.messageLog = []
        self.lastMessageScrape = []     
    
    def addAuthorizedUser( self, username ):
        if username not in self.authUsers:
            self.authUsers.append( username )
    
    def addCommand( self, command, message ):
        if command not in self.commands.keys():
            self.commands[ command ] = message
    
    def parseMessage( self, message ):
        print( message[ USERNAME_INDEX ] + ": " + message[ MESSAGE_INDEX ] )
        self.messageLog.append( message )
        
        if message[ MESSAGE_INDEX ] in self.commands.keys() and message[ USERNAME_INDEX ] in self.authUsers:
            sendMessage( self.driver, self.commands[ message[ MESSAGE_INDEX ] ] )
        
    def findMessageMatchPoint( self, scrapedMessages ):
        #Find find the index to current message match point, start by iterating backwards through the log
        for logIdx in range( len( self.messageLog ) - 1, -1, -1 ):
            
            #Compare against the messages in the last grab
            for msgIdx in range( 0, len( scrapedMessages ) ):
                
                #If the username and message are the same, we have a tentative match
                if( compareMessages( self.messageLog[ logIdx ], scrapedMessages[ msgIdx ] ) ):
                    return msgIdx
                    
        return 0
                    
    def checkForMessages( self ):
        
        #Grab all of the messages from the site
        currentMessages = getMessages( self.driver )
        
        matchPos = self.findMessageMatchPoint( currentMessages )                            
        for msgIdx in range( matchPos + 1, len( currentMessages ) ):
            self.parseMessage( currentMessages[ msgIdx ] )
    
    
    
if __name__ == "__main__":
    
    #Create the bot
    dazBot = DazBot( "https://www.kamcord.com/live/evolution590/chat" )

    #Add all of the users and commands
    dazBot.addAuthorizedUser( "evolution590" )
    dazBot.addAuthorizedUser( "DazBoot" )
    dazBot.addAuthorizedUser( "Gravithon" )
    
    dazBot.addCommand( "!test", "This is a test command!" )
    dazBot.addCommand( "!commands", "GET OUT OF HERE!" )

    
    #Connect and login
    time.sleep( 1 ) #Wait 1 second for the page to load before we continue
    sendMessage( dazBot.driver, "Test message from DazBot" )
    time.sleep( 1 ) #Wait 1 second for the login prompt before we continue
    login( dazBot.driver, USERNAME, PASSWORD )
    time.sleep( 1 ) #Wait 1 second for login to complete before we continue

    
    while( True ):
        dazBot.checkForMessages()
        time.sleep( 0.5 )