from configparser import ConfigParser
import os
from cerberus import Validator


# check that modifier is either sum or mean
def modifier_type_check(field, value, error):
    if value not in ['sum', 'mean']:
        error(field, "Modifier must be of type \'sum\' or \'mean\'")


# specify a valid config schema
config_schema = {
    'name': {
        'type': 'string'
    },
    'elevation': {
        'type': 'integer',
        'min': 0
    },
    'latitude': {
        'type': 'string'
    },
    'longitude': {
        'type': 'string'
    },
    'skip_first_n': {
        'type': 'integer',
        'min': 1
    },
    'modify_values': {
        'type': 'boolean'
    },
    'interval_minutes': {
        'type': 'integer',
        'min': 1
    },
    'modifier': {
        'check_with': modifier_type_check
    }
}

# define a validator
config_validator = Validator(config_schema, require_all=True)


# parse values in config files to required types
def parse_config(config):
    config['elevation'] = int(config['elevation'])
    config['skip_first_n'] = int(config['skip_first_n'])
    config['modify_values'] = bool(config['modify_values'])
    config['interval_minutes'] = int(config['interval_minutes'])
    return config


def get_config(path, name):
    parser = ConfigParser(inline_comment_prefixes=";")
    file_name = name + "_config.txt"
    config_file_path = os.path.join(path, file_name)
    if os.path.isfile(config_file_path):
        parser.read(config_file_path)
        # read the station section
        station = dict(parser.items('station'))
        # read the data section
        data = dict(parser.items('data'))
        # combine to config dict
        config = {**station, **data}
        # parse values in dict
        config = parse_config(config)
        # validate the config with the schema
        valid = config_validator.validate(config)
        if not valid:
            raise ValueError(config_validator.errors)
        return config

    else:
        print("Config file {} not found in location. Using default values.".format(file_name))
        return get_default_values()


def get_default_values():
    # define default values for config
    return {
        "name": "unknown",
        "elevation": 0,
        "latitude": 0,
        "longitude": 0,
        "skip_first_n": 10,
        "modify_values": False,
        "interval_minutes": 1,
        "modifier": "sum"
    }


# generate a config.txt
def generate_default_config(file):
    default = get_default_values()
    f = open(file, "w+")
    f.write("[station]\n")
    f.write(f"name={default['name']}\n")
    f.write(f"elevation={default['elevation']}\n")
    f.write(f"latitude={default['latitude']}\n")
    f.write(f"longitude={default['longitude']}\n")
    f.write("\n")
    f.write("[data]\n")
    f.write(f"skip_first_n={default['skip_first_n']}\t; number of entries to be skipped. Set this number to at least "
            f"the number of header rows.\n")
    f.write(f"modify_values={default['modify_values']}\t; set this to True if you want to apply below modifiers to "
            f"the values \n")
    f.write(f"interval_minutes={default['interval_minutes']}\t; set this to the number of minutes for one interval\n")
    f.write(f"modifier={default['modifier']}\t; Possible values: mean => get the mean of the interval, sum => get "
            f"the sum of the interval\n")
    f.close()
