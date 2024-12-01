import os

import yaml


def load_plugins(plugins_directory):
    plugins = {}
    for filename in os.listdir(plugins_directory):
        if filename.endswith(".yaml"):
            with open(os.path.join(plugins_directory, filename), 'r') as file:
                plugin_name = os.path.splitext(filename)[0]
                plugins[plugin_name] = yaml.safe_load(file)
    return plugins

data = load_plugins("data/plugins_files")

def list_node_types(plugin_name):
    node_types_list = []
    node_types = data[plugin_name + "_plugin"]["node_types"]
    node_types_list.extend(node_types.keys())
    return node_types_list


def list_node_type_properties(plugin_name, node_type):
    properties_list = []
    if "node_types" in data[plugin_name + "_plugin"] and node_type in data[plugin_name + "_plugin"]["node_types"]:
        properties = data[plugin_name + "_plugin"]["node_types"][node_type]["properties"]
        properties_list.extend(properties.keys())
        return properties_list
    else:
        return None


def get_node_type_property_data(plugin_name, node_type, property_name):
    if "node_types" in data[plugin_name + "_plugin"] and node_type in data[plugin_name + "_plugin"]["node_types"]:
        return data[plugin_name + "_plugin"]["node_types"][node_type]["properties"][property_name]
    else:
        return None
