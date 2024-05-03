import os
from dotenv import load_dotenv
from openai import AzureOpenAI

#Load variables from .env file
load_dotenv()

#Initialize Azure OpenAI Service details
AZURE_OPEN_AI_KEY = os.getenv('AZURE_OPEN_AI_KEY')
AZURE_OPEN_AI_ENDPOINT = os.getenv('AZURE_OPEN_AI_ENDPOINT')

API_VERSION = "2024-02-01"
MODEL_NAME = "gpt-35-turbo"

client = AzureOpenAI(
    azure_endpoint=AZURE_OPEN_AI_ENDPOINT,
    api_key=AZURE_OPEN_AI_KEY,
    api_version=API_VERSION,
)
