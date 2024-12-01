from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import time
import yaml

from plugins_agent.db.plugins_data import available_actions
from plugins_agent.json_utils import extract_json
from plugins_agent.prompts import system_prompt


def read_yaml(file_path: str) -> dict:
    """Reads a YAML file and returns its contents as a dictionary."""
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
        print("File is ok")
        return data
    except Exception as e:
        print(f"Error reading YAML file: {e}")
        return {}


def get_context_from_yaml(yaml_data: dict) -> str:
    """Converts YAML data to a string context for the LLM."""
    return yaml.dump(yaml_data, default_flow_style=False)


class AWSAgent:
    def __init__(self, model_name: str):
        base_url = "http://10.227.242.120:11434"
        self.model = OllamaLLM(model=model_name, base_url=base_url)

        # Store the context as an attribute
        # self.context = "a"

        self.system_prompt = system_prompt
        # self.system_prompt = (
        #         "based only on yaml configuration: " + self.context +
        #         "write answer to user question " +
        #         "make it short and to the point"
        # )

        # self.system_prompt = (
        #     "[INST] Using the following information, answer user questions accurately and comprehensively. "
        #     "Ensure all responses are based solely on the content provided below, without including any external data or references. " +
        #     "Start each response directly with the answer. " +
        #     "Do not mention or expose the source of the information. "+
        #     "Maintain a professional and clear tone throughout the answers. [/INST]" +
        #     "[TOOL_RESULTS]"+
        #         self.context +
        #     "[/TOOL_RESULTS]"
        # )

        # self.template = """System: {system_prompt}
        #                    User: {question}
        #                    """
        # self.prompt = ChatPromptTemplate.from_template(self.template)

    def ask(self, user_query: str) -> str:
        # Start timing
        start_time = time.time()

        turn_count = 1
        max_turns = 3
        while turn_count < max_turns:
            print(f"Loop: {turn_count}")
            print("----------------------")
            turn_count += 1

            template = """System: {system_prompt}
                          User: {question}
                          Assistant: {assistant}
                                   """
            agent_response = ""
            prompt = ChatPromptTemplate.from_template(template)
            formatted_prompt = prompt.format(system_prompt=self.system_prompt,
                                             question=user_query,
                                             assistant=agent_response)
            agent_response = self.model.invoke(formatted_prompt)

            print("agent_response: " + agent_response)

            # extract action JSON From Text Response.
            action_json = extract_json(agent_response)

            if action_json:
                function_name = action_json[0]['function_name']
                function_params = action_json[0]['function_params']
                if function_name not in available_actions:
                    raise Exception(f"Unknown action: {function_name}: {function_params}")
                print(f" -- running {function_name} {function_params}")
                action_function = available_actions[function_name]
                action_function(**function_params)
                # call the function
                result = action_function(**function_params)
                print("Action_Response:", result)
                function_result_message = f"Action_Response: {result}"
                user_query = function_result_message
                print("----------------------")
            else:
                break

        # End timing
        end_time = time.time()

        # Calculate latency
        latency = end_time - start_time
        print(f"{latency:.2f} seconds")
        return agent_response
