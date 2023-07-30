from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

def initialize_langchain(api_key, data_path):
    llm = OpenAI(openai_api_key="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")
    loader = TextLoader(data_path)
    index = VectorstoreIndexCreator().from_loaders([loader])
    # Add any other initialization steps or return necessary objects
    return llm, loader, index