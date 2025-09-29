# Visão Geral

O propósito dos requisitos funcionais é **definir o que a plataforma Mural UnB deve oferecer** ao usuário em termos de comportamento e funcionalidades observáveis. Abaixo estão os **epics** já pensados e desdobrados em **user stories**, **critérios de aceitação** e exemplos de payloads/endpoint quando aplicável.

> 🔴 P0 (Crítico / MVP) – funcionalidade essencial para o funcionamento básico.  
> 🟠 P1 (Importante) – relevante, mas pode ser entregue após o MVP.  
> 🟢 P2 (Desejável) – incrementos ou funcionalidades complementares.  

# Papéis (roles)

- **Aluno**: usuário principal que consome recomendações e favorita oportunidades.

- **Professor** / Orientador: pode solicitar a publicação de oportunidades (opcional, dependendo do MVP).

- **Administrador**: gerencia conteúdo, valida publicações e resolve abusos.

## Epic: Autenticação

### US-01 — Cadastro / Login

**Descrição**: Usuário pode criar conta com email e senha | pode fazer login.

**Prioridade**: P0 🔴

- Endpoints (ex.):

  - POST /api/auth/register — { name, email, password }

  - POST /api/auth/login — { email, password } -> retorna { access_token, refresh_token, user }

### US-02 — OAuth (Google/UnB SSO)

**Descrição**: Login via Google/SSO da universidade (se possível).

**Prioridade**: P1 🟠

### US-03 — Recuperação de senha

**Descrição**: Usuário solicita recuperação por email.

**Prioridade**: P1 🟠

**Critérios**: Email com link expirável (15–60 min).

## Epic: Perfil & Personalização inicial

### US-04 — Perfil do Usuário

**Descrição**: Usuário pode ver e editar seu perfil (nome, curso, semestre, interesses).

**Prioridade**: P0 🔴

**Campos sugeridos**: name, email (read-only), campus, curso, semestre, interesses.

**Critérios**: Alterações são salvas e refletidas no feed de recomendações.

### US-05 — Onboarding / Personalização do Primeiro Acesso

**Descrição**: Ao criar conta, o usuário responde um fluxo curto para personalizar recomendações.

**Prioridade**: P0 🔴

**Passos**: curso e escolher áreas de interesse (tags).

**Critérios**: A conclusão do onboarding atualiza preferência do usuário e afeta o feed.

## Epic: Feed & Recomendação

### US-06 — Feed personalizado

**Descrição**: Usuários recebem lista de oportunidades ordenada por relevância.

**Prioridade**: P0 🔴

**Exemplo de response**: { items: [{ id, oportunidade_object, type, score, tags }] }

### US-07 — Favoritar / Bookmark (Salvar)

**Descrição**: Usuário pode favoritar oportunidade; ver lista de favoritos no perfil.

**Prioridade**: P1 🟠

**Critério**: Favorito é persistido por usuário; botão alterna estado prédio/filled.

### US-08 — Notificações (push / email)

**Descrição**: Notificar usuário sobre novas oportunidades relevantes.

**Prioridade**: P1 🟠

**Critérios**: Usuário pode ativar/desativar por canal e por tipo de oportunidade.

## Epic: Oportunidade

### US-09 — Listar oportunidades

**Descrição**: Endpoint público para listar oportunidades com filtros.

**Prioridade**: P0 🔴

### US-10 — Pesquisar oportunidade específica

**Descrição**: Capaz de retornar oportunidades associadas a pesquisa

**Prioridade**: P0 🔴

## Epic: Navbar & Navegação

### US-11 — Navbar responsiva

**Descrição**: Navbar fixa com acessos: Home, Oportunidades, Favoritos, Perfil, Sobre, Login/Logout.

**Prioridade**: P0 🔴

**Critério**: Mostra items de acordo com auth state (login vs logout).

## Epic: ETL Dados

### US-12 — ETL das EJs (FCTE)

**Descrição**: Coletar, transformar e carregar o banco de dados com as empresas juniores da FCTE (scopo inicial).

**Prioridade**: P0 🔴

**Exemplo de estrutura**: 

```bash
EJs {
  id: UUID PK
  nome: string,
  curso: enum(Software, Eletrônica, Aeroespacial, Automotiva, Energia) FK,
  campus: string FK,
  sobre: string,
  tags: FK,
  site?: string, 
  instagram?: string,
}
```


### US-13 — ETL das Laboratórios (FCTE)

**Descrição**: Coletar, transformar e carregar o banco de dados com os laboratórios de pesquisa da FCTE (scopo inicial).

**Prioridade**: P0 🔴

**Exemplo de estrutura**: 

```bash
EJs {
  id: UUID PK
  nome: string,
  subTitulo: string,
  curso: enum(Software, Eletrônica, Aeroespacial, Automotiva, Energia) FK,
  campus: string FK,
  sobre: string,
  coordenador: string,
  email: string,
  tags: FK,
  site?: string, 
  instagram?: string,
}
```

### US-14 — ETL das Equipes de Competição (FCTE)

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

### US-15 — Microsserviço de Vetorização

**Descrição**: O sistema deve possuir um microsserviço dedicado para armazenar embeddings vetoriais de oportunidades e perfis de usuários.

**Prioridade**: P0 🔴


## Conclusão

Este documento estabelece a **base funcional** da plataforma Mural UnB, detalhando epics, user stories, critérios de aceitação e exemplos técnicos para orientar tanto o desenvolvimento quanto a validação do produto. A priorização (P0, P1, P2) auxilia na definição do MVP, garantindo **foco nas funcionalidades essenciais** para entrega inicial de valor.

## Observação  

> 🔖 Para **mais detalhes visuais** sobre fluxos, protótipos e mapeamento de funcionalidades, consulte o [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0), que está sendo utilizado pela equipe como **central de informações**.  