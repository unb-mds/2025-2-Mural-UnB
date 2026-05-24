<a id="readme-top"></a>

<!-- ESCUDOS DO PROJETO -->
<p align="center">
  <a href="https://github.com/unb-mds/Mural-UnB/graphs/contributors">
    <img src="https://img.shields.io/github/contributors/unb-mds/Mural-UnB.svg?style=for-the-badge" alt="Contribuidores" />
  </a>
  <a href="https://github.com/unb-mds/Mural-UnB/network/members">
    <img src="https://img.shields.io/github/forks/unb-mds/Mural-UnB.svg?style=for-the-badge" alt="Forks" />
  </a>
  <a href="https://github.com/unb-mds/Mural-UnB/stargazers">
    <img src="https://img.shields.io/github/stars/unb-mds/Mural-UnB.svg?style=for-the-badge" alt="Stars" />
  </a>
  <a href="https://github.com/unb-mds/Mural-UnB/issues">
    <img src="https://img.shields.io/github/issues/unb-mds/Mural-UnB.svg?style=for-the-badge" alt="Issues" />
  </a>
  <a href="https://github.com/unb-mds/Mural-UnB/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/unb-mds/Mural-UnB.svg?style=for-the-badge" alt="Licença" />
  </a>
  <a href="mailto:unb.mural@gmail.com">
    <img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail" />
  </a>
</p>

<p align="center">
  <a href="https://muralunb.com.br">
    <img src="https://img.shields.io/badge/GH%20Pages-Site-blue?style=for-the-badge&logo=github" alt="Site"/>
  </a>
  <a href="https://tiagosbittencourt.github.io/Mural-UnB/">
    <img src="https://img.shields.io/badge/GH%20Pages-Docs-blue?style=for-the-badge&logo=github" alt="Docs"/>
  </a>
  <a href="https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0">
    <img src="https://img.shields.io/badge/Figma-Hub-purple?style=for-the-badge&logo=figma" alt="Figma"/>
  </a>
</p>

<h1 align="center">
  <br>
  <a href="https://muralunb.com.br/"><img src="./readme/main_logo.png" alt="Mural UnB" width="300"></a>
</h1>

<p align="center"> 
  🌎 Languages: <a href="./readme/README.en.md">English</a> | <a href="./README.md">Português</a>
</p>

<h3 align="center">Plataforma de mural digital da Universidade de Brasília (UnB)</h3>

<!--
<p align="center">
  <a>
    <img src="https://badge.fury.io/js/mural-unb.svg" alt="Versão npm">
  </a>
  <a>
    <img src="https://badge.fury.io/py/pip.svg" alt="Versão PyPi">
  </a>
  <a>
    <img src="https://img.shields.io/badge/docker%20engine-28.4-blue" alt="Docker">
  </a>
</p>
-->

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#principais-funcionalidades">Funcionalidades</a> •
  <a href="#como-funcionar">Como Funciona</a> •
  <a href="#🔗-links">Links</a> •
  <a href="#🙋‍♂️-equipe">Equipe</a> •
  <a href="#🧾-licença">Licença</a> •
  <a href="#🤝-contribuição">Contribuição</a> •
  <a href="#📜-código-de-conduta">Código de Conduta</a>
</p>

## Sobre

O **Mural UnB** é uma plataforma digital projetada para centralizar e recomendar oportunidades acadêmicas e profissionais dentro da Universidade de Brasília (UnB).

O objetivo é criar uma **experiência personalizada**, onde os estudantes possam facilmente descobrir oportunidades alinhadas aos seus interesses e histórico acadêmico.  
Ao analisar o perfil do usuário, a plataforma recomenda as opções mais relevantes e envia notificações sobre novas vagas.

Inclui oportunidades como:

- **Empresas juniores**
- **Laboratórios de pesquisa**
- **Equipes de Competição**

Em resumo, o Mural UnB funciona como um **mural virtual**, que vai além de apenas listar oportunidades — ele **ajuda os estudantes a se conectarem com as oportunidades certas, no momento certo**.

## Como Funciona

1. **Listagem de Oportunidades (Feed)** → O usuário tem acesso a uma página com grande parte das oportunidades na UnB.
2. **Análise de perfil** → O sistema identifica interesses e habilidades que o usuário quer ser recomendado por meio de Tags.
3. **Recomendações personalizadas** → O estudante recebe oportunidades alinhadas ao seu perfil (tags).

## 🔗 Links

- [Demo (Site)](https://muralunb.com.br/)
- [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0)
- [Repositório GitHub](https://github.com/unb-mds/Mural-UnB)

## 📚 Documentação Técnica

Para desenvolvedores e contribuidores, criamos guias detalhados sobre o funcionamento interno do projeto:

- 🐍 **[Manual dos Scripts (Backend)](scripts/README.md):** Aprenda a rodar os crawlers, pipelines de IA e testes automatizados.
- 💾 **[Estrutura de Dados](data/README.md):** Entenda o esquema dos arquivos CSV, JSON e a organização das imagens.
- 🔒 **[Política de Segurança](SECURITY.md):** Como reportar vulnerabilidades.

### 🛠️ Instalação Rápida para Desenvolvedores

```bash
# 1. Clone o repositório
git clone https://github.com/unb-mds/2025-2-Mural-UnB.git

# 2. Configuração do Backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 3. Configuração do Frontend
cd site
npm install
npm run dev
```

## 🙋‍♂️ Equipe

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/TiagoSBittencourt">
        <img src="https://github.com/TiagoSBittencourt.png" width="100px;" alt="Tiago Bittencourt"/>
        <br /><sub><b>Tiago Bittencourt</b></sub>
      </a>
      <br /><span>SM • ML & Agent Developer</span>
    </td>
    <td align="center">
      <a href="https://github.com/Karmantinedev">
        <img src="https://github.com/Karmantinedev.png" width="100px;" alt="João Souza"/>
        <br /><sub><b>João Gonzaga</b></sub>
      </a>
      <br /><span>PO • Backend Developer</span>
    </td>
    <td align="center">
      <a href="https://github.com/luanludry">
        <img src="https://github.com/luanludry.png" width="100px;" alt="Luan Ludry"/>
        <br /><sub><b>Luan Ludry</b></sub>
      </a>
      <br /><span>Frontend Developer</span>
    </td>
    <td align="center">
      <a href="https://github.com/Lucasft16">
        <img src="https://github.com/Lucasft16.png" width="100px;" alt="Lucas Fujimoto"/>
        <br /><sub><b>Lucas Fujimoto</b></sub>
      </a>
      <br /><span>Backend Developer</span>
    </td>
    <td align="center">
      <a href="https://github.com/MariaClara-Canuto">
        <img src="https://github.com/MariaClara-Canuto.png" width="100px;" alt="Maria Canuto"/>
        <br /><sub><b>Maria Canuto</b></sub>
      </a>
      <br /><span>Frontend Developer</span>
    </td>
    <td align="center">
      <a href="https://github.com/apptrx">
        <img src="https://github.com/apptrx.png" width="100px;" alt="Matheus Saraiva"/>
        <br /><sub><b>Matheus Saraiva</b></sub>
      </a>
      <br /><span>Backend Developer</span>
    </td>
  </tr>
</table>

## 🧾 Licença

[MIT](./LICENSE)

## 🤝 Contribuição

Contribuições da comunidade são muito bem-vindas! 🎉  
Veja nosso [CONTRIBUTING.md](./.github/CONTRIBUTING.md) para saber como começar.

## 📜 Código de Conduta

Este projeto segue um **Código de Conduta** para garantir um ambiente acolhedor.  
Assim que disponível, você pode acessá-lo aqui: [CODE_OF_CONDUCT.md](./.github/CODE_OF_CONDUCT.md).

---

> Site [muralunb.com.br](https://muralunb.com.br/) &nbsp;&middot;&nbsp;
> GitHub [Mural-UnB](https://github.com/unb-mds/Mural-UnB) &nbsp;&middot;&nbsp;
> Instagram [@**\_\_**]() &nbsp;&middot;&nbsp;
> email [unb.mural@gmail.com]()
