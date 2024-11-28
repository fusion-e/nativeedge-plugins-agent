import yaml
import os

plugin_directory = 'plugins_files'


def load_plugins(plugin_directory):
    plugins = {}
    for filename in os.listdir(plugin_directory):
        if filename.endswith(".yaml"):  # Assume files are in YAML format
            with open(os.path.join(plugin_directory, filename), 'r') as file:
                plugin_name = filename[:-5]  # Remove .yaml extension for plugin name
                plugins[plugin_name] = yaml.safe_load(file)
    return plugins


def list_node_types(plugin_data):
    node_types_list = []
    node_types = plugin_data["node_types"]
    node_types_list.extend(node_types.keys())
    return node_types_list


def list_node_type_properties(plugin_data, node_type):
    properties_list = []
    if "node_types" in plugin_data and node_type in plugin_data["node_types"]:
        properties = plugin_data["node_types"][node_type]["properties"]
        properties_list.extend(properties.keys())
        return properties_list
    else:
        return None


def get_node_type_property_data(plugin_data, node_type, property_name):
    if "node_types" in plugin_data and node_type in plugin_data["node_types"]:
        return plugin_data["node_types"][node_type]["properties"][property_name]
    else:
        return None
