# Módulo de Recomendação por IA

## 1. Visão Geral

O Módulo de Recomendação por Inteligência Artificial é o componente central responsável por personalizar a experiência do usuário na plataforma, indo além de simples buscas por palavras-chave.

O objetivo principal é entender o **significado semântico** dos interesses de um usuário e das características de uma oportunidade, para então conectar os dois de forma inteligente. Em vez de apenas casar a tag "IA" com oportunidades que contenham a palavra "IA", o sistema é capaz de inferir que um usuário interessado em `Intelligência Artificial` também pode se interessar por oportunidades com as tags `Machine Learning`, `Ciência de Dados` e `Processamento de Linguagem Natural`.

Isso é alcançado através do uso de **Embeddings Vetoriais** para representar tags, usuários e oportunidades em um espaço matemático multidimensional.

---

## 2. Arquitetura Lógica e Componentes

A arquitetura do módulo de IA é composta por um conjunto de serviços especializados que trabalham em conjunto.

!!! info "Diagrama de Alto Nível"
    O diagrama abaixo ilustra a interação entre os principais componentes do Módulo de IA e o resto do sistema. Note que o Módulo de IA **não acessa** o Banco de Dados Relacional; ele apenas retorna IDs para o Backend API.

    ```mermaid
    graph TD
        subgraph Sistema Principal
            A[Backend API]
            D[Banco de Dados Relacional]
        end

        subgraph Módulo de IA
            B[Serviço de Recomendação]
            C[Banco de Dados Vetorial]
            E[Serviço de Geração de Embeddings]
        end

        subgraph Terceiros
            F[API da OpenAI]
        end

        A -- 1. Requisição de Recomendações --> B
        B -- 2. Busca por Similaridade --> C
        C -- 3. Retorna IDs Relevantes --> B
        B -- 4. Retorna lista de IDs para o Backend --> A
        A -- 5. Busca Detalhes dos IDs --> D
        D -- 6. Retorna Detalhes --> A
        
        A -- Cadastro de Oportunidade --> E
        E -- Gera Vetor --> F
        F -- Retorna Vetor --> E
        E -- Armazena Vetor --> C
    ```

### Descrição dos Componentes

#### Serviço de Geração de Embeddings
* **Responsabilidade:** Interfacear com a API da OpenAI para converter textos (nossas tags) em vetores numéricos (embeddings). Este serviço é usado tanto na indexação de novas oportunidades quanto na criação de perfis de usuário.

#### Banco de Dados Vetorial (Vector DB)
* **Responsabilidade:** Armazenar os vetores de todas as oportunidades. É altamente otimizado para realizar buscas de similaridade em alta velocidade, sendo o coração da nossa lógica de recomendação.

#### Serviço de Recomendação
* **Responsabilidade:** Orquestrar o processo de recomendação. Ele recebe o ID de um usuário, calcula (ou busca) seu vetor de interesses, consulta o Banco Vetorial para encontrar os IDs das oportunidades mais relevantes e **retorna essa lista de IDs ordenada por relevância** para o serviço que o chamou (o Backend API).

---

## 3. Fluxos de Dados Principais

Existem dois fluxos críticos para o funcionamento do sistema de IA.

!!! success "Fluxo 1: Indexação de uma Nova Oportunidade"
    Este fluxo ocorre quando um administrador cadastra uma nova oportunidade no sistema. (Este fluxo permanece inalterado).

    ```mermaid
    sequenceDiagram
        participant Admin
        participant Backend API
        participant Serviço de Indexação (IA)
        participant Banco Vetorial

        Admin->>Backend API: Cadastra Oportunidade com Tags [IA, Software]
        Backend API->>Serviço de Indexação (IA): Solicita indexação da Oportunidade #123
        Serviço de Indexação (IA)->>Serviço de Indexação (IA): Calcula vetor médio a partir das tags
        Note right of Serviço de Indexação (IA): V_oport = avg(V_IA, V_Softare)
        Serviço de Indexação (IA)->>Banco Vetorial: Armazena (ID: #123, Vetor: V_oport)
        Banco Vetorial-->>Serviço de Indexação (IA): Confirmação
        Serviço de Indexação (IA)-->>Backend API: Oportunidade Indexada
    ```

!!! success "Fluxo 2: Geração de Recomendações para um Usuário (Arquitetura Revisada)"
    Este fluxo foi atualizado para refletir o desacoplamento. O Serviço de IA apenas retorna os IDs, e o Backend API busca os dados completos.

    ```mermaid
    sequenceDiagram
        participant Usuário
        participant Backend API
        participant Serviço de Recomendação (IA)
        participant Banco Vetorial
        participant DB Relacional

        Usuário->>Backend API: GET /api/recommendations
        Backend API->>Serviço de Recomendação (IA): Solicita recomendações para User #ABC
        
        Note over Serviço de Recomendação (IA), Banco Vetorial: Início da Lógica de IA
        Serviço de Recomendação (IA)->>Serviço de Recomendação (IA): Calcula/Busca vetor do User #ABC
        Serviço de Recomendação (IA)->>Banco Vetorial: Busca K vizinhos mais próximos de V_user
        Banco Vetorial-->>Serviço de Recomendação (IA): Retorna IDs e Scores [Op #123, Op #456]
        Serviço de Recomendação (IA)-->>Backend API: Retorna JSON com IDs e Scores
        Note over Serviço de Recomendação (IA), Banco Vetorial: Fim da Lógica de IA
        
        Note over Backend API, DB Relacional: Início do Enriquecimento de Dados
        Backend API->>DB Relacional: Busca detalhes das Oportunidades ONDE ID in [#123, #456]
        DB Relacional-->>Backend API: Retorna detalhes completos
        Backend API->>Backend API: Compila a resposta final para o usuário
        Backend API-->>Usuário: Retorna JSON com as recomendações completas
    ```

---

## 4. Modelo de IA e Lógica de Embedding

A escolha do modelo e a lógica de agregação são decisões críticas que impactam diretamente a qualidade das recomendações.

| Parâmetro | Valor Escolhido | Justificativa |
| :--- | :--- | :--- |
| **Modelo de Embedding** | `text-embedding-3-small` (OpenAI) | Excelente equilíbrio entre custo, performance e alta qualidade semântica para textos em português. |
| **Banco Vetorial** | ChromaDB | Solução open-source robusta que suporta busca vetorial. |
| **Métrica de Distância** | **Similaridade de Cosseno** | Padrão da indústria para medir a similaridade de orientação entre vetores textuais, independentemente de sua magnitude. |

### Lógica de Agregação de Vetores

Para criar um único vetor que represente uma entidade com múltiplas tags (seja uma oportunidade ou um usuário), utilizamos a **média aritmética dos vetores de suas tags**. A fórmula é:

$$\vec{V}_{\text{entidade}} = \frac{1}{N} \sum_{i=1}^{N} \vec{V}_{\text{tag}_i}$$

Onde $N$ é o número de tags associadas à entidade. Este vetor resultante é então normalizado para ter um comprimento unitário antes de ser armazenado ou usado em buscas.

---

## 5. Contrato da API de Recomendação

Com a nova arquitetura, temos dois contratos de API a considerar: a interna (entre Backend e IA) e a externa (entre Backend e Cliente).

### 5.1. API Interna (Backend -> Serviço de IA)

**Endpoint no Serviço de IA:** `POST /recommend`

**Request Body (Exemplo):**
```json
{
  "user_vector": [0.15, 0.75, 0.25, 0.4],
  "limit": 10
}
```
**Success Response (200 OK) - O que o Serviço de IA retorna:**

```json

{
  "recommendations": [
    {
      "opportunity_id": "opp_cdef9012",
      "score": 0.9234
    },
    {
      "opportunity_id": "opp_abcd5678",
      "score": 0.8971
    }
  ]
}
```

> Note que o Backend API é quem calcula ou busca o user_vector e o envia para o serviço de IA.