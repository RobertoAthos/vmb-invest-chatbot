#!/usr/bin/env python
import streamlit as st
import warnings
from datetime import datetime
from demo_bot.crew import DemoBot

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Configuração da página
st.set_page_config(
    page_title="VMB Invest DemoBot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    /* Fundo geral da aplicação */
    .stApp {
        background-color: #000000;
        color: #25c5f3;
    }
    
    /* Container principal */
    .main .block-container {
        background-color: #000000;
        padding-top: 1rem;
    }
    
    .main-header {
        text-align: center;
        padding: 1.5rem;
        background-color: #000000;
        color: #25c5f3;
        border: 2px solid #25c5f3;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 0 20px rgba(37, 197, 243, 0.3);
    }
    
    .vmb-logo {
        max-width: 200px;
        height: auto;
        margin-bottom: 1rem;
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #25c5f3;
        background-color: rgba(0, 0, 0, 0.8);
    }
    
    .user-message {
        background: linear-gradient(135deg, rgba(37, 197, 243, 0.1), rgba(37, 197, 243, 0.05));
        border-left: 4px solid #25c5f3;
        color: #25c5f3;
    }
    
    .bot-message {
        background: linear-gradient(135deg, rgba(37, 197, 243, 0.15), rgba(37, 197, 243, 0.08));
        border-left: 4px solid #25c5f3;
        color: #ffffff;
    }
    
    /* Estilo dos botões */
    .stButton>button {
        background: linear-gradient(135deg, #25c5f3, #1a9bc7);
        color: #000000;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-weight: bold;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(37, 197, 243, 0.3);
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #1a9bc7, #25c5f3);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 197, 243, 0.5);
    }
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #000000;
        border-right: 2px solid #25c5f3;
    }
    
    .sidebar .sidebar-content {
        background-color: #000000;
        color: #25c5f3;
    }
    
    /* Input fields */
    .stTextInput>div>div>input {
        background-color: #000000;
        color: #25c5f3;
        border: 2px solid #25c5f3;
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #25c5f3;
        box-shadow: 0 0 10px rgba(37, 197, 243, 0.5);
    }
    
    /* Métricas */
    .metric-container {
        background-color: rgba(37, 197, 243, 0.1);
        border: 1px solid #25c5f3;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Textos gerais */
    .stMarkdown, .stText {
        color: #25c5f3;
    }
    
    /* Título das seções */
    h1, h2, h3, h4, h5, h6 {
        color: #25c5f3 !important;
    }
    
    /* Warning e success messages */
    .stAlert {
        background-color: rgba(37, 197, 243, 0.1);
        border: 1px solid #25c5f3;
        color: #25c5f3;
    }
    
    /* Spinner customizado */
    .stSpinner {
        color: #25c5f3;
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
    """Exibe o histórico de mensagens"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 Você ({message["timestamp"]})</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message bot-message">
                <strong>🤖 VMB Invest Assistant ({message["timestamp"]})</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

def process_user_input(user_input):
    """Processa a entrada do usuário e obtém resposta da crew"""
    try:
        with st.spinner("🤖 Processando sua pergunta..."):
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
        if st.session_state.messages:
            display_chat_history()
        
        # Campo de entrada para nova mensagem
        with st.container():
            col_input, col_btn_send, col_btn_clear = st.columns([4, 1, 1])
            
            with col_input:
                user_input = st.text_input(
                    "Digite sua pergunta:",
                    key="user_input",
                    placeholder="Ex: Como posso organizar melhor minhas finanças como médico PJ?"
                )
            
            with col_btn_send:
                send_button = st.button("📤 Enviar", use_container_width=True)
            
            with col_btn_clear:
                if st.button("�️ Limpar", use_container_width=True):
                    st.session_state.messages = []
                    st.session_state.conversation_started = False
                    st.rerun()
            
            # Processa entrada do usuário
            if send_button and user_input.strip():
                # Adiciona mensagem do usuário
                add_message("user", user_input)
                
                # Processa e obtém resposta
                bot_response = process_user_input(user_input)
                
                # Adiciona resposta do bot
                add_message("assistant", bot_response)
                
                # Limpa o campo de entrada e atualiza a página
                st.rerun()
            
            elif send_button and not user_input.strip():
                st.warning("Por favor, digite uma pergunta antes de enviar.")
    
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
