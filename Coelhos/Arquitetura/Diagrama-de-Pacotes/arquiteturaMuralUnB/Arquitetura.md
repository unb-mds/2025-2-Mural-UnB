# Diagrama de Pacotes da Arquitetura do MuralUnB

Este documento detalha a arquitetura de pacotes (apps Django) do projeto MuralUnB, utilizando a notação UML para diagramas de pacotes.

## 1. Visão Geral da Aplicação

A arquitetura de alto nível do MuralUnB é dividida em duas camadas principais: o Frontend (interface do usuário) e o Backend (lógica de negócio e dados).

**Diagrama de Visão Geral:**

![Visão Geral da Aplicação](caminho/para/visao_geral.png) 

* **Frontend**: Representa a interface do usuário que roda no navegador. É responsável por exibir as informações ao aluno, coletar suas interações (login, filtros, salvos) e exibir o feed de notícias.
* **Backend**: Corresponde ao projeto Django. É o servidor que hospeda a lógica de negócio, gerencia os dados, as autenticações e o sistema de recomendação.

**Relação:**
* **`Frontend` -- `≪access≫` --> `Backend`**: Indica que o `Frontend` faz uso dos serviços expostos pelo `Backend` (via API RESTful, por exemplo) para acessar dados e funcionalidades. O `Frontend` depende do `Backend` para operar, mas não acessa diretamente seus componentes internos.

## 2. Arquitetura Interna do Backend (Django Apps)

O `Backend` é modularizado em apps Django, cada um com responsabilidades específicas. Esta separação visa promover a coesão e o baixo acoplamento, facilitando a manutenção e a evolução do sistema.

**Diagrama de Pacotes do Backend:**

![Arquitetura Interna do Backend](caminho/para/arquitetura_backend.png)

### Descrição dos Pacotes:

* **`Autenticacao_Usuarios`**:
    * **Responsabilidade**: Gerencia o ciclo de vida dos usuários: cadastro, login, logout, gerenciamento de perfil e armazenamento das preferências do aluno (ex: "backend", "robótica").
    * **Dependências**:
        * `Banco_de_Dados`: Para persistir as informações dos usuários e suas preferências.

* **`Conteudo_Feed`**:
    * **Responsabilidade**: Responsável pela gestão dos itens que compõem o feed: notícias da UnB, projetos, vagas de PIBIC, posts de Empresas Juniores. Define a estrutura e o comportamento de um "post" genérico.
    * **Dependências**:
        * `Banco_de_Dados`: Para persistir e recuperar os dados dos posts.
        * `Recomendacoes`: Para obter a ordem personalizada dos posts no feed.
        * `Filtros_Busca`: Para aplicar critérios de filtragem e busca nos posts.

* **`Recomendacoes` (Módulo de IA)**:
    * **Responsabilidade**: O "cérebro" do sistema de personalização. Contém a lógica de Inteligência Artificial/Machine Learning (utilizando conceitos como os estudados em Scikit-Learn) para analisar as preferências do usuário e o conteúdo disponível, gerando uma lista de posts ordenada por relevância para cada usuário.
    * **Dependências**:
        * `Autenticacao_Usuarios`: Para acessar as preferências e o histórico de interações do usuário.
        * `Conteudo_Feed`: Para acessar o pool de posts disponíveis que podem ser recomendados.

* **`Favoritos`**:
    * **Responsabilidade**: Gerencia a funcionalidade de "salvar para ver depois". Registra quais posts foram marcados como favoritos por cada usuário.
    * **Dependências**:
        * `Autenticacao_Usuarios`: Para identificar qual usuário está salvando um item.
        * `Conteudo_Feed`: Para identificar qual post está sendo salvo.

* **`Filtros_Busca`**:
    * **Responsabilidade**: Implementa a lógica para a barra de pesquisa e os filtros temáticos que o usuário pode aplicar ao feed.
    * **Dependências**:
        * `Conteudo_Feed`: Para realizar a filtragem e busca sobre os dados de posts.
        * `Banco_de_Dados`: Para executar as consultas necessárias.

* **`Banco_de_Dados` (Camada de Persistência)**:
    * **Responsabilidade**: Representa a camada de persistência de dados. No contexto Django, isso engloba os `models.py` de todos os apps e a interação com o SGBD subjacente.
    * **Dependências**: É um pacote fundamental; quase todos os outros pacotes do `Backend` dependem dele para armazenar e recuperar dados.

### 3. Por Que Apenas Relações de Dependência no Backend?

A decisão de usar primariamente relações de **dependência** (linha tracejada com seta) entre os pacotes do `Backend` reflete as melhores práticas de modularização em sistemas como o Django:

* **Coerência com UML:** Em diagramas de pacotes, a dependência é o estereótipo mais comum e genérico para indicar que as mudanças em um pacote podem afetar outro.
* **Modularidade e Baixo Acoplamento:** Cada app Django (pacote) deve ter uma responsabilidade bem definida. Quando um app precisa de algo de outro (ex: `Recomendacoes` precisa saber o `User` de `Autenticacao_Usuarios`), ele "depende" desse outro. Isso evita que os apps se tornem excessivamente interligados, permitindo que alterações em um app tenham impacto limitado nos outros.
* **Evitando Outros Estereótipos:**
    * `≪access≫`: Já usado para a relação `Frontend` - `Backend` para indicar o consumo de uma interface pública. Dentro do `Backend`, a granularidade de acesso é melhor representada pela dependência genérica quando se fala de apps.
    * `≪import≫`: Embora `import` seja o que acontece no código Python, `dependência` é o termo UML mais abrangente que engloba essa importação. Poderíamos usar `≪import≫` se quiséssemos ser *extremamente* literais sobre cada `import` statement, mas a dependência já transmite a mesma ideia no nível de pacotes.
    * `≪merge≫`: Não é adequado, pois não estamos "fundindo" o código de um app no outro; eles são mantidos separados e interagem através de dependências bem definidas.

Esta documentação serve como um guia essencial para o desenvolvimento, garantindo que a arquitetura planejada seja compreendida e mantida durante a evolução do projeto.