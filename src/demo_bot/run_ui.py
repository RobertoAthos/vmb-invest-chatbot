#!/usr/bin/env python
"""
Script para executar a interface Streamlit do VMB Invest DemoBot
"""
import subprocess
import sys
import os

def run_streamlit():
    """Executa a aplicação Streamlit"""
    try:
        # Caminho para o arquivo da aplicação Streamlit
        app_path = os.path.join(os.path.dirname(__file__), "streamlit_app.py")
        
        print("🚀 Iniciando VMB Invest DemoBot...")
        print("📱 A interface será aberta no seu navegador em breve...")
        print("🔗 URLs disponíveis:")
        print("   • Local: http://localhost:8501")
        print("   • Rede local: http://192.168.1.4:8501 (pode variar)")
        print("\n💡 Para parar a aplicação, pressione Ctrl+C\n")
        
        # Executa o Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", app_path,
            "--server.headless", "true",
            "--theme.base", "light",
            "--theme.primaryColor", "#2a5298",
            "--theme.backgroundColor", "#ffffff",
            "--theme.secondaryBackgroundColor", "#f0f2f6"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada pelo usuário.")
    except Exception as e:
        print(f"❌ Erro ao iniciar a aplicação: {e}")
        print("\n💡 Certifique-se de que o Streamlit está instalado:")
        print("   pip install streamlit")

if __name__ == "__main__":
    run_streamlit()
