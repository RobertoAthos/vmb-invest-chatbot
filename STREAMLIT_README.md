# 🤖 VMB Invest DemoBot - Interface Streamlit

Uma interface web moderna e interativa para o VMB Invest DemoBot, especializado em atendimento a médicos PJ.

## 🚀 Como executar

### 1. Instalar dependências

```bash
cd demo_bot
uv sync
```

### 2. Executar a interface

**Opção 1: Usando o comando configurado**
```bash
uv run ui
```

**Opção 2: Executando diretamente**
```bash
uv run streamlit run src/demo_bot/streamlit_app.py
```

**Opção 3: Usando o script de execução**
```bash
uv run python src/demo_bot/run_ui.py
```

## 🎨 Funcionalidades

### Interface Principal
- **Chat em tempo real** com os assistentes especializados
- **Design responsivo** que funciona em desktop e mobile
- **Histórico de conversa** persistente durante a sessão
- **Indicadores visuais** para status de processamento

### Sidebar Interativa
- **Informações do sistema** e instruções de uso
- **Estatísticas da conversa** em tempo real
- **Botão de limpeza** para reiniciar a conversa
- **Perguntas frequentes** para acesso rápido

### Recursos Avançados
- **Botões de pergunta rápida** para tópicos comuns
- **Timestamps** em todas as mensagens
- **Tratamento de erros** com mensagens amigáveis
- **Tema customizado** com cores da VMB Invest

## 🎯 Fluxo de Uso

1. **Inicialização**: Os assistentes são carregados automaticamente
2. **Boas-vindas**: Mensagem de apresentação e orientações
3. **Interação**: Digite perguntas ou use os botões de acesso rápido
4. **Processamento**: A crew processa a pergunta com os 3 agentes
5. **Resposta**: Retorno especializado baseado na configuração YAML

## 🔧 Configuração

A interface utiliza as mesmas configurações da crew:
- **Agentes**: Definidos em `config/agents.yaml`
- **Tasks**: Definidas em `config/tasks.yaml`
- **Ferramentas**: JSONSearchTool para QA

## 🎨 Personalização

### Cores e Tema
As cores podem ser modificadas no arquivo `streamlit_app.py`:
```python
# CSS customizado na seção <style>
primary_color = "#2a5298"
background_color = "#ffffff"
secondary_bg_color = "#f0f2f6"
```

### Mensagens e Textos
- Mensagem de boas-vindas
- Perguntas frequentes
- Textos da sidebar
- Placeholders dos campos

## 📱 Compatibilidade

- **Navegadores**: Chrome, Firefox, Safari, Edge
- **Dispositivos**: Desktop, tablet, mobile
- **Resolução**: Responsivo para todas as telas

## 🚨 Solução de Problemas

### Erro "streamlit not found"
```bash
uv add streamlit
```

### Erro na inicialização da crew
Verifique se todas as dependências do crewAI estão instaladas:
```bash
uv sync
```

### Interface não abre
Verifique se a porta 8501 está disponível ou use:
```bash
uv run streamlit run src/demo_bot/streamlit_app.py --server.port 8502
```

## 📊 Monitoramento

A interface inclui métricas básicas:
- Número de mensagens na conversa
- Timestamp da última atividade
- Status dos assistentes

## 🔮 Próximas Funcionalidades

- [ ] Exportação de conversas
- [ ] Temas personalizáveis
- [ ] Integração com analytics
- [ ] Chat com múltiplas sessões
- [ ] Feedback do usuário
- [ ] Histórico persistente

---

**Desenvolvido para VMB Invest** | Especialistas em soluções financeiras para médicos PJ
