# Git e GitHub [![starline](https://starlines.qoo.monster/assets/qoomon/5dfcdf8eec66a051ecd85625518cfd13@gist)](https://github.com/qoomon/starline)

Aprenda o essencial para versionar projetos com **Git** e colaborar usando **GitHub**.  

---

## 📌 Resumão rápido
- **Git** → versionamento local/distribuído (salva versões do código).  
- **GitHub** → backup online + colaboração em equipe.  
- **Push** → envia código pro GitHub.  
- **Pull** → baixa atualizações do GitHub.  
- **Branching** → ramificações para trabalhar em paralelo.  
- **Merging** → junta branches (ex.: `feature` → `main`).  
- **Pull Request (PR)** → revisão antes de juntar.  
- **Conflitos** → quando duas branches mexem no mesmo trecho de jeitos diferentes.  

---

## Git

### Conceitos importantes
- **Changed Area**: alterações locais ainda não staged.  
- **Staged Area**: arquivos prontos para o próximo commit.  
- **HEAD**: aponta para a versão/branch atual.  
- **.gitignore**: arquivos/pastas que o Git deve ignorar (ex.: `.env`, `node_modules`).  

---

### Comandos básicos
<pre>
git init                  # inicia repositório
git status                # mostra status dos arquivos
git add .                 # adiciona todos
git add &lt;arquivo&gt;          # adiciona específico
git commit -m "mensagem"  # cria commit
git log --all --graph     # histórico visual
</pre>

---

### Ajustando versões
<pre>
git commit --amend -m "nova mensagem"   # altera último commit
git reset &lt;arquivo&gt;                     # tira da staged area
git checkout &lt;id-do-commit&gt;             # vai para commit específico
</pre>

> [!NOTE]  
> `git checkout <id>` leva a *detached HEAD* — cuidado pra não perder commits novos; crie uma branch antes.  

---

### Personalizações
<pre>
git config --global alias.s "status"   # cria atalho (git s)
git config --global user.name "Seu Nome"
git config --global user.email "vc@ex.com"
rm -rf .git                            # apaga todo o repo local
</pre>

> [!TIP]  
> Use `git diff` e `git diff --staged` para revisar antes de commitar.  

---

## GitHub

### O que é
Plataforma online para hospedar repositórios Git, trabalhar em equipe, abrir **issues** e **pull requests**.  

---

### Conectar local ↔ remoto
<pre>
git remote add origin &lt;url&gt;   # conecta repo local ao remoto
git remote remove origin      # remove conexão
</pre>

> [!NOTE]  
> Para autenticar `git push`, use **Personal Access Token** (em vez de senha).  

---

### Fluxo básico de uso
<pre>
# primeira vez
git add .
git commit -m "mensagem"
git push --set-upstream origin main

# depois
git push

# atualizar local
git fetch
git pull origin main
</pre>

---

### Clonar repositório
<pre>
git clone &lt;url&gt;              # clona repo
git clone &lt;url&gt; &lt;pasta&gt;      # clona em pasta personalizada
</pre>

---

## Branching

### Por que usar
Trabalhar em features/correções sem atrapalhar a `main`.  

### Comandos
<pre>
git branch &lt;nome&gt;       # cria branch
git checkout &lt;nome&gt;     # troca de branch
git switch -c &lt;nome&gt;    # cria e troca (atalho moderno)
</pre>

---

## Merging

### Conceito
Juntar a branch de feature na branch principal.  

<pre>
git checkout main
git pull origin main
git merge minha-feature
</pre>

---

### Conflitos
Ocorrem quando duas branches alteram o mesmo trecho.  

- Git marca com `<<<<<<<`, `=======`, `>>>>>>>`.  
- Resolve manualmente no editor, depois:  
<pre>
git add .
git commit
git push origin minha-feature
</pre>

---

## Feature Branch Workflow

1. **Clonar repositório**  
   `git clone <url>`  

2. **Criar branch**  
   `git checkout -b feature/minha-coisa`  

3. **Trabalhar e commitar**  
   `git add . && git commit -m "feat: implementa X"`  

4. **Subir branch**  
   `git push origin feature/minha-coisa`  

5. **Abrir Pull Request no GitHub**  
   - Base: `main` ← Compare: `feature/minha-coisa`  
   - Escreve descrição clara, linka issues, explica testes.  

6. **Revisões**  
   - Corrigir o que pedirem, dar push novamente.  

7. **Merge**  
   - Após aprovação, escolher método de merge (Merge commit / Squash / Rebase).  
   - Deletar branch remota se não for mais necessária.  

---

## Observações finais
- Use `.gitignore` para não versionar arquivos sensíveis.  
- Proteja a `main`: só merge via Pull Request.  
- Commits descritivos (evite “update” ou “teste”).  
- Use `git reflog` para recuperar commits perdidos.  
- Tokens/SSH para autenticar pushes.  

---

<sub>Documentação criada por **Matheus Saraiva** ([@apptrx](https://github.com/apptrx))</sub>