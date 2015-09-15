import sys
import os
import time
import random
import Skype4Py
import markovify
from chatterbot import ChatBot
import trainer

# Read text file, replace new lines with spaces, and save to variable
with open ("padula.txt", "r") as myfile:
      padula_text=myfile.read().replace('\n', ' ')

# Build the model.
text_model = markovify.Text(padula_text)

# Create Chatterbot Instance
chatbot = ChatBot('Padula')
trainer.TrainDefault(chatbot)

# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in
#case.
def OnAttach(status):
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach()

    if status == Skype4Py.apiAttachSuccess:
       print('***************************************')
       print('Type "markov" to generate sentences')
       print('Type "exit" to quit')
       print('Type "help" for help')
       
# Fired on chat message status change.
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'

def OnMessageStatus(Message, Status):
    if Status == 'RECEIVED':
        print(Message.FromHandle + ': ' + Message.Body)
        markov_orNot = random.randint(0, 11) # generates a number in the range of 0 and 11.
        if markov_orNot == 5: # if the number is 5, print a markov sentence as a reply.
            print("Markov! Choo-Choo!")
            response = text_model.make_sentence()
            skype.SendMessage(Message.FromHandle, response)
        else:
            print("Chatbot is thinking...")
            response = chatbot.get_response(Message.Body)
            skype.SendMessage(Message.FromHandle, response)
        
    if Status == 'READ':
        print(Message.FromDisplayName + ': ' + Message.Body)

    if Status == 'SENT':
        print('Message Delivered.')

# Creating instance of Skype object, assigning handler functions and attaching to Skype.
skype = Skype4Py.Skype()
skype.OnAttachmentStatus = OnAttach
skype.OnMessageStatus = OnMessageStatus

print('***************************************')
print 'Connecting to Skype..'
skype.Attach()

# Looping until user types 'exit'
Cmd = ''
while not Cmd == 'exit' and not Cmd == 'quit':
    Cmd = raw_input('User/: ')
    if Cmd == 'markov':
        for i in range(50):
            print(text_model.make_sentence())
            next
    if Cmd == 'help':
       print('Type "markov" to generate sentences')
       print('Type "exit" to quit')
       print('Type "help" for help')
       next
