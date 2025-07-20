# LLM Chatbot Backend

Backend FastAPI modular para chatbot usando LlamaIndex e Gemini SDK.

## 🚀 Funcionalidades

- ✅ **API REST** com FastAPI
- ✅ **Busca contextual** com LlamaIndex (opcional)
- ✅ **LLM Gemini** para geração de respostas
- ✅ **Arquitetura modular** e escalável
- ✅ **Documentação automática** (Swagger)
- ✅ **Health checks** e logs
- ✅ **Fallback robusto** se dependências falharem

## ⚡ Instalação Rápida

### Opção 1: Instalação Simplificada (Recomendada)

```bash
cd backend

# 1. Instala dependências essenciais
python install_essential.py

# 2. Configura .env (edite sua GEMINI_API_KEY)
# O arquivo será criado automaticamente

# 3. Inicia servidor
python simple_start.py
```

### Opção 2: Instalação Completa

```bash
cd backend
python setup.py
```

### Opção 3: Manual

```bash
cd backend
pip install fastapi uvicorn python-dotenv google-generativeai
python simple_start.py
```

## 🔧 Configuração

### 1. API Key do Gemini
- Obtenha sua chave em: https://makersuite.google.com/app/apikey
- Edite o arquivo `.env` e configure `GEMINI_API_KEY`

### 2. Dados (Opcional)
- Adicione arquivos `.txt` na pasta `data/`
- Ou use os dados de exemplo incluídos

## 🌐 Uso da API

### Endpoint Principal - Chat
```http
POST /chat
Content-Type: application/json

{
  "question": "Quais são os principais serviços da Total?"
}
```

**Resposta:**
```json
{
  "answer": "A Total oferece diversos serviços na área de energia...",
  "status": "success"
}
```

### Health Check
```http
GET /health
```

### Documentação
Acesse: `http://localhost:8000/docs`

## � Estrutura Robusta

O sistema tem **3 níveis de fallback**:

1. **Ideal**: LlamaIndex + Gemini (busca contextual avançada)
2. **Funcional**: Gemini direto + arquivos de contexto
3. **Básico**: Gemini puro (sem contexto local)

## 📁 Estrutura do Projeto

```
backend/
├── app/
│   ├── main.py              # Entry point FastAPI
│   ├── routes.py            # Endpoints da API
│   ├── llm_utils.py         # LlamaIndex + Gemini (flexível)
│   ├── config.py            # Configurações
│   ├── index_builder.py     # Construção do índice (opcional)
│   └── scraper.py           # Scraper para dados (opcional)
├── data/                    # Documentos para indexação
├── install_essential.py     # Instalação básica
├── simple_start.py          # Início simplificado
├── setup.py                 # Instalação completa
├── test_api.py              # Testes da API
├── requirements.txt         # Dependências
├── .env                     # Variáveis de ambiente
└── README.md
```

## 🛠️ Scripts Disponíveis

### `install_essential.py`
- Instala apenas dependências essenciais
- Mais rápido e confiável
- Funciona mesmo com problemas de compilação

### `simple_start.py`
- Inicia servidor com configuração mínima
- Cria arquivos necessários automaticamente
- Funciona com dependências básicas

### `setup.py`
- Instalação completa com todas as funcionalidades
- Inclui LlamaIndex e indexação avançada
- Pode falhar em alguns ambientes

### `test_api.py`
- Testa todos os endpoints
- Modo interativo de chat
- Útil para validar instalação

## � Troubleshooting

### Erro de Compilação (Rust/pydantic-core)
```bash
# Use instalação simplificada
python install_essential.py
python simple_start.py
```

### LlamaIndex não funciona
- O sistema funciona sem LlamaIndex
- Use arquivos .txt na pasta `data/` como contexto
- Fallback automático para Gemini direto

### Dependências faltando
```bash
# Instale manualmente as essenciais
pip install fastapi uvicorn python-dotenv google-generativeai
```

### Problemas com .env
- O arquivo será criado automaticamente
- Configure apenas `GEMINI_API_KEY=sua_chave_aqui`

## 🎯 Testando a Instalação

1. **Teste simples**:
   ```bash
   python simple_start.py
   # Acesse: http://localhost:8000/docs
   ```

2. **Teste da API**:
   ```bash
   python test_api.py
   ```

3. **Chat interativo**:
   ```bash
   python test_api.py chat
   ```

## ✅ Validação

O sistema está funcionando se:
- ✅ Servidor inicia em `http://localhost:8000`
- ✅ `/docs` mostra documentação Swagger
- ✅ `/health` retorna status "healthy"
- ✅ `/chat` responde a perguntas

## � Próximos Passos

- [ ] Adicionar seus próprios dados na pasta `data/`
- [ ] Configurar LlamaIndex para busca avançada
- [ ] Implementar autenticação
- [ ] Adicionar cache de respostas
- [ ] Deploy em produção

## � Dependências

### Essenciais (sempre funcionam)
- fastapi
- uvicorn
- python-dotenv  
- google-generativeai

### Opcionais (funcionalidades avançadas)
- llama-index-core
- llama-index-llms-gemini
- requests, beautifulsoup4 (scraping)

## 📝 Licença

MIT License - veja o arquivo LICENSE para detalhes.
