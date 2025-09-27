# Estudo de Typescript aplicado a React

Este documento tem o objetivo de fornecer as anotações sobre o uso do TypeScript ou Tsx aplicado á web utilizando React como framework.

## Pre-requisitos

- Git Instalado
- Node.js Instalado (versão LTS)
- Conhecimento básico de Javascript
- Ambiente de Desenvolvimento Integrado (IDE)

## Instalação

- Abra o git bash, ou o terminal, e verifique a sua versão do node.js
`$ node -v`

> Deve retornar a versão instalada mais recente, caso retorne um erro, no Linux rode o comando a baixo. No Windows, baixe o node.js no [site oficial](https://nodejs.org/en/download/)

```bash
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash - 
sudo apt-get install -y nodejs
```

- Com o node.js instalado corretamente, abra o git bash ou o terminal e digite o comando:
`$ npm install -g typescript`

- Se for desejado instalar a linguagem localmente em um projeto, vá para o diretório do seu projeto e instale o Typescript como uma dependência:
`$ npm install --save-dev typescript`

- (Opicional) Inicialize a configuração do Typescript, dessa forma é possível configurar o comportamento do compilador
`$ npx tsc --init`

---

## Configuração do tsconfig.json para React

Para projetos React com TypeScript, o `tsconfig.json` define como o compilador interpreta seu código. Um exemplo básico de configuração:

```json
{
  "compilerOptions": {
    "target": "ES6",                        // Versão do JavaScript de saída
    "lib": ["DOM", "DOM.Iterable", "ESNext"], // Bibliotecas disponíveis
    "allowJs": true,                         // Permitir arquivos .js
    "skipLibCheck": true,                     // Ignorar checagem de bibliotecas externas
    "esModuleInterop": true,                 // Importações compatíveis com CommonJS
    "allowSyntheticDefaultImports": true,    // Importação padrão de módulos
    "strict": true,                           // Habilitar checagem estrita de tipos
    "forceConsistentCasingInFileNames": true,// Evitar conflitos de maiúsculas/minúsculas
    "module": "ESNext",                       // Tipo de módulo
    "moduleResolution": "Node",               // Resolução de módulos
    "resolveJsonModule": true,                // Importar arquivos JSON
    "isolatedModules": true,                  // Necessário para projetos React
    "noEmit": true,                           // Não emitir arquivos .js (usado com Babel/React Scripts)
    "jsx": "react-jsx"                        // Transformação JSX (React 17+)
  },
  "include": ["src"],                         // Pastas incluídas na compilação
  "exclude": ["node_modules"]                 // Pastas excluídas
}
```

---

## Integração com Bibliotecas e APIs Externas

Em aplicações React modernas, é comum precisar integrar bibliotecas externas (como Axios, Lodash, Moment.js) ou consumir APIs externas (REST ou GraphQL).  
O TypeScript ajuda garantindo tipos corretos para dados e funções, evitando erros e facilitando o autocompletar.

### 🔹 Integração com Bibliotecas Externas

#### 1. Instalando bibliotecas

Exemplo com Axios para requisições HTTP:

```bash
npm install axios
npm install --save-dev @types/axios
```

> Muitas bibliotecas já vêm com tipos embutidos. Se não tiver, podemos usar @types/nome-da-biblioteca.

#### 2. Uso com tipagem

```tsx
import axios from "axios";
import React, { useEffect, useState } from "react";

type Usuario = {
  id: number;
  nome: string;
  email: string;
};

function ListaUsuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);

  useEffect(() => {
    axios.get<Usuario[]>("https://jsonplaceholder.typicode.com/users")
      .then(res => setUsuarios(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <ul>
      {usuarios.map(u => (
        <li key={u.id}>{u.nome} - {u.email}</li>
      ))}
    </ul>
  );
}
```

> Tipar a resposta da API (axios.get<Usuario[]>) evita erros de acesso a propriedades inexistentes.

### 🔹 Integração com APIs externas

#### 1. Fetch API com tipagem

```tsx
import React, { useEffect, useState } from "react";

type Post = {
  id: number;
  title: string;
  body: string;
};

function ListaPosts() {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    fetch("https://jsonplaceholder.typicode.com/posts")
      .then(res => res.json())
      .then((data: Post[]) => setPosts(data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      {posts.map(p => (
        <div key={p.id}>
          <h3>{p.title}</h3>
          <p>{p.body}</p>
        </div>
      ))}
    </div>
  );
}
```

> Use try/catch ou .catch para tratar erros e evitar crash da aplicação.

#### 2. Criando um Hook para Requisições Reutilizáveis

```tsx
import { useState, useEffect } from "react";

function useFetch<T>(url: string) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then(res => res.json())
      .then((res: T) => setData(res))
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [url]);

  return { data, loading, error };
}

// Uso do hook
type Produto = { id: number; nome: string; preco: number };

function ListaProdutos() {
  const { data: produtos, loading, error } = useFetch<Produto[]>("https://api.exemplo.com/produtos");

  if (loading) return <p>Carregando...</p>;
  if (error) return <p>Erro: {error}</p>;

  return (
    <ul>
      {produtos?.map(p => (
        <li key={p.id}>{p.nome} - R$ {p.preco}</li>
      ))}
    </ul>
  );
}
```

### 🔹 Boas Práticas

- Sempre tipar a resposta da API com type ou interface.
- Tratar erros usando try/catch ou .catch.
- Criar hooks reutilizáveis para requisições frequentes.
- Usar bibliotecas com tipos embutidos ou @types/....
- Evitar manipular dados da API diretamente sem checagem de tipos.

---

## Tipos básicos e Avançados

### 🔹 Tipos básicos

A seguir, segue os tipos mais comuns, utilizados no dia a dia

#### 1. `String` - Textos

`let nome: string = "Mario";`

#### 2. `Number` - Inteiros e Decimais

`let idade: number = 15;`

#### 3. `Boolean` - Verdadeiro ou Falso

`let ativo: boolean = true;`

#### 4. `Null` e `Unidentified`

```tsx
vazio: null = null;
let indefinido: unidentified = unidentified;
```

#### 5. `Any` - Aceita qualquer tipo

```tsx
let dado: any = "texto"; 
dado = 10; \\válido
```

#### 6. `Unknown` - Similar ao any mas requer checagem de tipo antes de usar

```tsx
let valor: unknown = "texto"; 
if(typeof valor == "string") {
    console.log(valor.toUpperCase());
    }
```

#### 7. `Void` - Usado em funções que não retornam valor

```tsx
function: logar(): void {
    console.log("Executando...")
};
```

#### 8. `Object` - Qualquer objeto não primitivo

```tsx
let pessoa: object = { nome: "Ana", idade: 22 };
```

#### 9. `Never` - Funções que nunca retornam (lançam erro ou loop infinito)

```function erro(msg: string): never {throw new Error(msg);}```

#### 10. `Array`

```tsx
let numeros: number[] = [1, 2, 3];
let nomes: Array<string> = ["Ana", "João"];
```

#### 11. `Tupla` - Array com tamanho e tipos fixos

```let tupla: [string, number] = ["idade", 30];```

### 🔹 Tipos Avançados

#### 1. `Interface` - Contrato para objetos

```tsx
interface Usuario {nome: string; idade: number;}
let u: Usuario = { nome: "Carlos", idade: 30 };
```

#### 2. `Enum` – Conjunto de valores nomeados

```tsx
enum Cores {Vermelho, Verde,Azul}
let cor: Cores = Cores.Verde;
```

#### 3. `Union` (|) – Variável pode ter múltiplos tipos

```tsx
let id: number | string; id = 123; 
id = "ABC123";
```

#### 4. `Intersection` (&) – Combina tipos

```tsx
type Pessoa = { nome: string }; 
type Funcionario = { salario: number }; type Empregado = Pessoa & Funcionario;
let joao: Empregado = { nome: "João", salario: 5000 };
```

#### 5. `Type Aliases` – Apelidos para tipos complexos

```tsx
type ID = string | number;
let userId: ID = 42;
```

#### 6. `Generics` – Tipos genéricos reutilizáveis

```tsx
function identidade<T>(valor: T): T {return valor;}
let numero = identidade<number>(10);
let texto = identidade<string>("Oi");
```

#### 7. `Literal` types – Restringe valores possíveis

```tsx
let direcao: "norte" | "sul" | "leste" | "oeste"; 
direcao = "norte";
```

#### 8. `Optional` e `Nullable`

```tsx
function ola(nome?: string) {
    console.log("Olá " + (nome ?? "visitante"));
}
```

#### 9. `Type assertion` – forçar tipo

```tsx
let valorDesconhecido: unknown = "texto";
let tamanho: number = (valorDesconhecido as string).length;
```

#### 10. `Mapped` type – Criar tipos a partir de outros

```tsx
UsuarioBase = { nome: string; idade: number }; 
type Parcial<T> = { [K in keyof T]?: T[K] };
let u1: Parcial<UsuarioBase> = { nome: "João" };
```

#### 11. `Utility` types – utilitários prontos do

```tsx
interface Pessoa {nome: string; idade: number; email?: string}
let p1: Partial<Pessoa> = { nome: "Lucas" };// todos opcionais
let p2: Required<Pessoa> = { nome: "Ana", idade: 20, email: "a@b.com" }; // todos obrigatórios
let p3: Readonly<Pessoa> = { nome: "Marcos", idade: 30 }; // somente leitura
let p4: Pick<Pessoa, "nome"> = { nome: "Sofia" };  // pega apenas "nome"
let p5: Omit<Pessoa, "email"> = { nome: "Leo", idade: 22 }; // remove "email"
```

---

## Tipagem de props e estados em React com Tsx

No React com TypeScript, tipar props e estados é essencial para garantir que os componentes recebam e manipulem os dados corretos, evitando erros em tempo de compilação.

### 🔹 Tipagem de Props

Props são propriedades que um componente recebe de outro componente pai.  
A tipagem das props define quais dados e tipos são esperados, permitindo autocompletar e checar tipos.

#### 1. Usando `type`

```tsx
type BotaoProps = {
  texto: string;
  onClick: () => void;
};

function Botao({ texto, onClick }: BotaoProps) {
  return <button onClick={onClick}>{texto}</button>;
}

<Botao texto="Clique aqui" onClick={() => alert("Clicou!")} />;
```

#### 2. Usando `interface`

```tsx
interface CardProps {
  titulo: string;
  conteudo: string;
  destacado?: boolean; // opcional
}

function Card({ titulo, conteudo, destacado = false }: CardProps) {
  return (
    <div style={{ border: destacado ? "2px solid red" : "1px solid gray" }}>
      <h3>{titulo}</h3>
      <p>{conteudo}</p>
    </div>
  );
}

<Card titulo="Nota" conteudo="Exemplo de card" />;
```

#### 3. Props com `children`

```tsx
type LayoutProps = {
  children: React.ReactNode;
};

function Layout({ children }: LayoutProps) {
  return <div className="layout">{children}</div>;
}

<Layout>
  <h1>Olá Mundo</h1>
</Layout>;
```

### 🔹 Tipagem de Estado `useState`

O estado é um dado interno do componente que pode mudar ao longo do tempo.
Tipar o estado garante que você atribua valores compatíveis.

#### 1. Estado Simples

```tsx
import { useState } from "react";

function Toggle() {
  // Estado booleano simples
  const [visivel, setVisivel] = useState<boolean>(false);

  return (
    <div>
        <button onClick={() => setVisivel(!visivel)}>
            {visivel ? "Ocultar" : "Mostrar"} Mensagem
        </button>

        {visivel && <p>🎉 Agora você está vendo esta mensagem!</p>}
    </div>
    )
}

export default Toggle;
```

#### 2. Estado com objeto

```tsx
type Usuario = {
  nome: string;
  idade: number;
};

function Perfil() {
  const [usuario, setUsuario] = useState<Usuario | null>(null);

  return (
    <div>
      <button
        onClick={() => setUsuario({ nome: "Ana", idade: 25 })}
      >
        Carregar Usuário
      </button>

      {usuario && <p>{usuario.nome} - {usuario.idade} anos</p>}
    </div>
  );
}
```

#### 3. Estado com Array tipado

```tsx
function Lista() {
  const [itens, setItens] = useState<string[]>([]);

  return (
    <div>
      <button onClick={() => setItens([...itens, "Novo item"])}>
        Adicionar
      </button>
      <ul>
        {itens.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
```

### 🔹 Dicas

- Sempre prefira type ou interface para descrever props e estados complexos.
- Use union types para restringir valores possíveis em props.
- Tipar o useState ajuda a evitar estados undefined inesperados.
- Para children, use React.ReactNode.
- Para eventos, utilize os tipos do React:

`React.ChangeEvent<HTMLInputElement>`
`React.MouseEvent<HTMLButtonElement>`
`React.FormEvent<HTMLFormElement>`

---

## Funções e Generics em TypeScript

### 🔹 Funções

No tsx, as funções funcionam da mesma maneira que no Javascript porém permite a tipagem da entrada e do returno da função.

#### 1. Declaração de função com tipagem

```tsx
function soma(a: number, b: number): number {
  return a + b;
}

let resultado = soma(2, 3); // 5
```

#### 2. Funções anônimas (arrow function)

```tsx
const multiplicar = (x: number, y: number): number => {
  return x * y;
};
```

#### 3. Parâmetros opcionais

```tsx
function saudacao(nome: string, saudacao?: string): string {
  return `${saudacao ?? "Olá"}, ${nome}`;
}

saudacao("Ana"); // "Olá, Ana"
saudacao("Ana", "Bem-vinda"); // "Bem-vinda, Ana"
```

#### 4. Parâmetros com valor padrão

```tsx
function potencia(base: number, expoente: number = 2): number {
  return base ** expoente;
}

potencia(3); // 9
potencia(2, 3); // 8
```

#### 5. Funções que não retornam valor (`void`)

```tsx
function logar(mensagem: string): void {
  console.log(mensagem);
}
```

#### 6. Funções que nunca retornam (`never`)

```tsx
function erro(mensagem: string): never {
  throw new Error(mensagem);
}
```

---

### 🔹 Generics

Generics permitem criar funções, hooks ou componentes que funcionam com vários tipos, mantendo a tipagem forte.

#### 1. Função genérica

```tsx
function identidade<T>(valor: T): T {
  return valor;
}

let numero = identidade<number>(10);
let texto = identidade<string>("Oi");
```

#### 2. Array genérico

```tsx
function primeiroElemento<T>(arr: T[]): T | undefined {
  return arr[0];
}

let primeiro = primeiroElemento([1, 2, 3]); // 1
let palavra = primeiroElemento(["a", "b", "c"]); // "a"
```

#### 3. Restrição de tipo (`extends`)

```tsx
function obterTamanho<T extends { length: number }>(obj: T): number {
  return obj.length;
}

obterTamanho("Hello"); // 5
obterTamanho([1, 2, 3]); // 3
```

#### 4. Generics em interfaces

```tsx
interface RespostaApi<T> {
  dados: T;
  sucesso: boolean;
}

let respostaUsuario: RespostaApi<{ nome: string; idade: number }> = {
  dados: { nome: "Ana", idade: 25 },
  sucesso: true,
};
```

#### 5. Generics em classes

```tsx
class Caixa<T> {
  private valor: T;

  constructor(valor: T) {
    this.valor = valor;
  }

  getValor(): T {
    return this.valor;
  }
}

let caixaNumero = new Caixa<number>(100);
let caixaTexto = new Caixa<string>("Genérico");
```

---

## Hooks com TypeScript

Hooks são funções especiais do React que permitem usar o estado e outros recursos em componentes funcionais sem a necessidade de criar classes específicas. 
O Typescript permite a tipagem de estados, funções e contextos nos hooks.

### 🔹 useState

O `useState` precisa ser tipado quando o TypeScript não consegue inferir automaticamente o tipo.

#### 1. Estado simples (number)

```tsx
import { useState } from "react";

function Contador() {
  const [contador, setContador] = useState<number>(0);

  return (
    <div>
      <p>Valor: {contador}</p>
      <button onClick={() => setContador(contador + 1)}>Incrementar</button>
    </div>
  );
}
```

#### 2. Estado booleano

```tsx
function Toggle() {
  const [visivel, setVisivel] = useState<boolean>(false);

  return (
    <div>
      <button onClick={() => setVisivel(!visivel)}>
        {visivel ? "Ocultar" : "Mostrar"} Mensagem
      </button>
      {visivel && <p>🎉 Agora você está vendo a mensagem!</p>}
    </div>
  );
}
```

#### 3. Estado com objeto

```tsx
type Usuario = {
  nome: string;
  idade: number;
};

function Perfil() {
  const [usuario, setUsuario] = useState<Usuario | null>(null);

  return (
    <div>
      <button onClick={() => setUsuario({ nome: "Ana", idade: 25 })}>
        Carregar Usuário
      </button>
      {usuario && <p>{usuario.nome} - {usuario.idade} anos</p>}
    </div>
  );
}
```

#### 4. Estado com array

```tsx
function Lista() {
  const [itens, setItens] = useState<string[]>([]);

  return (
    <div>
      <button onClick={() => setItens([...itens, "Novo item"])}>
        Adicionar
      </button>
      <ul>
        {itens.map((item, i) => <li key={i}>{item}</li>)}
      </ul>
    </div>
  );
}
```

### 🔹 useEffect

    O `useEffect` executa efeitos colaterais como requisições, timers e subscrições.

```tsx
import { useState, useEffect } from "react";

function Relogio() {
  const [hora, setHora] = useState<Date>(new Date());

  useEffect(() => {
    const timer = setInterval(() => setHora(new Date()), 1000);

    return () => clearInterval(timer); // cleanup
  }, []);

  return <h2>{hora.toLocaleTimeString()}</h2>;
}
```

### 🔹 useContext

O `useContext` permite compartilhar estado global sem precisar passar props manualmente.

```tsx
import { createContext, useContext, useState } from "react";

type Tema = "claro" | "escuro";

const TemaContext = createContext<{
  tema: Tema;
  alternar: () => void;
}>({
  tema: "claro",
  alternar: () => {},
});

function TemaProvider({ children }: { children: React.ReactNode }) {
  const [tema, setTema] = useState<Tema>("claro");

  const alternar = () => setTema(tema === "claro" ? "escuro" : "claro");

  return (
    <TemaContext.Provider value={{ tema, alternar }}>
      {children}
    </TemaContext.Provider>
  );
}

function BotaoTema() {
  const { tema, alternar } = useContext(TemaContext);
  return <button onClick={alternar}>Tema atual: {tema}</button>;
}

function App() {
  return (
    <TemaProvider>
      <BotaoTema />
    </TemaProvider>
  );
}
```

### 🔹 useReducer

O `useReducer` é útil para estados mais complexos ou com múltiplas transições.

```tsx
import { useReducer } from "react";

type Estado = { contador: number };
type Acao = { type: "incrementar" } | { type: "decrementar" };

function reducer(estado: Estado, acao: Acao): Estado {
  switch (acao.type) {
    case "incrementar":
      return { contador: estado.contador + 1 };
    case "decrementar":
      return { contador: estado.contador - 1 };
    default:
      return estado;
  }
}

function ContadorReducer() {
  const [estado, dispatch] = useReducer(reducer, { contador: 0 });

  return (
    <div>
      <p>Contador: {estado.contador}</p>
      <button onClick={() => dispatch({ type: "incrementar" })}>+</button>
      <button onClick={() => dispatch({ type: "decrementar" })}>-</button>
    </div>
  );
}
```

### 🔹 Custom Hooks

Custom hooks permitem extrair lógica reutilizável em funções próprias. A seguir segue um exemplo de hook para armazenar estado no `localStorage`.

```tsx
import { useState, useEffect } from "react";

function useLocalStorage<T>(chave: string, valorInicial: T) {
  const [valor, setValor] = useState<T>(() => {
    const salvo = localStorage.getItem(chave);
    return salvo ? (JSON.parse(salvo) as T) : valorInicial;
  });

  useEffect(() => {
    localStorage.setItem(chave, JSON.stringify(valor));
  }, [chave, valor]);

  return [valor, setValor] as const;
}

function App() {
  const [nome, setNome] = useLocalStorage<string>("nome", "");

  return (
    <div>
      <input value={nome} onChange={(e) => setNome(e.target.value)} />
      <p>Nome salvo: {nome}</p>
    </div>
  );
}
```

---

## Tratamento de Eventos e Tipos de JSX

No React, os eventos são usados para interagir com os elementos da interface, como cliques, mudanças de input, submissão de formulários, etc.  
No TypeScript, podemos tipar esses eventos para garantir maior segurança e evitar erros em tempo de compilação.

### 🔹 Tratamento de Eventos

#### 1. Tipos básicos de eventos

O TypeScript oferece tipos específicos para cada tipo de evento no React, disponíveis no namespace `React`.  
Alguns exemplos:

| Evento                    | Tipo                         |
|----------------------------|-----------------------------|
| Click em botão            | `React.MouseEvent<HTMLButtonElement>` |
| Mudança em input           | `React.ChangeEvent<HTMLInputElement>` |
| Submit de formulário       | `React.FormEvent<HTMLFormElement>` |
| Foco/Blur                  | `React.FocusEvent<HTMLInputElement>` |

---

#### 2. Exemplo: Evento de click

```tsx
import React from "react";

function Botao() {
  const handleClick = (evento: React.MouseEvent<HTMLButtonElement>) => {
    console.log("Botão clicado!", evento);
  };

  return <button onClick={handleClick}>Clique aqui</button>;
}
```

#### 3. Exemplo: Evento de input

```tsx
import React, { useState } from "react";

function Input() {
  const [valor, setValor] = useState("");

  const handleChange = (evento: React.ChangeEvent<HTMLInputElement>) => {
    setValor(evento.target.value);
  };

  return (
    <div>
      <input type="text" value={valor} onChange={handleChange} />
      <p>Valor digitado: {valor}</p>
    </div>
  );
}
```

#### 4. Exemplo: Submit de formulário

```tsx
import React, { useState } from "react";

function Formulario() {
  const [nome, setNome] = useState("");

  const handleSubmit = (evento: React.FormEvent<HTMLFormElement>) => {
    evento.preventDefault(); // evita reload da página
    alert(`Nome enviado: ${nome}`);
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={nome} onChange={e => setNome(e.target.value)} />
      <button type="submit">Enviar</button>
    </form>
  );
}
```

### 🔹 Tipos de JSX

Em TypeScript, podemos tipar elementos JSX e funções que retornam JSX.

#### 1. Função que retorna JSX

```tsx
import React from "react";

function Saudacao(nome: string): JSX.Element {
  return <h1>Olá, {nome}!</h1>;
}
```

> JSX.Element é o tipo padrão para qualquer elemento JSX retornado por uma função.
> Também é possível usar React.ReactNode para aceitar JSX, strings, números ou arrays de elementos.

#### 2. Props com JSX

```tsx
type CardProps = {
  titulo: string;
  conteudo: React.ReactNode; // aceita JSX ou texto
};

function Card({ titulo, conteudo }: CardProps) {
  return (
    <div className="card">
      <h2>{titulo}</h2>
      <div>{conteudo}</div>
    </div>
  );
}

// Uso do componente
function App() {
  return (
    <Card 
      titulo="Meu Card" 
      conteudo={<p>Este é um conteúdo em JSX dentro do card!</p>} 
    />
  );
}
```

<sub>Documentação criada por **Maria Clara** ([@MariaClara-Canuto](https://github.com/MariaClara-Canuto))</sub>