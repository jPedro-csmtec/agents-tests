# OBD Shaun Agents

Este projeto é uma plataforma modular para análise, extração, sumarização e planejamento clínico de informações médicas, utilizando agentes inteligentes para processar laudos, exames, diagnósticos e documentos hospitalares.

## Estrutura do Projeto

- **gateway/**  
  Camada de entrada da aplicação, responsável por receber requisições, orquestrar chamadas aos agentes e expor endpoints REST.  
  - `app/`: Código principal da API, middlewares, roteadores e schemas de integração.
  - `schemas/`: Define os contratos de entrada e saída das funções (ex: extração, resumo, CID, planejamento).

- **configurations/**  
  Configurações globais do projeto, como variáveis de ambiente e parâmetros de execução.  
  - `config.py`: Centraliza configurações utilizadas pelos módulos.

- **libs/**  
  Bibliotecas de utilidades e tratamento de erros.  
  - `errors/`: Modelos, exceções e handlers para padronizar respostas de erro.
  - `utils/`: Funções auxiliares e geração de dados fictícios para testes.

- **logs/**  
  Gerenciamento e armazenamento de logs de execução e auditoria.  
  - `logger.py`: Implementação do sistema de logging.

- **services/**  
  Módulos de agentes inteligentes, cada um especializado em uma tarefa clínica:
  - **agent_extraction/**: Extração de informações estruturadas de documentos (PDF, imagens, etc).
  - **agent_summary/**: Geração de sumários clínicos detalhados e estruturados a partir de textos médicos.
  - **agent_resume/**: Resumos objetivos de laudos e exames, destacando objetivo, metodologia, resultados e conclusões.
  - **agent_cid_analysis/**: Identificação e detalhamento de códigos CID-10 presentes nos textos analisados.
  - **agent_diagnostic/**: Avaliação diagnóstica baseada em sintomas, exames e histórico, sugerindo hipóteses e planos de investigação.
  - **agent_planner/**: Planejamento de intervenções, acompanhamento e encaminhamentos clínicos.
  - **agent_treatment/**: Propostas de estratégias terapêuticas baseadas em evidências e informações extraídas.
  - **agent_rag/**: Recuperação de informações clínicas relevantes a partir de bases de conhecimento (RAG).
  - **agent_reports/**: Geração e manipulação de relatórios médicos.

- **scripts/**  
  Scripts utilitários para build, publicação, execução em Docker e integração contínua.

## Principais Funcionalidades

- **Extração de Dados**: Processa documentos médicos e retorna informações estruturadas.
- **Sumarização Clínica**: Gera sumários e resumos detalhados de prontuários, exames e laudos.
- **Análise CID-10**: Identifica, detalha e justifica códigos CID-10 presentes nos textos.
- **Diagnóstico Automatizado**: Sugere hipóteses diagnósticas e planos de investigação.
- **Planejamento e Tratamento**: Elabora planos de cuidado e estratégias terapêuticas.
- **RAG (Retrieval-Augmented Generation)**: Busca informações clínicas em bases externas para enriquecer respostas.

## Como Executar

1. Configure as variáveis de ambiente em `.env`.
2. Instale as dependências com `pip install -r requirements.txt`.
3. Execute o gateway para expor a API REST `unicorn app.main --reload`.
4. Utilize os endpoints para enviar documentos, textos ou dados clínicos e receber análises dos agentes.

## Observações

- Cada agente é independente e pode ser chamado separadamente via API.
- O projeto é extensível para novos agentes e integrações.
- Consulte a documentação dos endpoints na pasta `docs` ou via Swagger.

---

Para detalhes de cada módulo, consulte os arquivos de cada serviço em `services` e os schemas