# Arquitetura de Inteligência Artificial

A Inteligência Artificial no MuralUnB é o motor que possibilita a recomendação semântica de oportunidades. Ela permite que o sistema entenda o significado por trás das tags que o usuário seleciona e encontre as vagas mais relevantes, mesmo que as palavras-chave não correspondam exatamente.

Diferente de uma abordagem tradicional, o MuralUnB não utiliza um servidor de IA em tempo real. Para manter o projeto com custo zero, adotamos uma arquitetura em duas fases:

- **Fase Offline (Geração de Embeddings):** Ocorre durante o pipeline de ingestão de dados. Aqui, usamos um modelo de IA (Google Gemini) para "vetorizar" todo o conteúdo.  
- **Fase Online (Busca Vetorial):** Ocorre no Frontend (no navegador do usuário). Aqui, usamos matemática (Similaridade de Cosseno) para comparar os vetores e criar o ranking de recomendações.

---

## 1. O Conceito Principal: Embeddings (Vetores Semânticos)

Para que a IA funcione, precisamos primeiro converter palavras e frases em um formato que um computador possa entender e comparar: números.  
É aqui que entram os **Embeddings (ou Vetores Semânticos)**.

Pense em um embedding como um endereço em um mapa de significados. Em vez de um endereço com rua e número, é um endereço com centenas de dimensões (ex: 768 números).  

- Palavras ou frases com significados semelhantes (como "programação web", "desenvolvimento frontend" e "React.js") terão "endereços" (vetores) muito próximos nesse mapa.  
- Palavras com significados distintos (como "React.js" e "biologia molecular") terão "endereços" muito distantes.  

No nosso projeto, todo texto relevante (descrições de oportunidades, nomes de tags) é convertido em um vetor numérico.

---

### Geração de Embeddings (Fase Offline)

Como descrito na arquitetura de dados, este processo é feito de forma assíncrona:

1. O **Data Handler** envia um pedaço de texto limpo (ex: "Vaga para designer de interfaces com Figma") para o componente **Content Embedding**.  
2. Este componente usa a API do **Google Gemini** (ex: `text-embedding-bison`) para processar esse texto.  
3. A API do Gemini retorna o embedding: um vetor (uma lista de números) que captura o significado semântico daquele texto.  

**Exemplo:**
```json
"vector": [0.012, -0.45, 0.881, ..., 0.123]
O Vector Writer Service salva esse vetor diretamente no arquivo JSON, associado à sua respectiva oportunidade ou tag.
```
4. O **Vector Writer Service** salva esse vetor diretamente no arquivo JSON, associado à sua respectiva oportunidade ou tag.
## 2. O "Banco de Dados Vetorial": Um JSON Estático

Um "Banco de Dados Vetorial" é, em essência, um sistema otimizado para armazenar e consultar vetores de forma eficiente.

Para manter o custo zero e a simplicidade, nosso banco de dados vetorial é o próprio arquivo JSON estático (ex: `Oportunidades DB.json`).

Não utilizamos um serviço de banco de dados vetorial dedicado (como Pinecone, Weaviate ou ChromaDB).  
A lógica de "banco de dados" é substituída por arquivos estáticos que o frontend baixa e processa na memória.

- **Oportunidades DB.json:** Contém os metadados de cada vaga e seu `vector` pré-calculado.  
- **Tags DB.json:** Contém os nomes das tags e seus `vector` pré-calculados.  

Esta abordagem só é viável porque nosso volume de dados é relativamente pequeno (centenas ou alguns milhares de oportunidades), permitindo que um navegador moderno execute os cálculos de busca em milissegundos.

---

## 3. A Busca Vetorial (Fase Online no Frontend)

Esta é a "mágica" que o usuário vê. Ela acontece inteiramente no cliente, através dos componentes **User Vector Merge** e **Vector Search Service** no Frontend.

O fluxo é o seguinte:

---

### Etapa 1: O Usuário Define o Interesse

O usuário seleciona uma ou mais tags na interface (ex: "Python", "Data Science" e "Inteligência Artificial").

---

### Etapa 2: Cálculo do Vetor de Interesse  
**(Componente: User Vector Merge)**

O sistema não busca cada tag individualmente.  
Em vez disso, ele cria um único **"vetor de interesse"** que representa a combinação dos desejos do usuário.

- O serviço busca os vetores pré-calculados das tags "Python", "Data Science" e "IA" no `Tags DB.json`.  
- Ele então "funde" esses vetores. Uma abordagem comum é calcular a **média** desses vetores, criando um novo vetor que aponta para o **centro semântico** de todos os interesses do usuário.

---

### Etapa 3: Cálculo de Similaridade  
**(Componente: Vector Search Service)**

Agora, o sistema compara este "vetor de interesse" com o vetor de cada oportunidade no `Oportunidades DB.json`.

**Cálculo Matemático:**  
O serviço usa um cálculo chamado **Similaridade de Cosseno (Cosine Similarity)**.

**O que é?**  
A Similaridade de Cosseno mede o ângulo ($\theta$) entre dois vetores.  
Ela não se importa com o "tamanho" (magnitude) do vetor, apenas com a sua "direção" no mapa de significados.

- Se dois vetores apontam exatamente na mesma direção, o ângulo é **0°** e a similaridade é **1** (match perfeito).  
- Se são ortogonais (não relacionados), o ângulo é **90°** e a similaridade é **0** (sem relação).  
- Se apontam em direções opostas, o ângulo é **180°** e a similaridade é **-1** (opostos).

---

### Etapa 4: Ranking e Exibição

O **Vector Search Service** calcula essa pontuação de similaridade (um valor entre -1 e 1) para todas as oportunidades.  
Em seguida, ele simplesmente ordena a lista, da pontuação mais alta para a mais baixa.

A **User Web UI** (interface) exibe essa lista ordenada para o aluno, mostrando as vagas mais relevantes (com maior similaridade) no topo.