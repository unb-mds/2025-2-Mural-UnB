# Testes de Unidade e Qualidade (Scripts Python)

Esta pasta contém os testes unitários para os scripts Python localizados na pasta `/scripts`.

## Ferramentas Utilizadas

* **Pytest:** Para a execução dos testes unitários.
* **Pytest-Mock:** Para "mockar" (simular) chamadas externas, como requisições de internet (`requests`, `ddgs`) e leitura/escrita de arquivos, permitindo testes isolados e rápidos.
* **Pylint:** Para checagem de qualidade de código (linter).

## Como Rodar os Testes

1.  **Ative o Ambiente Virtual:**
    Certifique-se de que você está na raiz do projeto e que o `venv` está ativado:
    ```bash
    source venv/bin/activate
    ```

2.  **Instale as Dependências de Teste:**
    Se for a primeira vez, instale as dependências de desenvolvimento:
    ```bash
    pip install -r requirements-dev.txt
    ```
    (Se o `requirements-dev.txt` não existir, instale manualmente: `pip install pytest pytest-mock pylint`)

3.  **Execute o Pytest:**
    Para rodar todos os testes de forma verbosa (mostrando o nome de cada teste):
    ```bash
    pytest -v
    ```

4.  **Execute o Pylint:**
    Para checar a qualidade do código na pasta `scripts`:
    ```bash
    pylint scripts
    ```