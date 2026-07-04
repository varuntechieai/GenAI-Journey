from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ==================
# Step 1 - Load Document
# ==================
def load_document(file_path):
    loader = TextLoader(file_path)
    documents = loader.load()
    print(f"✅ Loaded document: {file_path}")
    print(f"📄 Total characters: {len(documents[0].page_content)}")
    return documents

# ==========================
# Step 2 - Split into Chunks
# ==========================
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks

# Test Steps 1 & 2
docs = load_document("company_policy.txt")
chunks = split_documents(docs)

# Print first 3 chunks to see what they look like
print("\n--- Sample Chunks ---")
for i, chunk in enumerate(chunks[:3]):
    print(f"\nChunk {i+1}:")
    print(chunk.page_content)
    print("-" * 30)

# =========================================
# Step 3 - Create Embeddings + Vector Store
# =========================================
def create_vector_store(chunks):
    print("\n Creating embeddings may take a minute")
    embeddings=HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-V2"
    )
    vector_store=FAISS.from_documents(chunks,embeddings)
    print("Vector Store created")
    return vector_store

#Test step 3
vector_store=create_vector_store(chunks)

# ===============================
# STep 4 - Search relevant chunks
# ===============================
def search_rlv_chunks(vector_store,question,k=3):
    rlv_chunks=vector_store.similarity_search(question,k=k)
    print(f"Found {len(rlv_chunks)} relevant chunks")
    return rlv_chunks

# ===============================
# STep 5 - Generate using Llama 3
# ===============================
def generate_answer(question,rlv_chunks):
    context="\n\n".join([chunk.page_content for chunk in rlv_chunks])
    prompt=f"""
You are a helpful HR assistant. Answer the question based ONLY on the context provided below.
If the answer is not in the context, say "I don't have that information in my documents."

Context:
{context}
Question: {question}

Answer="""
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {"role":"system","content":"You are a helpful HR assistant. Answer only from the provided context."},
            {"role":"user","content":prompt}
        ]
    )
    return response.choices[0].message.content.strip()

# ===============================
# STep 6 - Complete RAG Pipeline
# ===============================
def ask_document(question,vector_store):
    print(f"\nQuestion: {question}")

#Search relevant chunks
    rlv_chunks=search_rlv_chunks(vector_store,question)

#Generate answer
    answer=generate_answer(question,rlv_chunks)
    print(f"\n Answer: {answer}")
    return answer

#Test it
# ask_document("How many paid leaves do employee get",vector_store)
# ask_document("What is work from home policy",vector_store)
# ask_document("What is the salary of CEO",vector_store)

# ===============================
# STep 6 - Complete RAG Pipeline
# ===============================
def rag_chat(vector_store):
    print("=" * 50)
    print("🤖 HR Policy AI Assistant")
    print("Ask anything about company policies")
    print("Type 'exit' to quit")
    print("=" * 50)

    while True:
        question=input("\n You: ")
        if question.lower()=="exit":
            print("Goodbye Varun!")
            break
        ask_document(question,vector_store)

#Run interactive chat
rag_chat(vector_store)

