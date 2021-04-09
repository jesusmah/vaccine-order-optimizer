import json, time, os, datetime, uuid
from server.infrastructure.kafka.KafkaAvroProducer import KafkaAvroProducer
import server.infrastructure.kafka.EventBackboneConfig as EventBackboneConfig
import server.infrastructure.kafka.avroUtils as avroUtils

class DataProducer:
    """ 
    This class is meant to be instantiated once when the application starts up in order
    to producer test data to the Kafka Topics
    """
    def __init__(self):
        print("[DataProducer] - Initializing the data producers")
        # Get the data events file locations
        self.inventory_file = "/app/data/txt/inventory.txt"
        self.reefer_file = "/app/data/txt/reefer.txt"
        self.transportation_file = "/app/data/txt/transportation.txt"
        # Get the events Avro data schemas location
        self.schemas_location = "/app/data/avro/schemas/"
        # self.cloudEvent_schema = self.inventory_schema = avroUtils.getCloudEventSchema(self.schemas_location,"cloudEvent.avsc","inventory.avsc","reefer.avsc","transportation.avsc")
        self.cloudEvent_schema = avroUtils.getCloudEventSchema()
        print(self.cloudEvent_schema.to_json())
        # Build the Kafka Avro Producers
        self.kafkaproducer_inventory = KafkaAvroProducer("DataProducer_Inventory",json.dumps(self.cloudEvent_schema.to_json()),"VOO-Inventory")
        self.kafkaproducer_reefer = KafkaAvroProducer("DataProducer_Reefer",json.dumps(self.cloudEvent_schema.to_json()),"VOO-Reefer")
        self.kafkaproducer_transportation = KafkaAvroProducer("DataProducer_Transportation",json.dumps(self.cloudEvent_schema.to_json()),"VOO-Transportation")

    def produceData(self):
        self.produceInventoryData(EventBackboneConfig.getInventoryTopicName())
        self.produceReeferData(EventBackboneConfig.getReeferTopicName())
        self.produceTransportationData(EventBackboneConfig.getTransportationTopicName())

    def produceInventoryData(self,topic):
        print("[DataProducer] - Producing events in " + self.inventory_file)
        if os.path.isfile(self.inventory_file):
            with open(self.inventory_file) as f:
                lines = [line.rstrip() for line in f]
            for event in lines:
                event_json = {}
                event_json['type'] = "ibm.gse.eda.vaccine.orderoptimizer.VaccineOrderCloudEvent"
                event_json['specversion'] = "1.0"
                event_json['source'] = "Vaccine Order Optimizer producer endpoint"
                event_json['id'] = str(uuid.uuid4())
                event_json['time'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                event_json['dataschema'] = "https://raw.githubusercontent.com/ibm-cloud-architecture/vaccine-order-optimizer/master/data/avro/schemas/inventory.avsc"
                event_json['datacontenttype'] =	"application/json"
                event_json['data'] = json.loads(event)
                # We might want to publish events with the inventory 'lot_id' field as the key for better partitioning
                # self.kafkaproducer_inventory.publishEvent(event_json['id'],event_json,topic)
                self.kafkaproducer_inventory.publishEvent(event_json['data']['lot_id'],event_json,topic)
        else:
            print('[DataProducer] - ERROR - The file ' + self.inventory_file + ' does not exist')
    
    def produceReeferData(self,topic):
        print("[DataProducer] - Producing events in " + self.reefer_file)
        if os.path.isfile(self.reefer_file):
            with open(self.reefer_file) as f:
                lines = [line.rstrip() for line in f]
            for event in lines:
                event_json = {}
                event_json['type'] = "ibm.gse.eda.vaccine.orderoptimizer.VaccineOrderCloudEvent"
                event_json['specversion'] = "1.0"
                event_json['source'] = "Vaccine Order Optimizer producer endpoint"
                event_json['id'] = str(uuid.uuid4())
                event_json['time'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                event_json['dataschema'] = "https://raw.githubusercontent.com/ibm-cloud-architecture/vaccine-order-optimizer/master/data/avro/schemas/reefer.avsc"
                event_json['datacontenttype'] =	"application/json"
                event_json['data'] = json.loads(event)
                # We might want to publish events with the reefer 'reefer_id' field as the key for better partitioning
                # self.kafkaproducer_reefer.publishEvent(event_json['id'],event_json,topic)
                self.kafkaproducer_reefer.publishEvent(event_json['data']['reefer_id'],event_json,topic)
        else:
            print('[DataProducer] - ERROR - The file ' + self.reefer_file + ' does not exist')
    
    def produceTransportationData(self,topic):
        print("[DataProducer] - Producing events in " + self.transportation_file)
        if os.path.isfile(self.transportation_file):
            with open(self.transportation_file) as f:
                lines = [line.rstrip() for line in f]
            for event in lines:
                event_json = {}
                event_json['type'] = "ibm.gse.eda.vaccine.orderoptimizer.VaccineOrderCloudEvent"
                event_json['specversion'] = "1.0"
                event_json['source'] = "Vaccine Order Optimizer producer endpoint"
                event_json['id'] = str(uuid.uuid4())
                event_json['time'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
                event_json['dataschema'] = "https://raw.githubusercontent.com/ibm-cloud-architecture/vaccine-order-optimizer/master/data/avro/schemas/transportation.avsc"
                event_json['datacontenttype'] =	"application/json"
                event_json['data'] = json.loads(event)
                # We might want to publish events with the transportation 'lane_id' field as the key for better partitioning
                # self.kafkaproducer_transportation.publishEvent(event_json['id'],event_json,topic)
                self.kafkaproducer_transportation.publishEvent(event_json['data']['lane_id'],event_json,topic)
        else:
            print('[DataProducer] - ERROR - The file ' + self.transportation_file + ' does not exist')
