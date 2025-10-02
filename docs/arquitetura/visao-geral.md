# Arquitetura Geral do Projeto - MuralUnB

## 1. Visão Geral da Arquitetura

A arquitetura do projeto MuralUnB é baseada em um modelo de **componentes desacoplados**, onde cada parte principal do sistema opera de forma independente, comunicando-se através de APIs. Essa abordagem facilita o desenvolvimento paralelo, a manutenção e a escalabilidade.

O sistema é composto por três grandes componentes:

1.  **Frontend:** A aplicação web com a qual o usuário interage diretamente. É responsável por toda a camada de apresentação e experiência do usuário.
2.  **Backend (API):** O servidor central que orquestra a lógica de negócio, gerencia a autenticação de usuários e a persistência de dados no banco de dados.
3.  **Servidor de IA (AI Server):** Um microserviço especializado, responsável por executar os algoritmos de recomendação.

O fluxo de comunicação principal é: o **Frontend** se comunica exclusivamente com o **Backend**. O **Backend**, por sua vez, se comunica com o **Servidor de IA** para obter as recomendações personalizadas.

### **Diagrama de Containers**

![Diagrama de Containers](../assets/images/Diagrama_containers.png)

---

### **Diagrama de Componentes**

![Diagrama de Componentes](../assets/images/Diagrama_componentes.png)
