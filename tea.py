from slacker import Slacker

import random
import time

api_key = '<YOUR API KEY>'
icon_url = 'http://commsbusiness.co.uk/wp-content/uploads/2015/02/tea.jpg'

slack = Slacker(api_key)

tea_test_id = 'C041X0PD5'
tea_id = 'C041MRC1A'
id = tea_id
channel_name = '#tea'

one_min = 60

tea_requests = []
channel_history = []
decision_message = ', your turn to make tea'
announce_message = 'Enter your type of tea or coffee to start another round'

class TeaRequest(object):

    def __init__(self,message):
        self.username = get_user_name(message)
        self.text = message['text']
        self.user_id = message['user']

        self.strikes = 0
        if('please' in self.text.lower()):
            self.said_please = 'please' in self.text.lower()
            self.strikes += 1

        self.request = self.username + ' wants ' + self.text
        self.request.replace('please','')
        self.request.replace('Please','')

    def get_request(self):
        return self.request

    def get_username(self):
        return self.username

    def get_user_id(self):
        return self.user_id

    def strike(self):
        if self.strikes > 0 :
            self.strikes -= 1
            return False
        return True

def main():

    print 'Tea bot started'

    while True:

        post(announce_message)

        print 'listening for next round'

        while True:
            if check():
                break
            print 'checked to no prevail'
            time.sleep(one_min)

        post("3 minutes to place orders")
        time.sleep(one_min)
        post("2 minutes to place orders")
        time.sleep(one_min)
        post("1 minute to place orders")
        time.sleep(one_min)

        load_requests()

        if len(tea_requests)>0:
            tea_maker = make_decision(tea_requests)
            post_decision(tea_maker)

def update_channel_history():
    global channel_history
    channel_history = slack.channels.history(id).body['messages']

def check():
    update_channel_history()
    for message in channel_history:
        if announce_message in message['text']:
            return False
        if is_an_order(message):
            return True

def load_requests():
    global tea_requests
    tea_requests = []
    update_channel_history()
    for message in channel_history:
        if is_an_order(message):
            tea_requests.append(TeaRequest(message))
        if announce_message in message['text']:
            return

def get_private_channel_id(user_id):
    response = slack.im.open(user_id).body
    print response
    if response['ok']:
        return response['channel']['id']
    return 'D024BFF1M' # Theos user_id

def make_decision(tea_requests):
    for tea_request in tea_requests:
        print tea_request.get_request()
    while True :
        i = random.randrange( 0,len(tea_requests) )
        print 'i=', i
        if tea_requests[i].strike():
            return tea_requests[i]
        # post( tea_requests[i].get_username() + ' said please, so gets out of this one' )

def post_tea_requests(tea_requests):
    for tea_request in tea_requests:
        post(tea_request.get_request())

def is_an_order(message):
    return message['text'].startswith('tea') or message['text'].startswith('coffee')

def post_decision(tea_maker):
    user_id = tea_maker.get_user_id()
    private_channel_id = get_private_channel_id(user_id)

    print 'private_channel_id', private_channel_id

    slack.chat.post_message(private_channel_id,'You\'re up',username='Tea Master',icon_url=icon_url)
    for tea_request in tea_requests:
        slack.chat.post_message(private_channel_id,tea_request.get_request(),username='Tea Master',icon_url=icon_url)

def post(text):
    slack.chat.post_message(channel_name, text,username='Tea Master',
                            icon_url=icon_url)

def get_user_name(message):
    return slack.users.info(message['user']).body['user']['name']

if __name__ == '__main__':
    main()
