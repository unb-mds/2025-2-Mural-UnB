# Sprint 9

## O que foi feito

Nesta sprint, o foco foi na integração e consolidação dos dados, bem como na correção de fluxos críticos para a geração e consumo das informações pelo frontend. As tarefas visaram unificar os conjuntos de dados, padronizar identificadores e garantir a correta associação de recursos (imagens e tags).

## Desenvolvimentos Estruturais

**Integração do Frontend com Dados** - Implementação da função FETCH para consumo do arquivo JSON de dados a partir da pasta pública da aplicação.
(Responsável: Luan)

**Funcionalidade de Pesquisa** - Ajustes e finalização da funcionalidade de busca (search) para garantir seu perfeito funcionamento na interface.
(Responsável: Maria)

**Processamento e Associação de Tags** - Associação de tags contextuais às Empresas Juniores e preparação para a geração de embeddings. Correção do diretório (path) dos arquivos PDF para padronizar o output gerado pelos workflows de coleta de dados (tanto de Laboratórios quanto de EJs).
(Responsável: Lucas)

**Consolidação e Estruturação dos Dados** - Unificação dos arquivos de dados de EJs e Laboratórios em um único arquivo JSON. Criação e associação de IDs únicos para cada item (EJs iniciando com '1' e Labs com '2'). Inclusão do arquivo consolidado na estrutura do site.
(Responsável: Tiago)

**Organização de Mídia** - EJs - Associação do ID único de cada Empresa Júnior (definido no JSON) ao nome do arquivo .png da sua respectiva imagem (ex: ID '101' → imagem '101.png').
(Responsável: João)

**Organização de Mídia** - Laboratórios - Conclusão da extração das imagens dos Laboratórios. Associação sistemática das imagens de cada Laboratório ao seu respectivo ID (ex: Logo do Lab ID '201' → '201.png'; imagens adicionais como '201-1.png', '201-2.png').
(Responsável: Matheus)

### Status

**Consolidação dos Dados e Finalização da Integração de Recursos Concluída.**

A Sprint foi finalizada com sucesso, resultando em um conjunto de dados unificado e padronizado, com IDs únicos e a correta vinculação de todas as imagens. Isso estabelece uma base de dados sólida e bem estruturada para o consumo eficiente pelo frontend e pelas funcionalidades de busca e filtro.