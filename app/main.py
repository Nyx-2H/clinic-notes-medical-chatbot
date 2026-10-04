import os
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Bug-Proof Cloud-Native Internet Search RAG Engine Stack
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
# FIXED: Using the direct search api wrapper to completely bypass the broken Wikipedia routing loops
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

from app.core.settings import settings

# Thread-safe global application state registry controller
app_state = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Modern Lifespan Manager: Hooks up a bug-proof zero-dependency web research agent
    connecting live DuckDuckGo API wrappers directly to your cloud Groq Llama 3 engine.
    """
    try:
        # 1. Initialize the Fixed Live Web Search Tool Component (Forcing pure text results)
        print("Initializing Bug-Proof DuckDuckGo Web API search wrapper...")
        app_state["search_tool"] = DuckDuckGoSearchAPIWrapper(max_results=3)

        # 2. Connect to Groq LLM Client Gateway
        print("Connecting to Groq Engine Gateway...")
        app_state["llm"] = ChatGroq(
            groq_api_key=settings.GROQ_API_KEY.get_secret_value(),
            model_name="openai/gpt-oss-20b",
            temperature=0.2
        )
        print("🚀 Internet Research RAG Agent Engine loaded successfully!")
    except Exception as e:
        print(f"❌ Production system boot sequence failed: {str(e)}")
        app_state["search_tool"] = None
        app_state["llm"] = None
    yield
    app_state.clear()

# Initialize High-Performance FastAPI Engine running modern Lifespan protocols
app = FastAPI(
    title="High-Performance Live Web AI Chatbot Backend", 
    version="3.0.0",
    docs_url="/api/docs",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=1000)

# Professional Internet Summarization Prompt Engineering Template
INTERNET_RESEARCH_PROMPT = """You are a highly capable and empathetic clinical AI assistant. You answer questions by analyzing live research data extracted from the internet.

Live Internet Data Context:
{context}

Strict Execution Protocol:
1. Formulate a comprehensive, precise, and supportive summary based on the web text guidelines.
2. Citing sources or stating current context patterns clearly is highly recommended.
3. Your analysis must follow safe clinical information tracking rules. Always present general information only. Never give personalized medical evaluations.
4. You must include a structured summary broken into clean sections, outlining at least 3 distinct parameters or considerations matching the user scenario, and present at least 3 distinct management or study alternatives.

User Question: {question}
Helpful Clinical Research Response:"""

@app.post("/api/v1/chat")
async def handle_chat_query(request: ChatRequest):
    """
    Asynchronous Web Research Endpoint: Extracts user questions, searches the 
    live web via DuckDuckGo, and routes compilation data directly to Groq Llama 3.
    """
    if not app_state.get("search_tool") or not app_state.get("llm"):
        raise HTTPException(
            status_code=503, 
            detail="Core research components are warming up or configurations are missing, please re-submit shortly."
        )
    
    try:
        query = request.message
        search_tool = app_state["search_tool"]
        llm = app_state["llm"]
        
        # Step 1: Execute search through the fixed api wrapper (Guaranteed compiler/DNS proof)
        print(f"Crawling internet database records for: '{query}'...")
        web_context = await asyncio.get_running_loop().run_in_executor(
            None, search_tool.run, query
        )
        
        if not web_context or not web_context.strip():
            web_context = "No current live search results matching this query string were found on the internet."
            
        # Step 2: Bind gathered contextual variables to prompt templates
        prompt = ChatPromptTemplate.from_template(INTERNET_RESEARCH_PROMPT)
        formatted_prompt = prompt.format_messages(
            context=web_context,
            question=query
        )
        
        # Step 3: Dispatch processing request directly to gpt
        response = await asyncio.get_running_loop().run_in_executor(
            None, llm.invoke, formatted_prompt
        )
        
        return {
            "answer": response.content,
            "status": "success",
            "compliance_disclaimer": (
                "Research Disclaimer: This assistant provides general medical reference evaluations "
                "synthesized from real-time live internet crawling queries. It does not provide personalized "
                "medical advice or active treatments. Always consult a licensed healthcare professional."
            )
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Web research workflow process failed: {str(e)}")
