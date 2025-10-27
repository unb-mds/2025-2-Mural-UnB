# Arquitetura de Dados

A arquitetura de dados do MuralUnB é uma pipeline de ingestão offline, projetado para operar com custo zero e manutenção mínima.

Todo o processo de coleta, transformação e vetorização de dados não ocorre em tempo real. Em vez disso, ele é executado de forma assíncrona como um workflow automatizado (via GitHub Actions), que lê os dados de origem (PDFs de portfólios) e os transforma nos bancos de dados JSON estáticos que alimentam o Frontend.

Este pipeline é o único componente que interage com a API de Inteligência Artificial (Google Gemini) e é o responsável por pré-calcular todos os vetores semânticos.

---

## O Caminho dos Dados (Pipeline de Ingestão)

O fluxo de dados segue uma sequência linear e clara, orquestrada por scripts Python dentro de um workflow do GitHub Actions. O processo, ilustrado no container "Dados" do Diagrama de Componentes, pode ser dividido nas seguintes etapas:

### 1. Extração dos Dados Brutos (Input)

**Fonte:** O pipeline começa consumindo os arquivos de origem, primariamente os portfólios de empresas juniores, laboratórios e projetos de pesquisa da UnB (ex: "Portfólio das Empresas Juniores da UnB.pdf").

**Componente:** PDF Extractor

**Ação:** Este script Python é responsável por abrir os arquivos PDF, ler seu conteúdo página por página e extrair todo o texto bruto. O resultado desta etapa é uma massa de dados textuais não estruturados, contendo todas as informações dos portfólios.

---

### 2. Formatação e Normalização

**Componente:** Data Handler

**Ação:** O texto bruto extraído é enviado para o Data Handler. Este é um componente crítico que atua como o "cérebro" da transformação. Suas responsabilidades são:

- **Limpar:** Remover ruídos, quebras de linha desnecessárias, cabeçalhos/rodapés de página e outros artefatos do PDF.  
- **Normalizar:** Padronizar o texto (ex: converter para minúsculas, remover acentos para certas chaves).  
- **Estruturar:** Utilizar heurísticas e regras de negócio para identificar e separar as entidades de dados, como o nome de uma oportunidade, sua descrição, suas tags associadas (categorias, tecnologias, etc.) e links.

**Saída:** Ao final desta etapa, temos objetos de dados estruturados (ex: uma lista de Oportunidades e uma lista de Tags) prontos para serem vetorizados.

---

### 3. Vetorização (IA)

**Componente:** Content Embedding (utilizando Gemini - Embedding)

**Ação:** Os dados textuais limpos (como as descrições das oportunidades e os nomes das tags) são enviados para este componente. Ele atua como um cliente para a API do Google Gemini (ex: text-embedding-bison).

**Processo:** O serviço Content Embedding envia o conteúdo textual para o Gemini, que realiza a "Vetorização". Para cada pedaço de texto (ex: "Desenvolvimento Web com React") ele retorna um embedding: um vetor numérico de alta dimensão que representa o significado semântico daquele texto.

---

### 4. Escrita e Persistência (Output)

**Componente:** Vector Writer Service

**Ação:** Este serviço é o orquestrador final que monta os bancos de dados estáticos. Ele recebe duas fontes de informação:

- Os dados estruturados (metadata) vindos do Data Handler (títulos, links, etc.).  
- Os vetores semânticos correspondentes vindos do Content Embedding.

**Processo:** O serviço "funde" essas informações. Cada objeto de oportunidade agora contém seus metadados e um campo `vector` com seu embedding. O mesmo ocorre com as tags.

**Saída Final:** O componente salva os dados processados nos dois bancos de dados JSON estáticos do projeto:

- **Oportunidades DB [Container: JSON]:** Um arquivo JSON contendo um array de todos os objetos de oportunidade, cada um com seus detalhes e seu vetor.  
- **Tags DB [Container: JSON]:** Um arquivo JSON contendo um array de todos os objetos de tags, cada um com seu nome, categoria e vetor.

---

## Automação com GitHub Actions

Todo o pipeline descrito acima é executado dentro de um workflow do GitHub Actions.

- **Disparo:** O workflow é configurado para rodar/disparar quando há novos portfólios para processar.  
- **Execução:** O Action executa os scripts Python (PDF Extractor, Data Handler, etc.) em um executor do GitHub. Ele utiliza um secret (chave de API) para se autenticar com segurança na API do Gemini durante a etapa de vetorização.  
- **Deploy:** Ao final da execução bem-sucedida, o workflow faz um commit e push dos novos arquivos `Oportunidades DB.json` e `Tags DB.json` diretamente para o repositório.  
- **Atualização:** Como o Frontend é servido pelo GitHub Pages, no momento em que esses arquivos são atualizados no repositório, a aplicação web passa a consumir os dados mais recentes na próxima vez que o usuário carregar a página.

---

Este modelo garante que o sistema de consulta do usuário seja extremamente rápido (pois apenas consome arquivos estáticos) e que o processo de atualização de dados seja totalmente automatizado e sem custos.