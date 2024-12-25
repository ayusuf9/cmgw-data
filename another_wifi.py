import os
from typing import Dict, List, Optional, Any
from langchain_core.pydantic_v1 import BaseModel, Field
from langgraph.graph import Graph, StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Milvus
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# State Management
class AgentState(BaseModel):
    """State management for the financial Q&A agent."""
    messages: List[Any] = Field(default_factory=list)
    context: Optional[str] = None
    current_pdf: Optional[str] = None
    extracted_data: Dict = Field(default_factory=dict)
    error: Optional[str] = None

# PDF Processing
class PDFProcessor:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def process_pdf(self, pdf_path: str) -> List[str]:
        """Process PDF and split into chunks."""
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        texts = self.text_splitter.split_documents(pages)
        return texts

# Vector Store Management
class VectorStoreManager:
    def __init__(self, collection_name: str = "financial_docs"):
        self.embeddings = OpenAIEmbeddings()
        self.collection_name = collection_name
        
        # Milvus connection settings
        self.milvus_host = os.getenv("MILVUS_HOST", "localhost")
        self.milvus_port = int(os.getenv("MILVUS_PORT", "19530"))
        
    def initialize_vectorstore(self, texts: List[str]) -> Milvus:
        """Initialize Milvus vector store with document chunks."""
        return Milvus.from_documents(
            texts,
            self.embeddings,
            connection_args={
                "host": self.milvus_host,
                "port": self.milvus_port
            },
            collection_name=self.collection_name
        )

# Financial Context Enhancement
class FinancialContextEnhancer:
    def __init__(self):
        self.financial_terms_prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a financial domain expert. Enhance the following context with relevant financial insights.
            Focus on:
            1. Key financial metrics mentioned
            2. Industry-standard interpretations
            3. Related financial concepts
            Be concise and specific."""),
            ("human", "{context}")
        ])
        
        self.llm = ChatOpenAI(temperature=0)
        
    def enhance_context(self, context: str) -> str:
        """Enhance retrieved context with financial domain knowledge."""
        chain = self.financial_terms_prompt | self.llm
        enhanced_context = chain.invoke({"context": context})
        return enhanced_context

# Q&A Processing
class QAProcessor:
    def __init__(self, vectorstore: Milvus):
        self.llm = ChatOpenAI(temperature=0)
        self.retriever = vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 3}
        )
        
        # Contextualize questions with chat history
        contextualize_q_system_prompt = """
        Given a chat history and the latest user question which might reference context in the chat history,
        formulate a standalone question that can be understood without the chat history.
        Focus on financial terms and metrics mentioned in the conversation.
        Do NOT answer the question, just reformulate it if needed or return it as is.
        """
        
        self.contextualize_q_prompt = ChatPromptTemplate.from_messages([
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}")
        ])
        
        # Create history-aware retriever
        self.history_aware_retriever = create_history_aware_retriever(
            self.llm,
            self.retriever,
            self.contextualize_q_prompt
        )
        
        # Create document processing chain
        qa_system_prompt = """
        You are a financial analysis expert. Use the following retrieved context to answer the question.
        If you don't know the answer, just say that you don't know.
        
        Guidelines:
        - Cite specific financial metrics and figures when available
        - Explain the significance of financial terms
        - Provide industry context when relevant
        - Keep the answer focused and precise
        """
        
        qa_prompt = ChatPromptTemplate.from_messages([
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            ("human", "Context: {context}"),
        ])
        
        document_chain = create_stuff_documents_chain(
            self.llm,
            qa_prompt
        )
        
        # Create retrieval chain
        self.retrieval_chain = create_retrieval_chain(
            self.history_aware_retriever,
            document_chain
        )
        
    def process_query(self, query: str, chat_history: List) -> Dict:
        """Process user query and generate response."""
        response = self.retrieval_chain.invoke({
            "input": query,
            "chat_history": chat_history
        })
        return response

# Main Agent Class
class FinancialQAAgent:
    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.vector_store_manager = VectorStoreManager()
        self.context_enhancer = FinancialContextEnhancer()
        self.qa_processor = None
        
    def initialize_from_pdf(self, pdf_path: str):
        """Initialize the agent with a PDF document."""
        # Process PDF
        texts = self.pdf_processor.process_pdf(pdf_path)
        
        # Initialize vector store
        vectorstore = self.vector_store_manager.initialize_vectorstore(texts)
        
        # Initialize QA processor
        self.qa_processor = QAProcessor(vectorstore)
        
    def process_message(self, state: AgentState) -> AgentState:
        """Process incoming message and update state."""
        try:
            last_message = state.messages[-1]
            if not isinstance(last_message, HumanMessage):
                return state
                
            query = last_message.content
            chat_history = [(m.content, r.content) for m, r in zip(state.messages[:-1:2], state.messages[1::2])]
            
            # Get response from QA processor
            response = self.qa_processor.process_query(query, chat_history)
            
            # Update state
            state.messages.append(AIMessage(content=response["answer"]))
            state.context = str(response.get("context", ""))
            
            return state
            
        except Exception as e:
            state.error = str(e)
            return state

# Graph Construction
def should_continue(state: AgentState) -> bool:
    """Determine if the conversation should continue."""
    # Stop if there's an error or if we've processed the last message
    return not state.error and len(state.messages) > 0

def build_graph() -> Graph:
    """Construct the LangGraph processing graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("process_message", FinancialQAAgent().process_message)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "process_message",
        should_continue,
        {
            True: "process_message",  # Continue processing if condition is met
            False: END,  # Stop if condition is not met
        }
    )
    
    # Set entry point
    workflow.set_entry_point("process_message")
    
    # Compile graph
    return workflow.compile()

# Usage Example
def main():
    # Initialize agent
    agent = FinancialQAAgent()
    agent.initialize_from_pdf("financial_report.pdf")
    
    # Build graph
    graph = build_graph()
    
    # Initialize state
    initial_state = AgentState(
        messages=[HumanMessage(content="What were the key financial metrics for Q4?")]
    )
    
    # Run graph and get config
    config = {"recursion_limit": 10}
    
    # Convert state to dict for graph input
    state_dict = initial_state.dict()
    
    # Run graph
    final_state_dict = graph.invoke(state_dict, config)
    
    # Convert back to AgentState
    final_state = AgentState(**final_state_dict)
    
    # Print response
    if final_state.error:
        print(f"Error: {final_state.error}")
    elif final_state.messages:
        last_message = final_state.messages[-1]
        if isinstance(last_message, AIMessage):
            print(f"Response: {last_message.content}")
        else:
            print("No AI response in the final state")
    else:
        print("No messages in the final state")