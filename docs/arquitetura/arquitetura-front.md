# 🎓 Mural UNB

Interface web desenvolvida com React + TypeScript para navegação e pesquisa de oportunidades acadêmicas dentro da Universidade de Brasília.  
O sistema permite que estudantes encontrem projetos, laboratórios, equipes de competição e empresas júniores.

---

## Visão Geral

Funciona como um **portal de consulta**, oferecendo:
- Busca de oportunidades por tags e categorias
- Renderiza todas as telas e componentes visuais definidos no figma
- Interface estilizada com Tailwind + DaisyUI
- Lida com a navegação entre as páginas do site

O objetivo é fornecer um ambiente centralizado e rápido para que estudantes encontrem oportunidades dentro da faculdade.

Para acessar o protótipo do FIGMA, clique neste **[LINK](www.figma.com/design/oYY8vx5O4VbmmSJgbOCPhc/MuralUnB?node-id=0-1&p=f&t=Uy9bHNzfopOWyGos-0&fuid=1443018774773096939)**

---

## Tecnologias Utilizadas

### **Front-end**

- **React 19**  
- **TypeScript**  
- **Vite** como bundler  
- **React Router**

### **Estilização**

- **TailwindCSS**  
- **DaisyUI** (biblioteca de componentes para estilização rápida)

### **Suporte / Arquitetura**

- **ESLint + Prettier** para padronização  
- **Hooks customizados**  
- **Componentização modular**

---

## Estrutura Front-End

A estrutura do front-end segue o padrão modular, organizada da seguinte forma:

```bash
├── src/
│   ├── assets/
│   │   ├── fonts/
│   │   ├── icons/
│   │   ├── images/
|   |   |   └── fotos/
│   │   └── styles/
│   ├── components/
│   │   ├── feed/
│   │   ├── Carosel.tsx
│   │   └── NavBar.tsx
│   ├── data/
│   │   ├── opportunities.ts
│   │   └── tags.ts
│   ├── hooks/
│   │   └── useVectorSearch.ts
│   ├── pages/
│   │   ├── Home/
│   │   ├── Oportunidades/
│   │   └── Sobre/
│   ├── utils/
│   │   ├── types.ts
│   │   └── vectorMatch.ts
│   ├── App.css
│   ├── App.tsx
│   └── main.tsx
└── index.html
```

### **Resumo das pastas**

- **assets/** → imagens, ícones, fontes e estilos globais  
- **components/** → componentes reutilizáveis (ex.: NavBar, carrosséis, cards…)  
- **data/** → dados mockados ou tabelas estáticas (oportunidades, tags)  
- **hooks/** → lógica customizada, como busca vetorial  
- **pages/** → páginas de navegação do site  
- **utils/** → funções auxiliares e definições de tipos  
- **App.tsx** → layout raiz  
- **main.tsx** → ponto de entrada da aplicação
