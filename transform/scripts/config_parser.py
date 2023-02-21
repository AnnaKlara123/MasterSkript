from configparser import ConfigParser
import os
from cerberus import Validator


# check that modifier is either sum or mean
def modifier_type_check(field, value, error):
    if value not in ['sum', 'mean']:
        error(field, "Modifier must be of type \'sum\' or \'mean\'")

# Original ##
def nan_value_identifier_check(field, value, error):
    if value != '-' and not type(value) == list:
        error(field, "NanValueIdentifier must be \'-\' or of type integer.")

## Alternative ##
# def nan_value_identifier_check(field, value, error):
#     if not (value == '-' or (isinstance(value, list) and all(isinstance(x, int) for x in value))):
#         error(field, "NanValueIdentifier must be \'-\', an integer, or a list of integers.") 



def nan_value_replacement_check(field, value, error):
    if value != 'NaN' and not isinstance(value, int):
        error(field, "NanValueReplacement must be \'NaN\' or of type integer.")


# specify a valid config schema
config_schema = {
    'name': {
        'type': 'string'
    },
    'elevation': {
        'type': 'float',
        'min': 0.0
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
        'type': 'string',
        'check_with': modifier_type_check
    },
    'replace_nan_values': {
        'type': 'boolean'
    },
    'nan_value_identifier': {
        'check_with': nan_value_identifier_check
    },
    'nan_value_threshold': {
        'type': 'float'
    },
    'nan_value_replacement': {
        'check_with': nan_value_replacement_check
    }
}

# define a validator
config_validator = Validator(config_schema, require_all=True)

## Orginal parser
## parse values in config files to required types
# def parse_config(config):
#     config['elevation'] = int(config['elevation'])
#     config['skip_first_n'] = int(config['skip_first_n'])
#     config['modify_values'] = config['modify_values'] == 'True'
#     config['replace_nan_values'] = config['replace_nan_values'] == 'True'
#     config['interval_minutes'] = int(config['interval_minutes'])
#     ident = config['nan_value_identifier']
#     if ident != '-':                
#         ident_arr = ident.split(',')
#         config['nan_value_identifier'] = [float(x) for x in ident_arr]
#     if config['nan_value_replacement'] != 'NaN':
#         config['nan_value_replacement'] = int(config['nan_value_replacement'])
#     return config

###### Works fine with '-' and list of Int.  ##########
def parse_config(config):
    config['elevation'] = int(config['elevation'])
    config['skip_first_n'] = int(config['skip_first_n'])
    config['modify_values'] = config['modify_values'] == 'True'
    config['replace_nan_values'] = config['replace_nan_values'] == 'True'
    config['interval_minutes'] = int(config['interval_minutes'])
    ident = config['nan_value_identifier']
    if ident == '-':
        config['nan_value_identifier'] = '-'
    else:
        ident_arr = ident.split(',')
        if '-' in ident_arr:
            ident_arr.remove('-')
            config['nan_value_identifier'] = [float(x) for x in ident_arr]
            config['nan_value_identifier'].append('-')
        else:
            config['nan_value_identifier'] = [float(x) for x in ident_arr]
    if config['nan_value_replacement'] != 'NaN':
        config['nan_value_replacement'] = int(config['nan_value_replacement'])
        return config
###################################################################################

## Now try to impelment threshold###:
# def parse_config(config):
#     config['elevation'] = int(config['elevation'])
#     config['skip_first_n'] = int(config['skip_first_n'])
#     config['modify_values'] = config['modify_values'] == 'True'
#     config['replace_nan_values'] = config['replace_nan_values'] == 'True'
#     config['interval_minutes'] = int(config['interval_minutes'])
#     ident = config['nan_value_identifier']
#     if ident == '-':
#         config['nan_value_identifier'] = '-'
#     else:
#         ident_arr = ident.split(',')
#         if '-' in ident_arr:
#             ident_arr.remove('-')
#             config['nan_value_identifier'] = [float(x) for x in ident_arr]
#             config['nan_value_identifier'].append('-')
#         else:
#             config['nan_value_identifier'] = [float(x) for x in ident_arr]
#     if config['nan_value_replacement'] != 'NaN':
#         config['nan_value_replacement'] = int(config['nan_value_replacement'])
#     config['nan_value_threshold'] = float(config.get('nan_value_threshold', "inf"))
#     return config

#####################################################

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
        "elevation": 0.0,
        "latitude": 0,
        "longitude": 0,
        "skip_first_n": 10,
        "modify_values": False,
        "interval_minutes": 1,
        "modifier": "sum",
        "replace_nan_values": False,
        "nan_value_identifier": "-",
        "nan_value_threshold": False,
        "nan_value_replacement": 0
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
    f.write(f"replace_nan_values={default['replace_nan_values']}\t; set this to True if you want to replace invalid "
            f"values.\n")
    f.write(f"nan_value_identifier={default['nan_value_identifier']}\t; set this to '-' to replace all negative "
            f"values or set this to a specific value or a comma seperated list of values, that you want to replace.\n")
    f.write(f"nan_value_threshold={default['nan_value_threshold']}\t; set this to a thresholdvalue to replace all values above or below.\n")
    f.write(f"nan_value_replacement={default['nan_value_replacement']}\t; set this to the integer value that you "
            f"want to replace invalid values with, or set it to 'NaN' to set the value to NaN.\n")
    f.close()
