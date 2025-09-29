# Requisitos Não Funcionais

Os requisitos não funcionais do **Mural UnB** descrevem as características de qualidade, restrições técnicas e diretrizes que o sistema deve seguir para garantir desempenho, confiabilidade e uma boa experiência de uso.

---

## 1. Usabilidade
- A interface deve ser responsiva, funcionando em **desktop e mobile**.
- O design deve seguir os protótipos de **alta fidelidade no Figma** para manter consistência visual.
- Deve oferecer **fluxo de onboarding simples**, com no máximo 3–4 passos no primeiro acesso.
- Textos, labels e mensagens de erro devem ser **claros e acessíveis**.

---

## 2. Desempenho
- Tempo de resposta da API: **≤ 500ms** em requisições simples.
- Tempo de carregamento da página inicial: **≤ 2s** em caso geral.

---

## 3. Segurança
- Autenticação via **JWT** (Access e Refresh tokens).
- Senhas devem ser armazenadas usando **hash seguro (bcrypt)**.
- Conexões devem ser feitas exclusivamente em **HTTPS**.
- Logs de acesso e erros críticos devem ser armazenados de forma segura.

---

## 4. Manutenibilidade
- O código deve seguir boas práticas de **PEP8 (Python)** e **ESLint/Prettier (JavaScript/TypeScript)**.
- O projeto deve utilizar **Docker** para padronizar ambientes de desenvolvimento e produção.
- A documentação deve estar disponível em **GitHub Pages (MkDocs)** e atualizada a cada release.
- Testes unitários devem cobrir ao menos o **código crítico** no MVP.

---

## 5. Confiabilidade
- O sistema deve garantir **99% de uptime** em produção no MVP.
- Em caso de falha de microsserviços, o sistema deve **falhar graciosamente** (ex: fallback do feed).
- Backups automáticos da base de dados devem ser realizados **semanlmente**.

---

## 6. Escalabilidade
- Arquitetura baseada em **microsserviços**, permitindo expansão modular.
- Banco vetorizado para IA deve ser implementado como **serviço separado**.

---

## Observação  

> 🔖 Para **mais detalhes visuais** e alinhamento de design, consulte o [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0), que centraliza os protótipos e fluxos da equipe.