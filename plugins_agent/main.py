# import plugins_agent.db.plugins_data as plugins_data
from plugins_agent.agent import PluginsAgent

# data = plugins_data.load_plugins("data/plugins_files")
if __name__ == '__main__':
    # print(plugins_data.list_node_types(data["aws_plugin"]));
    # print(plugins_data.list_node_type_properties(data["aws_plugin"], "nativeedge.nodes.aws.dynamodb.Table"))
    # print(plugins_data.get_node_type_property_data(data["aws_plugin"], "nativeedge.nodes.aws.dynamodb.Table",
    #                                                "resource_config"));

    agent = PluginsAgent(model_name="mistral-small")

    question = "what node types I need for awss?"
    expectedAnswer = "list_node_types for aws"
    answer = agent.ask(question + '\n')
    print("Question:" + question)
    print(f"Answer: {answer}")
    print("Expected Answer:" + expectedAnswer + '\n')

    question = "What types of nodes do I need for azure??"
    expectedAnswer = "list_node_types for azure"
    answer = agent.ask(question + '\n')
    print("Question:" + question)
    print(f"Answer: {answer}")
    print("Expected Answer:" + expectedAnswer + '\n')

    question = "what properties exist for nativeedge.nodes.aws.dynamodb.Table? "
    answer = agent.ask(question)
    expectedAnswer = "TableName"
    print("Question:" + question)
    print(f"Answer: {answer}")
    print("Expected Answer:" + expectedAnswer + '\n')

    question = "what node types I need for helm?"
    expectedAnswer = "unknown"
    answer = agent.ask(question + '\n')
    print("Question:" + question)
    print(f"Answer: {answer}")
    print("Expected Answer:" + expectedAnswer + '\n')

    #
    # question = "is table name mandatory?"
    # expectedAnswer = "yes"
    # answer = agent.ask(question)
    # print("Question:" + question)
    # print("Answer:" + answer)
    # print("Expected Answer:" + expectedAnswer + '\n')
    #
    # question = "what type is it?"
    # expectedAnswer = "string"
    # answer = agent.ask(question + '\n')
    # print("Question:" + question)
    # print("Answer:" + answer)
    # print("Expected Answer:" + expectedAnswer + '\n')
    #
    # question = "is table name required?"
    # expectedAnswer = "yes"
    # answer = agent.ask(question + '\n')
    # print("Question:" + question)
    # print("Answer:" + answer)
    # print("Expected Answer:" + expectedAnswer + '\n')
    #
    # question = "what is table name?"
    # expectedAnswer = "The name of the table to create"
    # answer = agent.ask(question + '\n')
    # print("Question:" + question)
    # print("Answer:" + answer)
    # print("Expected Answer:" + expectedAnswer + '\n')
    #
    # question = "what node type I need for dynamodb table?"
    # expectedAnswer = "nativeedge.datatypes.aws.dynamodb.Table.config"
    # answer = agent.ask(question + '\n')
    # print("Question:" + question)
    # print("Answer:" + answer)
    # print("Expected Answer:" + expectedAnswer + '\n')
