import json
import pika
import requests
import time


class DataCollector:
    def __init__(self):
        self.api_url = 'https://collectionapi.metmuseum.org/public/collection/v1/'
        self.object_ids = []

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='data_raw')

    def get_object_ids(self):
        response = requests.get(self.api_url + 'objects')
        return response.json()['objectIDs']

    def get_object_data(self, object_id):
        response = requests.get(self.api_url + 'objects/' + str(object_id))
        return response.json()

    def start_data_collection(self):
        self.object_ids = self.get_object_ids()
        for object_id in self.object_ids:
            data = self.get_object_data(object_id)
            self.channel.basic_publish(exchange='', routing_key='data_raw', body=json.dumps(data).encode('UTF-8'))

            time.sleep(1)
        self.start_data_collection()
