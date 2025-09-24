Quero que você implemente um backend em **Python + FastAPI** que seja um chatbot de IA especializado no setor petrolífero angolano.  
O sistema deve rodar **tudo localmente**, exceto a chamada ao **Gemini API** para geração de respostas.  
Use minha `GEMINI_API_KEY` via variáveis de ambiente.

---

## 1. Scraping & Ingestão de Conteúdo
- Criar scrapers locais para os sites:
  - [ ] Sonangol (https://sonangol.co.ao)
  - [ ] ANPG (https://anpg.co.ao)
  - [ ] Azule Energy (https://azule-energy.com)
  - [ ] TotalEnergies Angola (https://totalenergies.co.ao)
  - [ ] **PetroAngola** (https://petroangola.com)
- Usar **requests + BeautifulSoup** para páginas estáticas.
- Usar **Playwright** quando o site depender de JavaScript.
- Para cada documento coletado, salvar em disco (JSON ou SQLite):
  - url
  - title
  - publish_date (se existir)
  - texto principal
  - snippet/citação curta
  - CSS selector ou XPath do elemento
  - snapshot_hash (SHA256 do HTML bruto)
  - fetched_at (timestamp)

---

## 2. Indexação & Vetorização (local)
- Usar um modelo **local de embeddings** (por exemplo `sentence-transformers/all-MiniLM-L6-v2` via `sentence-transformers`).
- Armazenar embeddings em um banco vetorial local: **Qdrant** (rodando localmente via Docker) ou **ChromaDB**.
- Indexar chunks de até 500 tokens.
- Guardar junto os metadados (url, title, snippet, selector, publish_date).

---

## 3. API de Consulta (RAG)
- Implementar endpoint `/ask` que recebe:
  ```json
  { "question": "texto da pergunta" }
Pipeline:

Criar embedding da pergunta (modelo local).

Buscar top-K chunks relevantes no Vector DB.

Montar prompt para o Gemini contendo:

Contexto dos documentos recuperados.

Instruções:

Responder de forma profissional.

Sempre citar as fontes no formato:
[1] Título — URL — trecho curto (máx. 25 palavras).

Se houver selector/XPath salvo, incluir também.

Se não houver fonte confiável, responder: "Não encontrei informação verificável sobre isto."

Enviar prompt para Gemini API usando google.generativeai Python SDK (pip install google-generativeai).

Retornar JSON:

json
Copiar código
{
  "answer": "...",
  "sources": [
    {
      "title": "...",
      "url": "...",
      "snippet": "...",
      "selector": "..."
    }
  ],
  "chart": { ... }
}
4. Detecção de Perguntas Analíticas & Gráficos
Se a pergunta contiver palavras-chave como:
“análise, tendência, evolução, variação, gráfico, produção, preço, série temporal” → ativar modo analítico.

Extrair dados numéricos dos documentos recuperados.

Usar pandas + matplotlib para gerar gráficos (linha, barras).

Salvar localmente (/charts/) e expor pelo FastAPI como arquivos estáticos.

Retornar URL do gráfico no JSON:

json
Copiar código
"chart": {
  "type": "image",
  "url": "http://localhost:8000/charts/plot123.png",
  "caption": "Evolução da produção mensal de petróleo (2019–2024)"
}
5. Restrições e Boas Práticas
Tudo deve rodar local: scraping, embeddings, vector DB, gráficos, storage.

Só a geração de resposta (LLM) usa Gemini API (GEMINI_API_KEY via .env).

Respeitar robots.txt e aplicar rate limiting (1 req/s por domínio).

Guardar fetched_at e snapshot_hash para auditoria.

Nunca inventar fonte: só citar URLs realmente indexados.

6. Estrutura do Projeto
bash
Copiar código
app/
  ├── main.py        # FastAPI app
  ├── scraping/      # scrapers de cada site
  ├── ingestion/     # embeddings + indexação
  ├── rag/           # pipeline de consulta
  ├── charts/        # geração de gráficos
  ├── storage/       # arquivos estáticos locais
  └── models/        # schemas Pydantic
7. Exemplo de Fluxo de Pergunta
Usuário pergunta:
"Quem é o PCA da Sonangol?"

Resposta esperada (JSON):

json
Copiar código
{
  "answer": "O PCA da Sonangol é João X, nomeado em janeiro de 2024.",
  "sources": [
    {
      "title": "Sonangol — Conselho de Administração",
      "url": "https://sonangol.co.ao/quem-somos/conselho",
      "snippet": "O PCA da Sonangol é João X desde janeiro de 2024.",
      "selector": "div#board > p:nth-of-type(1)"
    }
  ],
  "chart": null
}
Usuário pergunta:
"Mostra a evolução da produção de petróleo da Angola nos últimos 5 anos."

Resposta esperada (JSON):

json
Copiar código
{
  "answer": "Aqui está a análise da evolução da produção petrolífera angolana entre 2019 e 2024.",
  "sources": [
    {
      "title": "ANPG — Relatório Anual 2024",
      "url": "https://anpg.co.ao/relatorio2024",
      "snippet": "Produção em 2024 foi de 1,1 milhão bpd...",
      "selector": "table#production > tr:nth-of-type(2)"
    }
  ],
  "chart": {
    "type": "image",
    "url": "http://localhost:8000/charts/producao2019-2024.png",
    "caption": "Produção de petróleo (milhões bpd, 2019–2024)"
  }
}
⚡ Implemente exatamente essa arquitetura em FastAPI, rodando localmente, com embeddings locais + Qdrant/ChromaDB e Gemini API para geração final de respostas.
Cada módulo deve ser desacoplado (scraping, ingestão, RAG, gr