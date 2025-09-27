# INTRODUÇÃO A REACT E AXIOS

# 📘 Introdução a React e Axios

## 1. O que é o React?

O **React** é uma biblioteca JavaScript criada pela **Meta** para construção de **interfaces de usuário (UI)**.

Ele é baseado em **componentes reutilizáveis**, o que facilita o desenvolvimento de aplicações modernas e dinâmicas.

### Principais características:

- **Componentização**: cada parte da interface é um componente independente.
- **JSX**: permite escrever HTML dentro do JavaScript.
- **Virtual DOM**: melhora a performance atualizando apenas os elementos que mudaram.
- **Unidirecionalidade**: o fluxo de dados acontece de forma previsível (top-down).

### Exemplo:

```jsx
import React from "react";

function App() {
  return (
    <div>
      <h1>Olá, mundo com React!</h1>
    </div>
  );
}

export default App;

```

## 2. O que é Axios?

O **Axios** é uma biblioteca para fazer **requisições HTTP** (GET, POST, PUT, DELETE, etc.) no navegador e no Node.js.

É muito util em conjunto com React para **buscar e enviar dados a APIs**.

### Principais características:

- Suporte a **Promises**.
- Mais simples que o `fetch`.
- Suporta **interceptadores** (para autenticação, logs, etc.).
- Facilita o **tratamento de erros**.

Para a instalação:

```bash

npm install axios

```

## 3. Vantagem de usar React com Axios

A vantagem de usar **React** junto com **Axios** é que eles se complementam muito bem:

- O **React** organiza a interface em **componentes reutilizáveis** e atualiza a tela de forma eficiente com o **Virtual DOM**.
- O **Axios** resolve a parte de **comunicação com APIs**, permitindo buscar ou enviar dados de forma simples.

Unindo os dois:

- Você consegue **buscar dados de uma API** (por exemplo, lista de produtos, usuários, posts) com Axios.
- Esses dados podem ser **armazenados no estado do React** (`useState`) e exibidos de forma reativa nos componentes.
- Se os dados mudarem (como após um `POST` ou `DELETE`), o React **atualiza automaticamente a interface**, sem você precisar manipular a DOM manualmente.

## 4. Dicas

O Cursor AI, editor de código que o grupo que apresentou em sala o projeto do semestre passado, é muito recomendado para quem está começando a programar React + Axios.

### Vantagens

- **Geração de chamadas prontas**: é possível solicitar, por exemplo, *“faça um hook React que use Axios para buscar usuários de uma API”*, e o Cursor gera a função completa.
- **Tratamento de erros automático**: muitas vezes o desenvolvedor esquece de lidar com exceções (`try/catch`, `.catch`), e o Cursor já sugere essas boas práticas.
- **Integração com o estado do React**: a ferramenta entende o uso de hooks como `useState` e `useEffect`, construindo diretamente a lógica de busca e atualização de dados.
- **Documentação em tempo real**: caso o programador não se recorde da sintaxe do Axios, basta selecionar o trecho para receber uma explicação.
- **Refatoração inteligente**: se houver repetição de chamadas à API, o Cursor sugere a criação de um serviço separado (ex.: `api.js`), melhorando a organização do código.
- **Auxílio em autenticação**: ele ajuda a configurar interceptadores do Axios, como no uso de tokens JWT, sem necessidade de memorizar toda a sintaxe.
    
    Dessa forma, mesmo com tempo limitado, o Cursor pode acelerar o progresso do desenvolvimento e contribuir para que o código final tenha **mais qualidade e boas práticas**.
    
    A instalação é bem simples, é so acessar o site https://cursor.com/, a configuração é bem simples
    

## Referências:

Para as referências de react e axios eu usei a formação Front-end- HTML, css, javaScript, React e + da Udemy

Para o cursor:

- https://www.youtube.com/watch?v=Rgz6mX93C4Y&ab_channel=CorbinBrown
- https://youtu.be/-Olw8ytbSZw?si=6wMEzcXmisAXfS0w
- https://youtu.be/mGNm6GtoWuU?si=tZ3MS-Pwffwyc0WY
- O gpt tem bons prompts para o cursor

<sub>Documentação criada por **Luan Ludry** ([@luanludry](https://github.com/luanludry))</sub>