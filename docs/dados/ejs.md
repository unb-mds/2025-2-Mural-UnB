# Documentação de Dados — Empresas Juniores (EJs)

Este documento descreve a estrutura dos dados relacionados às **Empresas Juniores (EJs)** da Universidade de Brasília (UnB), incluindo diferentes faculdades/campus.  

Os dados das EJs foram **extraídos do PDF do portfólio das EJs da UnB**, utilizando um **script de leitura e extração de dados desenvolvido por [Tiago Bittencourt](https://github.com/TiagoSBittencourt)**.  


Ele serve como referência para desenvolvedores, analistas e para o fluxo de ETL, garantindo consistência e padronização na coleta, armazenamento e uso desses dados.

![Portifolio EJs](../assets/images/ejs_capa_portifolio.png){ width="300" }

---

## Estrutura da Tabela: Empresas Juniores (.csv)

| Coluna       | Tipo de Dado | Descrição                                                                                  | Observações                                               |
|--------------|-------------|--------------------------------------------------------------------------------------------|-----------------------------------------------------------|
| `Nome`       | string      | Nome oficial da empresa júnior.                                                            | Ex: "CJR"                                                 |
| `Faculdade`  | string      | Faculdade/campus a qual a EJ está vinculada.                                               | Permite expansão para diferentes unidades.               |
| `Cursos`     | string      | Cursos ou áreas atendidas ou de atuação da EJ.                                             | Pode ser múltiplo, separados por vírgula ou lista.       |
| `Sobre`      | string      | Descrição detalhada da EJ, história, objetivos e contexto.                                 | Pode conter múltiplas linhas ou parágrafos.              |
| `Missao`     | string      | Missão declarada da EJ.                                                                    | Opcional; pode ficar vazio se não houver.                |
| `Visao`      | string      | Visão declarada da EJ.                                                                     | Opcional; pode ficar vazio se não houver.                |
| `Valores`    | string      | Valores institucionais ou princípios da EJ.                                                | Opcional; pode ficar vazio se não houver.                |
| `Servicos`   | string      | Lista dos principais serviços oferecidos pela EJ.                                          | Ex: "Sistemas Web, Consultoria, PWA, E-Commerce"        |
| `Site`       | string      | Website oficial da EJ.                                                                     | Opcional; formato URL (ex: `cjr.org.br`).               |
| `Instagram`  | string      | Conta oficial no Instagram da EJ.                                                         | Opcional; prefixo `@`.                                    |

---

## Observações

- A coluna Faculdade permite identificar o campus ou unidade da EJ, tornando possível filtrar por localização.

- Campos opcionais (Missao, Visao, Valores, Site, Instagram) podem ficar vazios se não houver informação disponível.

- Recomenda-se manter consistência nos formatos de texto, URLs e nomes para facilitar buscas, filtros e recomendações no sistema.

- Esta documentação deve ser atualizada sempre que novas EJs forem adicionadas ou houver alterações na estrutura dos dados.
