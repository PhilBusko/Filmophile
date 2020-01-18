"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
MOVIES CHANNELS CONSUMERS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        print('ws connect')

        # Join room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name,
        #     self.channel_name
        # )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        text = text_data_json['text']

        print('receive')
        print(text)

        # send message to frontend
        # self.send(text_data=json.dumps({
        #     'type': 'from receive to front',
        #     'text': 'from receive to front',
        #     'data': 50,
        # }))

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
            'type': 'from receive',
            'text': 'from receive',
            'data': 10,
            }
        )

    # Receive message from room group
    # event: object from sender
    def chat_message(self, event):

        print('chat_message')
        print(event)

        message = event['text']

        # Send message to WebSocket
        # self.send(text_data=json.dumps({
        #     'message': message
        # }))

        self.send(text_data=json.dumps({
            'type': 'from room group',
            'text': 'from room group',
            'data': 100,
        }))

