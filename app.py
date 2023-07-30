#app.py

from flask import Flask, render_template_string, request, jsonify
import os

from src.data_prep import load_pdf_data_from_disk, clean_and_format_text
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

# Initialize Flask app
app = Flask(__name__)

# Load data and prepare env
os.environ["OPENAI_API_KEY"] = "sk-HIDDEN"

loader = TextLoader("data/clean_pdf_text.txt")
index = VectorstoreIndexCreator().from_loaders([loader])
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=10)
all_splits = text_splitter.split_documents(data)
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

# Flask routes
@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    question = ""
    if request.method == 'POST':
        question = request.form.get('question')
        print(question)
        response = qa_chain({"query": question})
        print(response)
        answer = response.get('result', 'I am sorry. No answer found.')

    return render_template_string(open("template.html", "r").read(), answer=answer, question=question)

if __name__ == "__main__":
    app.run(debug=True)
