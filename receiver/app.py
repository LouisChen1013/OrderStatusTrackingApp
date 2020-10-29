import connexion
import json
from connexion import NoContent
import requests
import yaml
import logging.config
from pykafka import KafkaClient
import datetime

with open('app_conf.yaml', 'r') as f:
    app_config = yaml.safe_load(f.read())
    url1 = app_config['add_order']['url']
    url2 = app_config['payment']['url']
    hostname = app_config['events']['hostname']
    port = str(app_config['events']['port'])
    config_topic = app_config['events']['topic']
    keys = list(app_config.keys())


with open('log_conf.yaml', 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')


def add_order(body):
    unique_id_order = body["customer_id"]
    logger.info(
        f"Received event {keys[1]} request with a unique id of {unique_id_order}")

    client = KafkaClient(hosts=hostname+':'+port)
    topic = client.topics[config_topic]
    producer = topic.get_sync_producer()
    msg = {"type": keys[1], "datetime": datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S"), "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event {keys[1]} response (Id: {unique_id_order})")

    return NoContent, 201


def payment(body):
    unique_id_payment = body["customer_id"]
    logger.info(
        f"Received event {keys[2]} request with a unique id of {unique_id_payment}")

    client = KafkaClient(hosts=hostname+':'+port)
    topic = client.topics[config_topic]
    producer = topic.get_sync_producer()
    msg = {"type": keys[2], "datetime": datetime.datetime.now().strftime(
        "%Y-%m-%dT%H:%M:%S"), "payload": body}
    msg_str = json.dumps(msg)
    producer.produce(msg_str.encode('utf-8'))

    logger.info(
        f"Returned event {keys[2]} response (Id: {unique_id_payment})")

    return NoContent, 201


app = connexion.FlaskApp(__name__, specification_dir='')

app.add_api("openapi.yaml", strict_validation=True, validate_responses=True)


if __name__ == "__main__":
    app.run(port=8080)
