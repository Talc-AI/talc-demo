from PyPDF2 import PdfReader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_openai import OpenAI
import os
import csv

reader = PdfReader("./knowledge_base/10050-Medicare-and-You.pdf")

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


# Load test set from csv
test_set = []
with open("./artifacts/test_set.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        test_set.append(row)

output = []
# Run the test set
for row in test_set:
    query = row["question"]
    docs = docsearch.similarity_search(query)
    response = chain.invoke({"input_documents": docs, "question": query})
    print(response["output_text"])
    row["user_answer"] = response["output_text"]

# write the output to a csv
with open("./artifacts/output.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=test_set[0].keys())
    writer.writeheader()
    writer.writerows(test_set)
