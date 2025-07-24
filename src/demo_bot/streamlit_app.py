#!/usr/bin/env python
import streamlit as st
import warnings
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from demo_bot.crew import DemoBot

# Load environment variables from .env file
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Configuração da página
st.set_page_config(
    page_title="VMB Invest DemoBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado - Design moderno e limpo
st.markdown("""
<style>
    /* Reset e configurações gerais */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        color: #ffffff;
    }
    
    .main .block-container {
        max-width: 900px;
        padding: 2rem 1rem;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(37, 197, 243, 0.3);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .vmb-logo {
        max-width: 150px;
        height: auto;
        margin-bottom: 1rem;
        filter: brightness(1.1);
    }
    
    .header-title {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(45deg, #25c5f3, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .header-subtitle {
        color: #b0b0b0;
        font-size: 1rem;
        margin: 0;
    }
    
    /* Mensagens do chat - garantir texto branco */
    .stChatMessage {
        color: #ffffff !important;
    }
    
    .stChatMessage p {
        color: #ffffff !important;
    }
    
    .stChatMessage div {
        color: #ffffff !important;
    }
    
    /* Ocultar elementos desnecessários */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    
    /* Botões modernos */
    .stButton > button {
        background: linear-gradient(135deg, #25c5f3, #1a9bc7);
        color: #000000;
        border: none;
        border-radius: 12px;
        padding: 0.7rem 1.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 197, 243, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 197, 243, 0.4);
        background: linear-gradient(135deg, #1a9bc7, #25c5f3);
    }
</style>
""", unsafe_allow_html=True)

def initialize_session_state():
    """Inicializa o estado da sessão do Streamlit"""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'crew_instance' not in st.session_state:
        st.session_state.crew_instance = None
    if 'conversation_started' not in st.session_state:
        st.session_state.conversation_started = False

def create_crew_instance():
    """Cria uma instância da crew se ainda não existir"""
    if st.session_state.crew_instance is None:
        with st.spinner("Inicializando assistentes..."):
            try:
                st.session_state.crew_instance = DemoBot()
                st.success("Assistentes prontos!")
            except Exception as e:
                st.error(f"Erro ao inicializar assistentes: {str(e)}")
                return False
    return True

def add_message(role, content, timestamp=None):
    """Adiciona uma mensagem ao histórico"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%H:%M")
    
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": timestamp
    })

def display_chat_history():
    """Exibe o histórico de mensagens usando st.chat_message"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])

def process_user_input(user_input):
    """Processa a entrada do usuário e obtém resposta da crew"""
    try:
        # Executa a crew com a pergunta do usuário
        result = st.session_state.crew_instance.crew().kickoff(
            inputs={"question": user_input}
        )
        
        # Converte o resultado para string se necessário
        if hasattr(result, 'raw'):
            response = result.raw
        else:
            response = str(result)
        
        return response
    
    except Exception as e:
        st.error(f"Erro ao processar pergunta: {str(e)}")
        return "Desculpe, ocorreu um erro ao processar sua pergunta. Tente novamente."

def main():
    """Função principal da aplicação"""
    
    # Header principal
    st.markdown("""
    <div class="main-header">
        <img src="https://vmbinvest.com.br/wp-content/uploads/2022/12/marca-vmb.png" class="vmb-logo" alt="VMB Invest">
        <h1>🤖 VMB Invest DemoBot</h1>
        <p>Assistente Virtual Especializado para Médicos PJ</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Inicializa estado da sessão
    initialize_session_state()
    
    # Área principal do chat
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Inicializa a crew
        if not create_crew_instance():
            st.stop()
        
        # Mensagem de boas-vindas
        if not st.session_state.conversation_started:
            welcome_message = """
            Olá! 👋 Sou o assistente virtual da VMB Invest, especializado em ajudar médicos que trabalham como PJ 
            com suas necessidades de organização financeira e investimentos.
            
            Como posso ajudá-lo hoje? Você pode me perguntar sobre:
            • Organização financeira
            • Proteção patrimonial
            • Investimentos
            • Planejamento de aposentadoria
            • Ou qualquer outra dúvida financeira
            """
            add_message("assistant", welcome_message)
            st.session_state.conversation_started = True
        
        # Exibe histórico de mensagens
        st.markdown("### 💬 Conversa")
        display_chat_history()
        
        # Campo de entrada para nova mensagem usando st.chat_input
        if prompt := st.chat_input("Digite sua pergunta (Ex: Como posso organizar melhor minhas finanças como médico PJ?)"):
            # Adiciona mensagem do usuário
            add_message("user", prompt)
            
            # Exibe mensagem do usuário imediatamente
            with st.chat_message("user", avatar="👤"):
                st.write(prompt)
            
            # Processa e obtém resposta
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖 Processando sua pergunta..."):
                    bot_response = process_user_input(prompt)
                    st.write(bot_response)
                    
                    # Adiciona resposta do bot ao histórico
                    add_message("assistant", bot_response)
        
        # Botão para limpar conversa
        col_clear = st.columns([1, 1, 1])
        with col_clear[1]:
            if st.button("🗑️ Limpar Conversa", use_container_width=True):
                st.session_state.messages = []
                st.session_state.conversation_started = False
                st.rerun()
    
    with col2:
        st.markdown("### 🎯 Dicas Rápidas")
        
        # Botões de perguntas frequentes
        quick_questions = [
            "Como organizar minhas finanças?",
            "Qual a melhor reserva de emergência?",
            "Como proteger meu patrimônio?",
            "Investimentos para médicos PJ",
            "Planejamento de aposentadoria"
        ]
        
        st.markdown("**Perguntas frequentes:**")
        for question in quick_questions:
            if st.button(question, key=f"quick_{question}", use_container_width=True):
                add_message("user", question)
                bot_response = process_user_input(question)
                add_message("assistant", bot_response)
                st.rerun()

if __name__ == "__main__":
    main()
