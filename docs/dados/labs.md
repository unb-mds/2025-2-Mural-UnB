# Documentação de Dados — Laboratórios FCTE

Este documento descreve a estrutura dos dados relacionados aos **Laboratórios da FCTE** da Universidade de Brasília (UnB).  

Os dados foram **extraídos do PDF de infraestrutura e laboratórios da UnB e do site de cada uma das engenharias da fcte**, extração feita por: **[Tiago Bittencourt](https://github.com/TiagoSBittencourt)**.  

Esta documentação serve como referência para desenvolvedores, analistas e para o fluxo de ETL, garantindo consistência e padronização na coleta, armazenamento e uso desses dados.

---

## Estrutura da Tabela: Laboratórios (.csv)

| Coluna        | Tipo de Dado | Descrição                                                                                  | Observações                                               |
|---------------|-------------|--------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `Nome`        | string      | Nome oficial do laboratório.                                                               | Ex: "AI Lab"                                              |
| `SubTitulo`   | string      | Breve descrição ou subtítulo do laboratório.                                               | Ex: "Laboratório de Inteligência Artificial"             |
| `Faculdade`   | string      | Faculdade a qual o laboratório está vinculado.                                             | Atualmente todos são da FCTE; escalável para outras.     |
| `Curso`       | string      | Curso ou área de atuação principal do laboratório.                                         | Ex: "Engenharia de Software"                              |
| `Sobre`       | string      | Descrição detalhada do laboratório, missão e objetivos.                                   | Pode conter múltiplas linhas ou parágrafos.              |
| `Coordenador` | string      | Nome do responsável ou coordenador do laboratório.                                         | Ex: "Nilton Correia da Silva"                             |
| `Email`       | string      | E-mail de contato do laboratório ou coordenador.                                           | Deve ser válido e preferencialmente institucional.       |
| `Instagram`   | string      | Conta oficial no Instagram.                                                               | Opcional; prefixo `@`.                                    |
| `Site`        | string      | Website oficial do laboratório.                                                           | Opcional; formato URL (ex: `ailab.unb.br`).             |

---

## Observações

- Embora atualmente todos os laboratórios estejam na FCTE, a tabela foi projetada para permitir expansão futura para outras faculdades.

- Campos opcionais (Instagram, Site) podem ficar vazios se não houver informação disponível.

- Recomenda-se manter consistência nos formatos de e-mail, URLs e nomes para facilitar buscas, filtros e recomendações no sistema.

- Esta documentação deve ser atualizada sempre que novos laboratórios forem adicionados ou houver alterações na estrutura dos dados.