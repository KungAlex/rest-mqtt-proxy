import yaml
import os
from app import MQTTSubscriptionV1
from flask_restful import fields, marshal
import configparser

APP_CONFIG_FILE=(os.getenv('APP_CONFIG_FILE', 'config/dev/config.ini'))
PRE_MAPPING_DIR=(os.getenv('PRE_MAPPING_DIR', 'config/dev/mappings'))

# Test Config
config = configparser.ConfigParser()
config.read(APP_CONFIG_FILE)

print("#############")
print("Test Config")

for s in config.sections():
    print("---")
    print(s)
    print(config.items(s))

# Test Mapping
cwd = os.getcwd()

sub_fields = {
    'kind': fields.String,
    'uuid': fields.String,
    'subregex': fields.String,
    'description': fields.String,
    'event_handlers': fields.Raw,
    'labels': fields.Raw,
    'spec': fields.Raw,
}

subscriptions_list = []

for file in os.listdir(PRE_MAPPING_DIR):
    if file.endswith(".yaml") or file.endswith(".yml"):
        yaml_file = (os.path.join(PRE_MAPPING_DIR, file))
        with open(yaml_file, 'r') as stream:
            yamls = yaml.load_all(stream)
            for y in yamls:

                try:

                    kind = y['kind']

                    # TODO switch case!
                    if kind == "MQTTSubscriptionV1":
                        try:
                            sub = MQTTSubscriptionV1.load_yaml(yaml=y)
                            subscriptions_list.append(sub)

                        except yaml.YAMLError as exc:
                            print(exc)
                            # TODO exceptions description#

                    if kind == "MQTTSubscriptionV2":
                        try:
                            sub = MQTTSubscriptionV1.load_yaml(yaml=y)
                            subscriptions_list.append(sub)

                        except yaml.YAMLError as exc:
                            print(exc)
                            # TODO exceptions description#

                except KeyError as exc:
                    print("KeyError: " + str(exc))


def show_list():
    return [marshal(sub, sub_fields) for sub in subscriptions_list]


print("#############")
print("Test Mappping")
list = show_list()

for l in list:
    print("---")
    print(l)
    # print(l.keys())
    # print(l.values())
