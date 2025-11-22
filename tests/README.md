# Testes de Unidade e Qualidade (Scripts Python)

Esta pasta contém os testes unitários para os scripts Python localizados na pasta `/scripts`.

## Ferramentas Utilizadas

* **Pytest:** Para a execução dos testes unitários.
* **Pytest-Mock:** Para "mockar" (simular) chamadas externas, como requisições de internet (`requests`, `ddgs`) e leitura/escrita de arquivos, permitindo testes isolados e rápidos.
* **Pylint:** Para checagem de qualidade de código (linter).
* **Pytest-cov:** Para geração de relatórios de cobertura de código.
* **Requests-mock:** Para mock de requisições HTTP.

## Como Rodar os Testes

1.  **Ative o Ambiente Virtual:**
    Certifique-se de que você está na raiz do projeto e que o `venv` está ativado:
    ```bash
    source venv/bin/activate
    ```

2.  **Instale as Dependências de Teste:**
    Se for a primeira vez, instale as dependências de desenvolvimento:
    ```bash
    pip install -r requirements-EJs-dev.txt
    ```

3.  **Execute o Pytest:**
    Para rodar todos os testes de forma verbosa (mostrando o nome de cada teste):
    ```bash
    pytest -v
    ```
    
    Para rodar testes com cobertura:
    ```bash
    pytest --cov=scripts --cov-report=html
    ```

4.  **Execute Testes Específicos:**
    ```bash
    # Testes de um arquivo específico
    pytest test_pdf_processor_ejs.py -v
    
    # Testes com uma marca específica
    pytest -m "not slow" -v
    ```

5.  **Execute o Pylint:**
    Para checar a qualidade do código na pasta `scripts`:
    ```bash
    pylint scripts
    ```

## Estrutura dos Testes

- `test_pdf_processor_ejs.py`: Testes para processamento de PDFs e extração de informações
- `test_pdf_crawler_ejs.py`: Testes para o crawler de PDFs
- `test_oportunidade_embd_ejs.py`: Testes para agregação de embeddings
- `test_extrair_empresas_juniores.py`: Testes para o script principal de extração
- `test_alocar_tags_ejs.py`: Testes para alocação de tags usando embeddings
- `conftest.py`: Configurações globais do pytest
- `requirements-dev.txt`: Dependências para desenvolvimento e testes

## Cobertura de Testes

Os testes (EJs) cobrem:
- Processamento de PDFs e extração de texto
- Download e manipulação de arquivos
- Integração com API Gemini (com mocks)
- Cálculo de similaridade de embeddings
- Filtragem e alocação de tags
- Consolidação de dados e estatísticas
- Tratamento de erros e casos extremos