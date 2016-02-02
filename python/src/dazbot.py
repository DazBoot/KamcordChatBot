import time
from config import *
from kamcordutils import *
from messages import MessageManager

USERNAME_INDEX = 0
MESSAGE_INDEX = 1

def compareMessages( firstMessage, secondMessage ):
    return firstMessage[ USERNAME_INDEX ] == secondMessage[ USERNAME_INDEX ] and firstMessage[ MESSAGE_INDEX ] == secondMessage[ MESSAGE_INDEX ]

class DazBot( object ):
    def __init__( self, streamUrl ):
        
        #Create the driver
        self.driver = webdriver.Firefox()
        self.driver.get( streamUrl )
        
        #Give the driver a chance to connect
        time.sleep( 2 )
        
        self.authUsers = []
        self.commands = {}
        
        self.messageManager = MessageManager( getMessages( self.driver ) )
        self.messageLog = []
        self.lastMessageScrape = []     
    
    def addAuthorizedUser( self, username ):
        if username not in self.authUsers:
            self.authUsers.append( username )
    
    def addCommand( self, command, message ):
        if command not in self.commands.keys():
            self.commands[ command ] = message
    
    def parseMessage( self, message ):
        if message.message in self.commands.keys() and message.username in self.authUsers:
            sendMessage( self.driver, self.commands[ message.message ] )
        
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
        newMessages = self.messageManager.processMessages( getMessages( self.driver ) )
        
        for msg in newMessages:
            self.parseMessage( msg )

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