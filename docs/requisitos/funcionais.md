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

**Descrição**: Usuários vizualizam os detalhes das oportunidades, como: Instagram, site, etc...

**Prioridade**: P0 🔴

### US-4 — Vizualizar tags das oportunidades

**Descrição**: Usuários vizualizam as tags relacionadas as oportunidades

**Prioridade**: P1 🟠

## Epic: Navbar & Navegação

### US-5 — Navbar responsiva

**Descrição**: Navbar fixa com acessos: Home, Oportunidades, Favoritos, Sobre.

**Prioridade**: P1 🟠

## Epic: ETL Dados

## Epic: Home

### US-6 — Página inicial

**Descrição**: Página inicial possuindo informações sobre o Mural-UnB que apresenta o projeto e as funcionalidades do site

**Prioridade**: P1 🟠

### US-7 — Sobre

**Descrição**: Página de sobre, que apresenta os integrantes do projeto e mostra a participação de cada um nele.

**Prioridade**: P2 🟢

## Epic: ETL Dados

### US-8 — ETL das EJs (FCTE)

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

### US-9 — ETL das Laboratórios (FCTE)

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

### US-10 — ETL das Equipes de Competição (FCTE)

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

### US-11 — Captação e Relacionamento das Tags

**Descrição**: O sistema deve ser capaz de gerar automaticamente os embeddings para a lista de tags em `tags.json` e relacionar as Oportunidades.

**Prioridade**: P0 🔴

## Epic: Recomendação com IA (Banco Vetorizado)

### US-12 — Similaridade no frontend

**Descrição**: O sistema deve fazer uma busca por similaridade para entregar uma recomendação para o usuario a partir das tags das oportunidades.

**Prioridade**: P0 🔴

## Observação

> 🔖 Para **mais detalhes visuais** sobre fluxos, protótipos e mapeamento de funcionalidades, consulte o [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0), que está sendo utilizado pela equipe como **central de informações**.
