from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
import os

reader = PdfReader("../knowledge_base/combustion.pdf")

raw_text = ""
for i, page in enumerate(reader.pages):
    text = page.extract_text()
    if text:
        raw_text += text

text_splitter = CharacterTextSplitter(
    separator="\n", chunk_size=1000, chunk_overlap=200, length_function=len
)

texts = text_splitter.split_text(raw_text)

embeddings = OpenAIEmbeddings()

docsearch = FAISS.from_texts(texts, embeddings)

chain = load_qa_chain(OpenAI(), chain_type="stuff")


def prompt_user():
    prompt = input("Enter your prompt: ")
    return prompt


while True:
    query = prompt_user()
    if query.lower() == "exit":
        break

    docs = docsearch.similarity_search(query)
    response = chain.invoke({"input_documents": docs, "question": query})
    print(response["output_text"])
