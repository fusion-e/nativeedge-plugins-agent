import yaml
import os

from plugins_agent.actions import list_node_types, list_node_type_properties, get_node_type_property_data





available_actions = {
    "list_node_types": list_node_types,
    "list_node_type_properties": list_node_type_properties,
    "get_node_type_property_data": get_node_type_property_data
}
