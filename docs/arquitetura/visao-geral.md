# Arquitetura Geral do Projeto - MuralUnB

> Ocorreram mudanças drásticas na arquitura geral do projeto. Documentação das mudanças em desenvolvimento

## 1. Visão Geral da Arquitetura

A arquitetura do projeto MuralUnB é baseada em um modelo de **componentes desacoplados**, onde cada parte principal do sistema opera de forma independente, comunicando-se através de APIs. Essa abordagem facilita o desenvolvimento paralelo, a manutenção e a escalabilidade.

O sistema é composto por três grandes componentes:

1.  **Frontend:** A aplicação web com a qual o usuário interage diretamente. É responsável por toda a camada de apresentação e experiência do usuário.
2.  **Backend (API):** O servidor central que orquestra a lógica de negócio, gerencia a autenticação de usuários e a persistência de dados no banco de dados.
3.  **Servidor de IA (AI Server):** Um microserviço especializado, responsável por executar os algoritmos de recomendação.

O fluxo de comunicação principal é: o **Frontend** se comunica exclusivamente com o **Backend**. O **Backend**, por sua vez, se comunica com o **Servidor de IA** para obter as recomendações personalizadas.

### 1.1 **Diagrama de Containers**
```mermaid
graph TD
    subgraph unb_ecosystem [Ecossistema Mural UnB]
        direction LR
        
        user("
            <b>Estudante da UnB</b>
            <br />
            [Person]
            <br />
            Navega e descobre oportunidades.
        ")

        subgraph spa [Frontend Web Application]
            direction TB
            
            ui_components("
                <b>UI Components</b>
                <br />
                [React (JSX, CSS)]
                <br />
                Renderiza a interface, captura<br/>as seleções de tags do usuário.
            ")

            state_store("
                <b>Application State Store</b>
                <br />
                [React Context / Zustand]
                <br />
                Gerencia o estado global:<br/>tags selecionadas, resultados da busca.
            ")

            vector_search_engine("
                <b>Vector Search Engine</b>
                <br />
                [JavaScript/TypeScript Module]
                <br />
                <b>O cérebro da busca no cliente.</b><br/>Calcula a similaridade de cosseno.
            ")

            data_service("
                <b>Data Service</b>
                <br />
                [JavaScript/TypeScript Module]
                <br />
                Busca os arquivos JSON<br/>do repositório.
            ")

            %% Fluxo interno da SPA
            ui_components -- "2. Atualiza perfil do usuário" --> state_store
            ui_components -- "3. Dispara a busca" --> vector_search_engine
            vector_search_engine -- "4. Obtém tags do usuário" --> state_store
            vector_search_engine -- "5. Solicita dados" --> data_service
            vector_search_engine -- "7. Calcula similaridade e ranqueia" --> vector_search_engine
            vector_search_engine -- "8. Armazena resultados ordenados" --> state_store
            state_store -- "9. Notifica UI para re-renderizar" --> ui_components
        end

        github_pages("
            <b>GitHub Pages/Repo</b>
            <br />
            [External System]
            <br />
            Armazena e serve os arquivos estáticos<br/>(JSON com embeddings).
        ")
    end

    %% Relações principais
    user -- "1. Seleciona suas tags de interesse" --> ui_components
    data_service -- "6. Fetch dos arquivos JSON [HTTPS]" --> github_pages
```    
![Diagrama de Containers](../assets/images/Diagrama_containers.png)

---

### 1.2 **Diagrama de Componentes**

![Diagrama de Componentes](../assets/images/Diagrama_componentes.png)

### 2. Arquitetura de pastas

A arquitetura de pastas paras os 3 componentes do servidor estão no nosso Figma (HUB) nesse **[FIGMA](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=zPE9vrXMLYmNhGSM-0)**