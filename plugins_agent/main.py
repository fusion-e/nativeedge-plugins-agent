import plugins_agent.db.plugins_data as plugins_data

if __name__ == '__main__':
    data = plugins_data.load_plugins("data/plugins_files")
    print(plugins_data.list_node_types(data["aws_plugin"]));
    print(plugins_data.list_node_type_properties(data["aws_plugin"], "nativeedge.nodes.aws.dynamodb.Table"))
    print(plugins_data.get_node_type_property_data(data["aws_plugin"], "nativeedge.nodes.aws.dynamodb.Table",
                                      "resource_config"))