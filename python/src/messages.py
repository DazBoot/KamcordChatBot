from kamcordutils import *

def checkMessageMatch( firstList, secondList ):
    for idx in range( 0, len( firstList ) ):
        if not firstList[ idx ].compareTo( secondList[ idx ] ):
            return False
    return True

class Message( object ):
    def __init__( self, message, username, timestamp ):
        self.message = message
        self.username = username
        self.timestamp = timestamp
        
    def __str__( self ):
        return self.timestamp + " [" + self.username + "] " + self.message
        
    def __repr__( self ):
        return self.timestamp + " [" + self.username + "] " + self.message
        
    def compareTo( self, msg ):
        #print( "Comparing: " + self.message + " to " + msg.message )
        return self.message == msg.message and self.username == msg.username

class MessageManager( object ):
    def __init__( self, initialMessages ):
        self.messageLog = []
        
        #Get the initial set of messages, so we don't act on them
        for msg in initialMessages:
            self.addMessageToLog( msg )
    
    def addMessageToLog( self, msg ):
        print( msg.username + ": " + msg.message )
        self.messageLog.append( msg )
    
    def processMessages( self, curMsgList ):        
        newMessages = []
        
        #invert the list, so it's easier to iterate over
        curMsgList = curMsgList[::-1]
        
        #Get the last message that we need to be comparing against
        lastMsg = self.messageLog[-1]
        
        #Iterate through the scraped list
        for idx in range( 0, len( curMsgList ) ):
            testMsg = curMsgList[ idx ]
            
            #Check to see if this is a potential match
            if lastMsg.compareTo( testMsg ):
 
                #Grab the rest of the scrape, if it is a match, it should sync with the scrape
                testScrapeSection = curMsgList[idx:]
           
                #Invert the log, since we inverted the scrape as well
                testLogSection = self.messageLog[::-1]

                #If we do have a match, log the message
                if checkMessageMatch( testScrapeSection, testLogSection ):
                    for message in curMsgList[0:idx]:
                        newMessages.append( message )
                    break
        
        #Un invert before we do anything
        newMessages = newMessages[::-1]
        for message in newMessages:
            self.addMessageToLog( message )
        
        return newMessages