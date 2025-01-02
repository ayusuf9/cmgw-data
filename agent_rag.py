import os
from typing import Sequence, List, Dict, Any
from typing_extensions import Annotated, TypedDict
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.document_loaders.parsers.pdf import PDFPlumberParser
from langchain.document_loaders import Blob
from langchain_milvus import Milvus
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

class RAGState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], "messages"]
    context: str
    retrieved_docs: List[Dict[str, Any]]

class EnhancedRAGChatbot:
    def __init__(
        self,
        pdf_path: str,
        azure_endpoint: str,
        api_key: str,
        chunk_size: int = 3000,
        chunk_overlap: int = 200,
        max_tokens: int = 4000
    ):
        self.azure_endpoint = azure_endpoint
        self.api_key = api_key
        self.max_tokens = max_tokens
        
        # Initialize embedding model
        self.embeddings = AzureOpenAIEmbeddings(
            model='text-embedding-3-large',
            azure_endpoint=azure_endpoint,
            openai_api_version="2024-02-01",
            api_key=api_key,
            chunk_size=100
        )
        
        # Initialize LLM
        self.llm = AzureChatOpenAI(
            azure_deployment="o1-mini",
            api_version="2024-09-01-preview",
            temperature=1,
            max_tokens=max_tokens,
            api_key=api_key,
            timeout=None,
            max_retries=2,
            azure_endpoint=azure_endpoint
        )
        
        # Load and process documents
        self._initialize_documents(pdf_path, chunk_size, chunk_overlap)
        
        # Initialize conversation graph
        self._initialize_graph()

    def _initialize_documents(self, pdf_path: str, chunk_size: int, chunk_overlap: int):
        # Load PDF
        parser = PDFPlumberParser()
        blob = Blob.from_path(pdf_path)
        documents = parser.parse(blob)
        
        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.docs = text_splitter.split_documents(documents)
        
        # Initialize vector store
        self.vectorstore = Milvus.from_documents(
            documents=self.docs,
            embedding=self.embeddings,
            connection_args={"uri": "./vtl_milvus.db"},
            drop_old=True,
        )
        self.retriever = self.vectorstore.as_retriever()

    def _initialize_graph(self):
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a helpful Financial AI assistant. Answer the question using only the 
            information provided in the context. Do not invent information or deviate from the provided context.
            Always leverage your natural language understanding to interpret tables, identifying headers, 
            relationships, and key insights based on the provided relevant context."""),
            MessagesPlaceholder(variable_name="messages"),
            ("human", "Context: {context}\n\nQuestion: {question}")
        ])

        # Initialize state graph
        workflow = StateGraph(state_schema=RAGState)
        
        def retrieve_context(state: RAGState):
            """Retrieve relevant documents for the latest question"""
            latest_message = state["messages"][-1]
            if isinstance(latest_message, HumanMessage):
                retrieved_docs = self.vectorstore.similarity_search(
                    latest_message.content, k=5
                )
                context = "\n\n".join(doc.page_content for doc in retrieved_docs)
                return {"context": context, "retrieved_docs": retrieved_docs}
            return {"context": state["context"], "retrieved_docs": state["retrieved_docs"]}

        def generate_response(state: RAGState):
            """Generate response using the LLM"""
            latest_message = state["messages"][-1]
            if isinstance(latest_message, HumanMessage):
                prompt_args = {
                    "messages": state["messages"][:-1],  # Previous conversation
                    "context": state["context"],
                    "question": latest_message.content
                }
                prompt = self.prompt.invoke(prompt_args)
                response = self.llm.invoke(prompt)
                return {"messages": [response]}
            return {"messages": []}

        # Add nodes and edges
        workflow.add_node("retrieve", retrieve_context)
        workflow.add_node("generate", generate_response)
        workflow.add_edge(START, "retrieve")
        workflow.add_edge("retrieve", "generate")
        
        # Compile graph with memory
        memory = MemorySaver()
        self.app = workflow.compile(checkpointer=memory)

    def chat(self, query: str, thread_id: str) -> str:
        """
        Send a message to the chatbot and get a response
        
        Args:
            query: User's question
            thread_id: Unique identifier for the conversation
            
        Returns:
            The chatbot's response
        """
        config = {"configurable": {"thread_id": thread_id}}
        input_messages = [HumanMessage(content=query)]
        
        # Initialize state if this is a new conversation
        state = {
            "messages": input_messages,
            "context": "",
            "retrieved_docs": []
        }
        
        output = self.app.invoke(state, config)
        return output["messages"][-1].content

    def stream_chat(self, query: str, thread_id: str):
        """
        Stream the chatbot's response token by token
        
        Args:
            query: User's question
            thread_id: Unique identifier for the conversation
            
        Yields:
            Tokens of the chatbot's response as they're generated
        """
        config = {"configurable": {"thread_id": thread_id}}
        input_messages = [HumanMessage(content=query)]
        
        # Initialize state if this is a new conversation
        state = {
            "messages": input_messages,
            "context": "",
            "retrieved_docs": []
        }
        
        for chunk, metadata in self.app.stream(
            state,
            config,
            stream_mode="messages"
        ):
            if isinstance(chunk, AIMessage):
                yield chunk.content

# Usage example:
if __name__ == "__main__":
    # Initialize the chatbot
    chatbot = EnhancedRAGChatbot(
        pdf_path="/users/CFII_DataScience/USERs/SPTADM/emma_agent/files/vlt-2015.pdf",
        azure_endpoint="https://apim-prd-quanthub-wus-3.azure-api.net",
        api_key=os.environ['TOKEN']
    )
    
    # Regular chat
    response = chatbot.chat(
        "What is the value to lien ratio?",
        thread_id="user123"
    )
    print("Regular response:", response)
    
    # Streaming chat
    print("\nStreaming response:")
    for token in chatbot.stream_chat(
        "What is the value to lien ratio?",
        thread_id="user123"
    ):
        print(token, end="", flush=True)