
# 🚀 GitHub Pages + Hugo

## 1. O que é GitHub Pages?

O **GitHub Pages** é basicamente um servidor grátis do GitHub.  
Você coloca os arquivos do seu site lá (HTML, CSS, JS) e ele fica online sem você pagar nada.  


  Só vale pra **site estático** (não pode PHP, banco de dados ou Node).  
É perfeito para as documentações que faremos



### Exemplo rápido:
- Criei um repositório no GitHub chamado `pages`
- Coloquei um arquivo `index.html` dentro
- Ativei o **GitHub Pages** nas configurações do repositório
- O site ficou no ar em: https://usuario.github.io/pages/
- Você pode usar um domínio próprio também ex: "www.squad6.com" se quiser

Teste que eu fiz : https://luanludry.github.io/teste-github-pages/

### Observações importantes:
- Só roda em site estático
- O repositório tem que ter no máximo 1 GB (que é o suficiente para a documentação)
- Da para usar diversas ferramentas que geram sites estáticos mas nós vamos usar o **Hugo**

## O que é o Hugo?

O Hugo é um gerador de sites estáticos bem rápido feito em Go. Você escreve um Markdown, escolhe o tema e o site ta pronto.
Tem diversos temas prontos que você pode encontrar aqui [Hugo Themes](https://themes.gohugo.io/)

**Tutorial** https://www.youtube.com/watch?v=rX7VVaEIzPM&ab_channel=%E8%BE%B0%E5%8D%97

## Como criar um site com Hugo + GitHub pages

bash
sudo apt install hugo

Ver se deu certo:
bash
hugo version



### Criar o projeto
bash
hugo new site meu-site
cd meu-site


---

### Escolher um tema
bash
git init
git submodule add https://github.com/theNewDynamic/gohugo-theme-ananke themes/ananke (exemplo de tema)


Configura no `hugo.toml`:
toml
theme = "ananke"


---

### Criar um post
bash
hugo new posts/primeiro-post.md


Vai em `content/posts/primeiro-post.md` e troca `draft = true` pra `draft = false`.

---

### Testar no navegador
bash
hugo server -D


Acesse: [http://localhost:1313](http://localhost:1313)

---

### Gerar o site final
bash
hugo


Ele vai criar a pasta `public/` com os arquivos prontos pra publicar.

---

## 4. Colocando no ar com GitHub Pages

### Jeito rápido (branch `gh-pages`)
1. Cria um repo no GitHub
2. Vai na pasta `public/`
3. Faz o push:
   bash
   git init
   git remote add origin https://github.com/seuusuario/meu-site.git
   git checkout -b gh-pages
   git add .
   git commit -m "deploy"
   git push origin gh-pages --force
   
4. No GitHub → **Settings → Pages** → escolhe o branch `gh-pages`.


## Observações importantes
- Acho que seria bom a gente padronizar os temas, existem alguns temas que eles são mais "completos" e são mais difíceis de ser usados
- A pasta public/ não deve ser comitada no repositorio principal
- o GitHub pages demora uns 3 minutos para ser postado, caso não funcione tenta fazer um novo commit, se isso não funcionar pode falar comigo que eu ajudo :)
- Infelizmente não existe muito conteúdo em português, mas por ser bem simples de ser usado o GPT e outras inteligencias artificiais podem auxiliar bastante

## linkds dos conteúdos estudados

- Site do hugo, existem muita coisa interessantes aqui: https://gohugo.io/documentation/
- Essa playlist tem muito conteúdo para iniciar com o site: https://www.youtube.com/watch?v=0RKpf3rK57I&list=PLbb_NncyMIquNU4pdg6rVW3TuK30Gq9dw&ab_channel=Fireship
- Desse site peguei o passo a passo, inclusive ele é feito usandoHugo: https://www.testingwithmarie.com/posts/20241126-create-a-static-blog-with-hugo/
- Um vídeo do Lempa fazendo o passo a passo de como usar o Hugo com um dos themes mais utilizados: https://youtu.be/MX4yy1dTVYg?si=abOstu-P9trbIxTy

<sub>Documentação criada por **Luan Ludry** ([@luanludry](https://github.com/luanludry))</sub>