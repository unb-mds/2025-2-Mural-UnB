# Requisitos Não Funcionais

Os requisitos não funcionais do **Mural UnB** descrevem as características de qualidade, restrições técnicas e diretrizes que o sistema deve seguir para garantir desempenho, confiabilidade e uma boa experiência de uso.

---

## 1. Usabilidade
- A interface deve ser responsiva, funcionando em **desktop e mobile**.
- O design deve seguir os protótipos de **alta fidelidade no Figma** para manter consistência visual.
- Deve oferecer **espaço de seleção de Tags**, com no facilidade de busca.
- Textos, labels e mensagens de erro devem ser **claros e acessíveis**.

---

## 2. Desempenho
- Tempo de resposta para recomendação: **≤ 2s** em recomendações pesadas.
- Tempo de carregamento da página inicial: **≤ 3s** em caso geral.

---

## 3. Segurança
- Conexões devem ser feitas exclusivamente em **HTTPS**.
- Logs de acesso e erros críticos devem ser armazenados de forma segura.

---

## 4. Manutenibilidade
- O código deve seguir boas práticas de **PEP8 (Python)** e **ESLint/Prettier (JavaScript/TypeScript)**.
- A documentação deve estar disponível em **GitHub Pages (MkDocs)** e atualizada a cada release.
- Testes unitários devem cobrir ao menos o **código crítico** no MVP (ideal *+90%*).

---

## 5. Confiabilidade
- O sistema deve garantir **99% de uptime** em produção no MVP.
- Em caso de falha, o sistema deve **falhar graciosamente** (ex: fallback do feed).

---

## 6. Escalabilidade
- Arquitetura baseada em **GitHuB Pages**, permitindo hostiamento *gratuito* (carregamento *user-side*).
- Carregamento do banco vetorizado para IA deve ser implementado como **serviço separado** (*ETL*).

---

## Observação  

> 🔖 Para **mais detalhes visuais** e alinhamento de design, consulte o [Figma - Hub do Projeto](https://www.figma.com/board/S9uS0BvdNKOcX2gYhVtMDY/Mural-UnB-MDS?node-id=0-1&p=f&t=3mDHHLQPSOljbISN-0), que centraliza os protótipos e fluxos da equipe.