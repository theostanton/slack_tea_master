from slacker import Slacker

import random
import time

slack = Slacker('<API-Token>')

tea_requests = []

def main():

    # while True:
    #     check()
    #     time.sleep(60*5)

    check()
    post_tea_requests(tea_requests)
    if len(tea_requests)>0:
        message = make_decision(tea_requests)
        post_decision(message)

def check():
    channel_history = slack.channels.history("C041MRC1A")
    for message in channel_history.body['messages']:
        if message['text'].startswith('Enter your type of tea or coffee to start another round'):
            break

        if message['text'].startswith('tea') or message['text'].startswith('coffee'):
            tea_requests.append(message)

def make_decision(tea_requests):
    i = random.randrange( 0,len(tea_requests) )
    return tea_requests[i]

def post_tea_requests(tea_requests):
    for tea_request in tea_requests:
        post(get_user_name(tea_request) + ' wants ' + tea_request['text'])

def post_decision(message):
    text =  'natalie is up'
    print text
    post(text)
    post("Enter your type of tea or coffee to start another round")

def post(text):
    slack.chat.post_message('#tea', text,username='Tea Master',
                            icon_url='http://commsbusiness.co.uk/wp-content/uploads/2015/02/tea.jpg')

def get_user_name(message):
    return slack.users.info(message['user']).body['user']['name']

if __name__ == '__main__':
    main()
