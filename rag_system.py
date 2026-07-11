from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================================
# Step 1 - Load Multiple Documents
# ================================
def load_documents(file_paths):
    all_documents=[]
    for file_path in file_paths:
        loader = TextLoader(file_path)
        docs=loader.load()
        documents = loader.load()
        # Add source metadata to each document
        for doc in docs:
            doc.metadata["source"]=file_path
        all_documents.extend(docs)
        print(f"✅ Loaded document: {file_path}")
    print(f"📄 Total documents loaded: {len(all_documents)}")
    return all_documents

# ==========================
# Step 2 - Split Documents into Chunks
# ==========================
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50,
        separators=["\n\n","\n","-","."," ",""]
    )
    chunks = splitter.split_documents(documents)
    print(f"✅ Split into {len(chunks)} chunks")
    return chunks

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

#Load all documents
documents=load_documents([
    "company_policy.txt",
    "finance_policy.txt",
    "tech_policy.txt"
])
chunks=split_documents(documents)
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
def generate_answer(question,rlv_chunks,conversation_history=[]):
    context="\n\n".join([chunk.page_content for chunk in rlv_chunks])

    #Build messages with History
    messages=[
        {
            "role":"system",
            "content":"""You are a helpful HR assistant.
        Answer questions based only on the context provided.
        If answer is not in context say I don't have that information."""
        }
    ]
    #Add conversation history
    for msg in conversation_history:
        messages.append(msg)
    #Add current question with context
    messages.append({
        "role":"user",
        "content":f"""Context:
{context}
Question: {question}"""
    })
    response=client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=messages
    )
       
    return response.choices[0].message.content.strip()

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

    #Memory - stores conversation history
    conversation_history=[]

    while True:
        question=input("\n You: ")
        if question.lower()=="exit":
            print("Goodbye Varun!")
            break
        #Search relevant chunks
        rlv_chunks=search_rlv_chunks(vector_store,question)
        sources=list(set([chunk.metadata["source"] for chunk in rlv_chunks]))

        #Generate answer with memory
        answer = generate_answer(question, rlv_chunks, conversation_history)
        
        print(f"\n🤖 Answer: {answer}")
        print(f"📌 Source: {', '.join(sources)}")

         # Update conversation history
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": answer})

#Run interactive chat
documents=load_documents([
    "company_policy.txt",
    "tech_policy.txt",
    "finance_policy.txt"
])
chunks = split_documents(documents)
vector_store = create_vector_store(chunks)
rag_chat(vector_store)


