import json
import os
import toml
from typing import Optional, Any, Dict, Type
from pydantic import Field
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import JSONLoader
from crewai.tools.base_tool import BaseTool
from langchain_core.documents import Document

class MyJSONSearchTool(BaseTool):
    name: str = "JSON Search"
    description: str = "Busca por informações em um arquivo JSON indexado com embeddings"
    
    # Private attributes that won't be validated by Pydantic
    _json_path: str = ""
    _config: Dict = {}
    _vectorstore: Optional[Any] = None
    _json_data: Optional[dict] = None
    
    def __init__(
        self,
        json_path: str,
        config: Dict,
        **kwargs
    ):
        super().__init__(**kwargs)
        self._json_path = json_path
        self._config = config
        self._load_vectorstore()

    def _load_documents(self) -> list[Document]:
        # Carrega e transforma o JSON em documentos para embedding
        loader = JSONLoader(file_path=self._json_path, jq_schema='.', text_content=False)
        return loader.load()

    def _load_vectorstore(self):
        # Load OpenAI API key from secrets.toml if not in environment
        if not os.getenv("OPENAI_API_KEY"):
            try:
                secrets_path = os.path.join(os.path.dirname(__file__), "../../../secrets.toml")
                if os.path.exists(secrets_path):
                    with open(secrets_path, 'r') as f:
                        secrets = toml.load(f)
                        api_key = secrets.get("OPENAI_API_KEY")
                        if api_key and api_key != "your-openai-api-key-here":
                            os.environ["OPENAI_API_KEY"] = api_key
            except Exception as e:
                print(f"Warning: Could not load secrets.toml: {e}")
        
        # Check if we have a valid OpenAI API key
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your-openai-api-key-here":
            print("Warning: No valid OpenAI API key found. The tool will work with limited functionality.")
            # Load JSON data for simple text matching as fallback
            with open(self._json_path, 'r', encoding='utf-8') as f:
                self._json_data = json.load(f)
            self._vectorstore = None
            return
        
        documents = self._load_documents()

        model_name = self._config["embedding_model"]["config"]["model"]
        embeddings = OpenAIEmbeddings(model=model_name)

        # Create vectorstore without client_settings to avoid compatibility issues
        self._vectorstore = Chroma.from_documents(
            documents,
            embedding=embeddings,
            persist_directory=self._config.get("persist_directory", "/tmp/chroma"),
            collection_name="json_qa"
        )

    def _run(self, query: str) -> str:
        # If vectorstore is available, use semantic search
        if self._vectorstore:
            results = self._vectorstore.similarity_search(query, k=3)
            if not results:
                return "Nenhuma informação encontrada."
            return "\n\n".join([doc.page_content for doc in results])
        
        # Fallback: simple text matching in JSON data
        if self._json_data:
            matches = []
            query_lower = query.lower()
            
            # Search through all FAQ categories
            for category, items in self._json_data.items():
                for item in items:
                    question = item.get('question', '').lower()
                    answer = item.get('answer', '').lower()
                    
                    # Simple keyword matching
                    if any(word in question or word in answer for word in query_lower.split()):
                        matches.append(f"Pergunta: {item.get('question', '')}\nResposta: {item.get('answer', '')}")
            
            if matches:
                return "\n\n".join(matches[:3])  # Return top 3 matches
            
        return "Nenhuma informação encontrada."

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Uso assíncrono não implementado.")
