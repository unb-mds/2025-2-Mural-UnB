## 4. Arquitetura do Servidor de IA (AI Server)

O Servidor de IA é um microserviço Python focado exclusivamente em processar e entregar recomendações.

### Responsabilidades:

- Receber dados do usuário (preferências, histórico) e a lista de oportunidades disponíveis.
- Executar modelos de Machine Learning (ex: filtragem colaborativa, clustering) para gerar uma lista ordenada de posts recomendados.
- Expor um endpoint simples para que o Backend possa solicitar essas recomendações.

### Tecnologias Utilizadas:

- **Linguagem:** Python.
- **Framework da API:** Flask ou FastAPI (sugestão, por serem leves).
- **Bibliotecas de IA:** Scikit-Learn, Pandas, NumPy.

### Comunicação:

O **Backend Django** fará uma requisição HTTP para o **Servidor de IA** (ex: `POST` para `/recommend`) enviando os dados necessários. O Servidor de IA processará e devolverá uma lista de IDs de posts, que o Backend então usará para buscar os dados completos no banco de dados e entregar ao Frontend.
