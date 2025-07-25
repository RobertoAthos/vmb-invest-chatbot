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
        background: #000000;
        color: #ffffff;
    }
    
    .main .block-container {
        max-width: 1000px;
        padding: 1rem;
        margin: 0 auto;
    }
    
    /* Header principal */
    .main-header {
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(37, 197, 243, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .vmb-logo {
        max-width: 120px;
        height: auto;
        margin-bottom: 0.5rem;
        filter: brightness(1.1);
    }
    
    .header-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(45deg, #25c5f3, #ffffff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.3rem 0;
    }
    
    .header-subtitle {
        color: #b0b0b0;
        font-size: 0.9rem;
        margin: 0.5rem 0;
    }
    
    .header-stats {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
        padding: 0.75rem;
        background: rgba(37, 197, 243, 0.1);
        border-radius: 10px;
        border: 1px solid rgba(37, 197, 243, 0.2);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-value {
        font-size: 1.2rem;
        font-weight: bold;
        color: #25c5f3;
    }
    
    .stat-label {
        font-size: 0.7rem;
        color: #b0b0b0;
        margin-top: 0.2rem;
    }
    
    .status-online {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        color: #00ff88;
        font-size: 0.8rem;
    }
    
    .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #00ff88;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Container do chat */
    .chat-container {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(37, 197, 243, 0.2);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1rem;
        max-height: 500px;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: rgba(37, 197, 243, 0.5) transparent;
    }
    
    .chat-container::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: transparent;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: rgba(37, 197, 243, 0.5);
        border-radius: 3px;
    }
    
    /* Mensagens do chat */
    .stChatMessage {
        margin-bottom: 1rem !important;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #25c5f3, #1a9bc7) !important;
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #00ff88, #00cc6a) !important;
    }
    
    .stChatMessage div {
        color: #ffffff !important;
    }
    
    .message-timestamp {
        font-size: 0.7rem;
        color: #888;
        margin-top: 0.3rem;
        opacity: 0.7;
    }
    
    /* Cards de sugestões */
    .suggestion-cards {
        display: flex;
        gap: 0.5rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    
    .suggestion-card {
        background: rgba(37, 197, 243, 0.1);
        border: 1px solid rgba(37, 197, 243, 0.3);
        border-radius: 10px;
        padding: 0.7rem 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        font-size: 0.85rem;
        color: #ffffff;
        flex: 1;
        min-width: 180px;
        text-align: center;
    }
    
    .suggestion-card:hover {
        background: rgba(37, 197, 243, 0.2);
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(37, 197, 243, 0.3);
    }
    
    /* Input do chat */
    .stChatInputContainer {
        background: transparent !important;
        border: 1px solid rgba(37, 197, 243, 0.3) !important;
        border-radius: 15px !important;
    }

    
    .stChatInputContainer input {
        background: transparent !important;
        color: #ffffff !important;
        border: none !important;
    }
    
    .stChatInputContainer input::placeholder {
        color: #888 !important;
    }
    
    /* Container inferior com background transparente */
    .stBottomBlockContainer {
        background: transparent !important;
    }
    
    /* Ocultar elementos desnecessários */
    .stDeployButton {display:none;}
    footer {visibility: hidden;}
    .stDecoration {display:none;}
    header[data-testid="stHeader"] {display:none;}
    
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
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 197, 243, 0.4);
        background: linear-gradient(135deg, #1a9bc7, #25c5f3);
    }
    
    /* Spinner customizado */
    .stSpinner > div {
        border-color: #25c5f3 transparent transparent transparent !important;
    }
    
    /* Alertas customizados */
    .stAlert {
        background: rgba(37, 197, 243, 0.1) !important;
        border: 1px solid rgba(37, 197, 243, 0.3) !important;
        border-radius: 10px !important;
        color: #ffffff !important;
    }
    
    /* Ações do footer */
    .footer-actions {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(255, 255, 255, 0.02);
        border-radius: 15px;
        border: 1px solid rgba(37, 197, 243, 0.1);
    }
    
    /* Loading indicator personalizado */
    .typing-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 1rem;
        background: rgba(37, 197, 243, 0.1);
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    
    .typing-dots {
        display: flex;
        gap: 0.3rem;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background: #25c5f3;
        border-radius: 50%;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    
    @keyframes typing {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
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
    if 'message_count' not in st.session_state:
        st.session_state.message_count = 0
    if 'session_start_time' not in st.session_state:
        st.session_state.session_start_time = datetime.now()

def get_quick_suggestions():
    """Retorna sugestões rápidas para o usuário"""
    return [
        "💼 Como organizar minhas finanças?",
        "🏦 Qual o melhor investimento para mim?", 
        "🛡️ Como proteger meu patrimônio?",
        "📈 Planejamento de aposentadoria",
        "💳 Organização para médicos PJ",
        "🎯 Diversificação de investimentos"
    ]

def display_typing_indicator():
    """Exibe indicador de digitação"""
    return st.markdown("""
    <div class="typing-indicator">
        <span>🤖 Assistente está digitando</span>
        <div class="typing-dots">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_header_with_stats():
    """Cria o header principal com estatísticas da sessão"""
    # Calcula estatísticas da sessão
    session_duration = datetime.now() - st.session_state.session_start_time
    hours, remainder = divmod(session_duration.total_seconds(), 3600)
    minutes, _ = divmod(remainder, 60)
    
    # Header principal com estatísticas
    st.markdown(f"""
    <div class="main-header">
        <img src="https://vmbinvest.com.br/wp-content/uploads/2022/12/marca-vmb.png" class="vmb-logo" alt="VMB Invest">
        <h1 class="header-title">VMB Invest DemoBot</h1>
        <p class="header-subtitle">Seu assistente especializado em organização financeira e investimentos</p>
    </div>
    """, unsafe_allow_html=True)

def create_crew_instance():
    """Cria uma instância da crew se ainda não existir"""
    if st.session_state.crew_instance is None:
        with st.status("🚀 Inicializando assistentes VMB...", expanded=True) as status:
            try:
                st.write("🔄 Carregando módulos de IA...")
                st.session_state.crew_instance = DemoBot()
                st.write("✅ Assistentes carregados com sucesso!")
                st.write("🎯 Sistema pronto para atendimento!")
                status.update(label="✅ Assistentes VMB Online!", state="complete", expanded=False)
                return True
            except Exception as e:
                st.write(f"❌ Erro: {str(e)}")
                status.update(label="❌ Erro na inicialização", state="error", expanded=True)
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
    
    # Incrementa contador de mensagens
    st.session_state.message_count += 1

def display_chat_history():
    """Exibe o histórico de mensagens usando st.chat_message com container"""
    if st.session_state.messages:
        # Container do chat com scroll
        chat_container = st.container()
        with chat_container:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            
            for i, message in enumerate(st.session_state.messages):
                if message["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.write(message["content"])
                        st.markdown(f'<div class="message-timestamp">{message["timestamp"]}</div>', 
                                  unsafe_allow_html=True)
                else:
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(message["content"])
                        st.markdown(f'<div class="message-timestamp">{message["timestamp"]}</div>', 
                                  unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

def display_suggestion_cards():
    """Exibe cards de sugestões rápidas"""
    suggestions = get_quick_suggestions()
    
    st.markdown("### 💡 Sugestões Rápidas")
    
    # Criar cards em linhas de 3
    for i in range(0, len(suggestions), 3):
        cols = st.columns(3)
        for j, suggestion in enumerate(suggestions[i:i+3]):
            with cols[j]:
                if st.button(suggestion, use_container_width=True, key=f"suggestion_{i+j}"):
                    # Simula o envio da sugestão
                    return suggestion.split(' ', 1)[1] if ' ' in suggestion else suggestion
    return None

def process_user_input(user_input):
    """Processa a entrada do usuário e obtém resposta da crew"""
    try:
        # Validação básica do input
        if not user_input.strip():
            return "Por favor, digite uma pergunta válida."
        
        # Executa a crew com a pergunta do usuário
        result = st.session_state.crew_instance.crew().kickoff(
            inputs={"question": user_input}
        )
        
        # Converte o resultado para string se necessário
        if hasattr(result, 'raw'):
            response = result.raw
        else:
            response = str(result)
        
        # Validação da resposta
        if not response or response.strip() == "":
            return "Desculpe, não consegui gerar uma resposta adequada. Pode reformular sua pergunta?"
        
        return response
    
    except Exception as e:
        error_msg = str(e)
        st.error(f"⚠️ Erro ao processar pergunta: {error_msg}")
        
        # Mensagem de erro mais amigável
        friendly_errors = {
            "connection": "Problema de conexão. Verifique sua internet e tente novamente.",
            "timeout": "A resposta está demorando mais que o esperado. Tente uma pergunta mais específica.",
            "invalid": "Formato de pergunta inválido. Tente reformular sua pergunta."
        }
        
        for key, msg in friendly_errors.items():
            if key in error_msg.lower():
                return f"🚨 {msg}\n\nDetalhes técnicos: {error_msg}"
        
        return f"""
        🚨 Ops! Algo deu errado ao processar sua pergunta.
        
        **Sugestões:**
        • Tente reformular sua pergunta
        • Verifique sua conexão com a internet  
        • Use uma pergunta mais específica
        
        Se o problema persistir, entre em contato conosco.
        
        **Erro técnico:** {error_msg}
        """

def main():
    """Função principal da aplicação"""
    
    # Inicializa estado da sessão
    initialize_session_state()
    
    # Header principal com estatísticas
    create_header_with_stats()
    
    # Inicializa a crew
    if not create_crew_instance():
        st.stop()
    
    # Mensagem de boas-vindas
    if not st.session_state.conversation_started:
        welcome_message = """
        Olá! 👋 Sou o assistente virtual da VMB Invest, especializado em ajudar com suas necessidades de organização financeira e investimentos.
        
        Como posso ajudá-lo hoje? Você pode me perguntar sobre:
        • 💼 Organização financeira
        • 🛡️ Proteção patrimonial  
        • 📈 Investimentos
        • 🏥 Planejamento de aposentadoria
        • 🩺 Soluções para médicos PJ
        • 🎯 Ou qualquer outra dúvida financeira
        
        Use as sugestões abaixo ou digite sua própria pergunta!
        """
        add_message("assistant", welcome_message)
        st.session_state.conversation_started = True
    
    # Exibe histórico de mensagens
    if len(st.session_state.messages) > 0:
        st.markdown("### 💬 Conversa")
        display_chat_history()
    
    # Cards de sugestões (apenas se não houver muitas mensagens)
    if len(st.session_state.messages) <= 2:
        suggested_prompt = display_suggestion_cards()
        if suggested_prompt:
            # Se uma sugestão foi clicada, processa imediatamente
            add_message("user", suggested_prompt)
            
            with st.chat_message("user", avatar="👤"):
                st.write(suggested_prompt)
                st.markdown(f'<div class="message-timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                          unsafe_allow_html=True)
            
            with st.chat_message("assistant", avatar="🤖"):
                with st.spinner("🤖 Processando sua pergunta..."):
                    bot_response = process_user_input(suggested_prompt)
                    st.write(bot_response)
                    st.markdown(f'<div class="message-timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                              unsafe_allow_html=True)
                    add_message("assistant", bot_response)
            
            # Força atualização da página para mostrar o input novamente
            st.rerun()
    
    # Campo de entrada para nova mensagem
    placeholder_text = "Digite sua pergunta aqui... (Ex: Como posso organizar melhor minhas finanças como médico PJ?)"
    
    if prompt := st.chat_input(placeholder_text):
        # Adiciona mensagem do usuário
        add_message("user", prompt)
        
        # Exibe mensagem do usuário imediatamente  
        with st.chat_message("user", avatar="👤"):
            st.write(prompt)
            st.markdown(f'<div class="message-timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                      unsafe_allow_html=True)
        
        # Processa e obtém resposta
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤖 Processando sua pergunta..."):
                bot_response = process_user_input(prompt)
                st.write(bot_response)
                st.markdown(f'<div class="message-timestamp">{datetime.now().strftime("%H:%M")}</div>', 
                          unsafe_allow_html=True)
                add_message("assistant", bot_response)
        
        # Força atualização da página
        st.rerun()
    
    # Rodapé informativo
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.8rem; padding: 1rem; margin-top: 2rem; border-top: 1px solid rgba(37, 197, 243, 0.2);">
        💡 <strong>Dica:</strong> Use as sugestões rápidas ou digite suas próprias perguntas<br>
        🔒 Suas conversas são privadas e seguras | 🚀 Powered by VMB Invest AI
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
