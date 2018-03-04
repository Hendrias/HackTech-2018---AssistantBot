from __future__ import print_function
import config
from slackclient import SlackClient
from quickstart import get_credentials
from quickstart import create_event
from quickstart import make_calendar
from quickstart import add_user

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime



class SlackBot(object):
    '''
    This is a wrapper for the slackclient library that you can use if you find
    helpful. Add methods as you see fit. Only a bot access token that starts
    with xoxb needs to be provided as an input argument.
    '''
    
    def __init__(self, access_token):
        self.sc = SlackClient(access_token)
        #name of the slack
        #self.team_calendar = ""
        #making the calendar with that slack's name
        make_calendar("dogs")

    def rtm_socket_connected(self):
        '''
        Checks if the bot is connected to the real time messaging socket, which
        allows it to monitor messages in the slack in real-time.
        '''
        return self.sc.rtm_connect()

    def send_message(self, message, channel):
        '''
        Sends a message to a channel. The message can be a formatted markdown
        message. The channel can be a DM, MPDM (multiple person DM), or a public
        or private channel.
        '''
        res = self.sc.api_call("chat.postMessage", channel=channel, text=message)
        return res

    def read_rtm_messages(self):
        '''
        Reads the incoming stream of real time messages from all channels the
        bot is a member of.
        '''
        res = self.sc.rtm_read()
        return res

    def handle_event(self, rtm_event):
        '''
        Handles all real time messaging events.
        '''

        if len(rtm_event) == 0:
            return

        event = rtm_event[0]

        # Right now, just handles the case where it replies to any message that
        # says "hello" with "hello there"
        if "type" in event and event["type"] == "message":
            channel = event["channel"]
            message = event["text"]

            if message == "hello":
                print("message sent was hello")
                self.send_message("hello there", channel)
            
            elif message == "see event":
                self.send_message("getting the calendars", channel)
                print('a0')
                credentials = get_credentials()
                print('a1')
                http = credentials.authorize(httplib2.Http())
                print('a2')
                service = discovery.build('calendar', 'v3', http=http)
                print('a3')
                now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
                print('a4')
                print('Getting the upcoming all events')
                eventsResult = service.events().list(
                    calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                    orderBy='startTime').execute()
                events = eventsResult.get('items', [])

                if not events:
                    print('No upcoming events found.')
                for event in events:
                    start = event['start'].get('dateTime', event['start'].get('date'))
                    print(start, event['summary'])
               
                print("looking at calendars")
               
            elif message == "make event":
                self.send_message("making the calendars", channel)
                print('c0')
                create_event()
                print('c1')


    def activate(self):
        '''
        Starts the bot, which monitors all messages events from channels it is a
        part of and then sends them to the message handler.
        '''

        if self.rtm_socket_connected():
            print("Bot is up and running\n")

            while True:
                try:
                    self.handle_event(self.read_rtm_messages())
                except:
                    continue
        else:
            print("Error, check access token!")

if __name__ == "__main__":
    bot = SlackBot(BOT_ACCESS_TOKEN)
    bot.activate()
