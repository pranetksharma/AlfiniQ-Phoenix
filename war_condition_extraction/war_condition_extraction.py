from openai import OpenAI
import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import HumanMessage, SystemMessage
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import joblib

os.environ["OPENAI_API_KEY"] = "sk-proj-7HJXBEATqkumYhMifJ5eT3BlbkFJYH0O07E58bjoLdWF85MG"

def initialize_chat_model(model_name, temperature):
    """
    Initialize the ChatOpenAI model from langchain.

    Args:
        model_name (str): The name of the ChatOpenAI model to use.
        temperature (float): The temperature value for the model, controlling the randomness of the output.

    Returns:
        ChatOpenAI: An instance of the ChatOpenAI model.
    """
    return ChatOpenAI(model_name=model_name, temperature=temperature)

# Initialize the ChatOpenAI model
chat = initialize_chat_model("gpt-3.5-turbo", 0.9)

# Define the prompt template
template = """Task Description:
Analyze the user input provided and identify which war-related crises the individual has likely experienced. Output your findings as a binary string where each digit represents a specific crisis from the provided list. Each position in the string corresponds to a crisis in the order listed below, with '1' indicating the presence of the crisis and '0' indicating its absence. Return the string as well as the associated crisis.

List of War Crises:
1. displacement 
2. separate own house
3. safe drinking water source
4. nutrition available
5. safe and healthy nutrition
6. vaccines available
7. no education
8. shortage of clean water
9. Destruction of healthcare infrastructure
10. Bombings
11. Chemical weapon exposure
12. Continuous stress exposure
13. Reduced access to diagnostic services
14. Radiation exposure from conflict
15. Increased rainfall leading to water contamination
16. Overcrowding in shelters
17. Exposure to toxic substances from bombings
18. Inadequate cancer treatment facilities
19. Trauma from bombings
20. Distrust in response efforts

User Input: "{user_input}"
Model Output Format: String of 20 binary digits (e.g., '0100110...') representing the identified crises and associated crisis. give me only the vector. the vector can have more than one '1'
"""

def format_prompt(template, user_input):
    """
    Format the prompt template with the given user input.

    Args:
        template (str): The prompt template string.
        user_input (str): The user input to be included in the prompt.

    Returns:
        str: The formatted prompt string with the user input.
    """
    prompt = ChatPromptTemplate.from_template(template)
    return prompt.format(user_input=user_input)

# Get user input
user_input = input("")

# Format the prompt with the user input
formatted_prompt = format_prompt(template, user_input)

# Generate a response using the formatted prompt
response = chat([HumanMessage(content=formatted_prompt)])

def get_binary_array(response):
    """
    Convert the model response into a binary NumPy array.

    Args:
        response (str): The response string from the ChatOpenAI model.

    Returns:
        numpy.ndarray: A NumPy array containing binary values (0 or 1) corresponding to the response.
    """
    return np.array([int(char) for char in response.content])

binary_array = get_binary_array(response)

diseases = ["breast cancer", "leukemia", "cholera", "diabetes", "hepatitis"]

def load_model(model_path):
    """
    Load a pre-trained model from a specified path.

    Args:
        model_path (str): The file path to the pre-trained model.

    Returns:
        Any: The loaded model object.
    """
    return joblib.load(model_path)

# Load the saved model
clf = load_model('../synthetic-data-analysis/random_forest_model.joblib')

def make_prediction(model, input_data):
    """
    Make a prediction using the loaded model and the input data.

    Args:
        model (Any): The loaded model object.
        input_data (list): The input data for making predictions.

    Returns:
        numpy.ndarray: An array containing the predicted values.
    """
    return model.predict(input_data)

# Make predictions
X_test = [binary_array]
predictions = make_prediction(clf, X_test)
print(diseases[predictions[0]])
