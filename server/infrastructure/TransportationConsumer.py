import json, threading, time
from userapp.server.infrastructure.kafka.KafkaConsumer import KafkaConsumer
import userapp.server.infrastructure.kafka.EventBackboneConfig as EventBackboneConfig
import pandas as pd

class TransportationConsumer:
    """ 
    This class is meant to be instantiated once when the application starts up in order
    to consume events from the Kafka Topics
    """
    def __init__(self):
        print("[TransportationConsumer] - Initializing the consumer")
        self.events_panda={}
        self.events={}
        self.index=0
        self.kafkaconsumer=KafkaConsumer(EventBackboneConfig.getTransportationTopicName())
        self.kafkaconsumer.prepareConsumer('TransportationConsumer')

    def startProcessing(self):
        x = threading.Thread(target=self.processEvents, daemon=True)
        print("[TransportationConsumer] - Starting to consume Events")
        x.start()
    
    def processEvents(self):
        while True:
            event = self.kafkaconsumer.pollNextRawEvent()
            if event is not None:
                print('[TransportationConsumer] - New event consumed: ' + event.value().decode('utf-8'))
                event_json = json.loads(event.value().decode('utf-8'))
                if ( len(self.events_panda) == 0 ):
                    for key, value in event_json.items():
                        self.events_panda[key] = {0:value}
                    self.index+=1
                else:
                    for key, value in event_json.items():
                        intermediate = self.events_panda[key]
                        intermediate[self.index] = value
                        self.events_panda[key] = intermediate
                    self.index+=1
                self.events[event.key().decode('utf-8')] = json.loads(event.value().decode('utf-8'))
            # time.sleep(1)
    
    def getEvents(self):
        return self.events
    
    def getEventsPanda(self):
        return pd.DataFrame.from_dict(self.events_panda)