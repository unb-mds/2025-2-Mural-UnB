# 🐍 Scripts de Backend e ETL

Esta pasta contém os scripts Python responsáveis pela extração, transformação e carregamento (ETL) dos dados, além das integrações com IA (Google Gemini).

## ⚙️ Configuração Inicial

Antes de executar qualquer script, certifique-se de estar na **raiz do projeto**:

1.  **Ative o ambiente virtual:**
    ```bash
    source venv/bin/activate
    # Windows: venv\Scripts\activate
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    pip install -r requirements-EJ.txt
    ```

3.  **Configuração de API (Gemini):**
    Para os scripts de IA funcionarem, crie um arquivo `.env` na raiz do projeto contendo sua chave:
    ```env
    GOOGLE_API_KEY="sua_chave_aqui"
    ```

---

## 🚀 Pipelines de Execução

Os comandos abaixo devem ser executados a partir da raiz do projeto.

### 1. Pipeline de Laboratórios (FGA)
Responsável por baixar o portfólio, extrair textos e buscar imagens na web.

```bash
# 1. Baixar o PDF oficial da UnB
python scripts/labs_pdf.py

# 2. Extrair dados, buscar imagens na web e gerar CSV
python scripts/extrair_labs_fga.py
```

Saída: data/Labs/labs_fga.csv e imagens em data/images/labs/.

### 2. Pipeline de Empresas Juniores (EJs)
Extrai dados dos editais e portfólios das EJs.

```bash
python scripts/extrair_empresas_juniores.py
```

### 3. Pipeline de Inteligência Artificial (Embeddings)
Gera vetores semânticos para permitir a busca inteligente e categorização.

```bash

# 1. Gerar embeddings para as tags base
python scripts/generate_embeddings_gemini.py

# 2. Alocar tags aos laboratórios baseado em similaridade semântica
python scripts/alocar_tags_embeddings.py
```
## 🧪 Testes e Qualidade
O projeto utiliza pytest para testes unitários (com mocks de rede/arquivos) e pylint para análise estática.

```bash
# Rodar todos os testes unitários
pytest -v

# Verificar qualidade e estilo do código
pylint scripts
```