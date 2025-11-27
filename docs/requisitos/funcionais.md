# Visão Geral

O propósito dos requisitos funcionais é **definir o que a plataforma Mural UnB deve oferecer** ao usuário em termos de comportamento e funcionalidades observáveis. Abaixo estão os **epics** já pensados e desdobrados em **user stories**, **critérios de aceitação** e exemplos de payloads/endpoint quando aplicável.

> 🔴 P0 (Crítico / MVP) – funcionalidade essencial para o funcionamento básico.  
> 🟠 P1 (Importante) – relevante, mas pode ser entregue após o MVP.  
> 🟢 P2 (Desejável) – incrementos ou funcionalidades complementares.

# Papéis (roles)

- **Aluno**: usuário principal que consome recomendações e favorita oportunidades.

- **Professor** / Orientador: pode solicitar a publicação de oportunidades (opcional, dependendo do MVP).

- **Administrador**: gerencia conteúdo, valida publicações e resolve abusos.

## Epic: Feed & Recomendação

### US-01 — Feed personalizado

**Descrição**: Usuários recebem lista de oportunidades ordenada por relevância.

**Prioridade**: P0 🔴

**Exemplo de response**: { items: [{ id, oportunidade_object, type, score, tags }] }

### US-02 — Busca textual

**Descrição**: Usuários pesquisam por palavras chaves sobre as oportunidades.

**Prioridade**: P0 🔴

## Epic: Oportunidade

### US-03 — Vizualizar detalhes

**Descrição**: Usuários vizualizam os detalhes das oportunidades

**Prioridade**: P0 🔴

### US-4 — Vizualizar tags das oportunidades

**Descrição**: Usuários vizualizam as tags relacionadas as oportunidades

**Prioridade**: P0 🔴

## Epic: Navbar & Navegação

### US-5 — Navbar responsiva

**Descrição**: Navbar fixa com acessos: Home, Oportunidades, Favoritos, Sobre.

**Prioridade**: P0 🔴

## Epic: ETL Dados

### US-6 — ETL das EJs (FCTE)

**Descrição**: Coletar, transformar e carregar o banco de dados com as empresas juniores da FCTE (scopo inicial).

**Prioridade**: P0 🔴

**Exemplo de estrutura**:

```bash
EJs {
  id: UUID PK
  nome: string,
  curso: enum(Software, Eletrônica, Aeroespacial, Automotiva, Energia) FK,
  missao: string FK,
  sobre: string,
  visao: string,
  valores: string,
  servicos: string,

  site?: string,
  instagram?: string,
}
```

### US-7 — ETL das Laboratórios (FCTE)

**Descrição**: Coletar, transformar e carregar o banco de dados com os laboratórios de pesquisa da FCTE (scopo inicial).

**Prioridade**: P0 🔴

**Exemplo de estrutura**:

```bash
EJs {
  id: UUID PK
  nome: string,
  curso: enum(Software, Eletrônica, Aeroespacial, Automotiva, Energia) FK,
  sobre: string,
  coordenador: string,
  email: string,
  tags: FK,
  site?: string,
  instagram?: string,
}
```

### US-8 — ETL das Equipes de Competição (FCTE)

**Descrição**: Coletar, transformar e carregar o banco de dados com as equipes de competição da FCTE (scopo inicial).

**Prioridade**: P2 🟢

**Exemplo de estrutura**:

```bash
EJs {
  id: UUID PK
  nome: string,
  subTitulo: string,
  curso: enum(Software, Eletrônica, Aeroespacial, Automotiva, Energia) FK,
  campus: string FK,
  sobre: string,
  tags: FK,
  site?: string,
  instagram?: string,
}
```

## Epic: Recomendação com IA (Banco Vetorizado)

### US-9 — Microsserviço de Vetorização

**Descrição**: O sistema deve possuir um microsserviço dedicado para armazenar embeddings vetoriais de oportunidades e perfis de usuários.

**Prioridade**: P0 🔴

## Conctags: FK,lusão

Este documento estabelece a **base funcional** da plataforma Mural UnB, detalhando epics, user stories, critérios de aceitação e exemplos técnicos para orientar tanto o desenvolvimento quanto a validação do produto. A priorização (P0, P1, P2) auxilia na definição do MVP, garantindo **foco nas funcionalidades essenciais** para entrega inicial de valor.

## Observação

> 🔖 Para **mais detalhes visuais** sobre fluxos, protótipos e mapeamento de funcionalidades, consulte o [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0), que está sendo utilizado pela equipe como **central de informações**.
