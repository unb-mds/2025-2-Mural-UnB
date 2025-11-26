# 💾 Documentação de Dados (Data Dictionary)

Esta pasta armazena os dados brutos (PDFs), processados (CSV/JSON) e multimídia (Imagens) do projeto. O fluxo segue o padrão ETL (Extract, Transform, Load).

## 📂 Estrutura de Diretórios

* **`Labs/`**: Dados específicos dos Laboratórios da FGA.
    * `Portfolio_Infraestrutura_UnB.pdf`: Documento oficial bruto (Fonte da verdade).
    * `labs_fga.csv`: Dados estruturados, limpos e enriquecidos (contém caminhos para imagens).
    * `labs_com_tags_embeddings.json`: Arquivo final para o Frontend (contém vetores de IA).
* **`EJs/`**: Dados das Empresas Juniores (PDFs e JSONs extraídos).
* **`images/`**: Banco de imagens local.
    * `labs/`: Imagens reais capturadas dos sites dos laboratórios via Web Scraping.
    * `placeholders/`: Imagens genéricas categorizadas (ex: software, eletrônica) usadas como fallback.
* **`mock/`**: Dados estáticos para testes unitários.

## 📄 Dicionário de Dados: `labs_fga.csv`

Este arquivo é o artefato principal gerado pelo script `extrair_labs_fga.py`.

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `id` | String | Identificador único gerado (ex: `200001`). |
| `nome` | String | Nome oficial do laboratório extraído do PDF. |
| `coordenador` | String | Nome do professor responsável. |
| `contato` | String | E-mail institucional ou telefone. |
| `descricao` | String | Descrição completa das atividades e equipamentos. |
| `caminho_imagem` | String | Caminho relativo para a imagem em `../data/images/labs/` ou `placeholders/`. |

## 🧠 Artefatos de IA

* **`tags.json`**: Lista base de tags e categorias.
* **`labs_com_embedding_agregado.json`**: Resultado final do processamento do Gemini, unindo os dados dos laboratórios com tags semânticas.