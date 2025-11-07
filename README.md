# 🏗️ Sistema de Manutenção de Máquinas - Mineração

Pipeline completo de dados para análise e monitoramento de manutenções de equipamentos na indústria de mineração, utilizando Airflow, DBT e PostgreSQL.

## 📊 Visão Geral

Este projeto implementa um Data Warehouse (DW) para centralizar e processar dados de:
- **Máquinas**: Equipamentos de mineração (escavadeiras, caminhões, britadores, etc.)
- **Manutenções**: Histórico de manutenções preventivas e corretivas
- **Operadores**: Dados dos operadores e suas certificações
- **Incidentes**: Registro de falhas e problemas operacionais

### 🎯 Objetivos

- Reduzir tempo de inatividade de máquinas
- Otimizar custos de manutenção
- Prever falhas através de análise de dados
- Monitorar KPIs operacionais em tempo real

## 🏗️ Arquitetura

```
┌─────────────┐
│   Seeds     │  Dados iniciais (CSV)
│   (CSVs)    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│         PostgreSQL Database             │
│  ┌──────────────────────────────────┐   │
│  │     Staging Layer (Views)        │   │
│  │  • stg_maquinas                  │   │
│  │  • stg_manutencoes               │   │
│  │  • stg_operadores                │   │
│  │  • stg_incidentes                │   │
│  └──────────────┬───────────────────┘   │
│                 │                       │
│  ┌──────────────▼───────────────────┐   │
│  │   Intermediate Layer (Tables)    │   │
│  │  • int_dim_maquinas              │   │
│  │  • int_dim_operadores            │   │
│  └──────────────┬───────────────────┘   │
│                 │                       │
│  ┌──────────────▼───────────────────┐   │
│  │      Mart Layer (Tables)         │   │
│  │  • Análises e agregações finais  │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   Airflow   │  Orquestração (Astronomer Cosmos)
│   + DBT     │
└─────────────┘
```

## 🛠️ Tecnologias

- **Orquestração**: Apache Airflow 2.10+ (Astronomer)
- **Transformação**: DBT (Data Build Tool) 1.9+
- **Banco de Dados**: PostgreSQL 16+
- **Containerização**: Docker + Docker Compose
- **Linguagem**: Python 3.12+
- **Framework DBT**: Astronomer Cosmos

## 📁 Estrutura do Projeto

```
project_mineiracao/
├── dags/
│   ├── dag.py                          # DAG principal do Airflow
│   └── dbt/
│       └── dw_mineiracao/              # Projeto DBT
│           ├── dbt_project.yml
│           ├── packages.yml
│           ├── models/
│           │   ├── staging/
│           │   │   ├── stg_maquinas.sql
│           │   │   ├── stg_manutencoes.sql
│           │   │   ├── stg_operadores.sql
│           │   │   └── stg_incidentes.sql
│           │   ├── intermediate/
│           │   │   └── dim/
│           │   │       ├── int_dim_maquinas.sql
│           │   │       └── int_dim_operadores.sql
│           │   └── mart/
│           │       └── # Análises finais
│           └── seeds/
│               ├── dados_maquinas.csv
│               ├── dados_manutencoes.csv
│               ├── dados_operadores.csv
│               └── dados_incidentes.csv
├── include/                            # Arquivos auxiliares
├── plugins/                            # Plugins do Airflow
├── Dockerfile                          # Configuração do container
├── docker-compose.yml                  # Orquestração Docker
├── requirements.txt                    # Dependências Python
├── .dockerignore                       # Arquivos ignorados no build
├── .gitignore                          # Arquivos ignorados no Git
└── README.md                           # Este arquivo
```

## 🚀 Como Executar

### Pré-requisitos

- Docker Desktop instalado
- Astronomer CLI instalado ([guia](https://www.astronomer.io/docs/astro/cli/install-cli))
- Git
- 8GB RAM disponível

### 1. Clonar o Repositório

```bash
git clone https://github.com/NicolasNagel/project_mineiracao.git
cd project_mineiracao
```

### 2. Iniciar o Ambiente

```bash
# Iniciar todos os serviços (Airflow + PostgreSQL)
astro dev start

# Aguardar ~2-3 minutos para inicialização completa
```

### 3. Acessar o Airflow

```
URL: http://localhost:8080
Username: admin
Password: admin
```

### 4. Configurar Conexão com Banco

No Airflow UI:
1. Vá em **Admin** → **Connections**
2. Clique em **+** (Add)
3. Preencha:
   - **Connection Id**: `docker_compose_db`
   - **Connection Type**: `Postgres`
   - **Host**: `postgres`
   - **Schema**: `dbt_db`
   - **Login**: `dbtuser`
   - **Password**: `dbtpassword`
   - **Port**: `5432`
4. Clique em **Save**

### 5. Executar a DAG

1. Na UI do Airflow, procure por `dag_mineiracao_dw`
2. Ative a DAG (toggle no canto esquerdo)
3. Clique em **Play** (▶️) para executar manualmente

## 📊 Dados

### Volumes de Dados

- **50 máquinas** de diferentes tipos (escavadeiras, caminhões, britadores)
- **300 registros de manutenção** (preventivas e corretivas)
- **30 operadores** com certificações
- **150 incidentes** registrados

### Tipos de Máquinas

- Escavadeira Hidráulica
- Caminhão Fora de Estrada
- Britador (Mandíbulas/Cônico)
- Perfuratriz Rotativa
- Pá Carregadeira
- Trator de Esteiras
- Correia Transportadora
- E mais...

### Fabricantes

Caterpillar, Komatsu, Liebherr, Volvo, Sandvik, Atlas Copco, entre outros.

## 🔍 KPIs Monitorados

- ⏱️ **Tempo de Inatividade**: Horas totais de parada por máquina
- 💰 **Custo de Manutenção**: Gastos totais e por tipo de manutenção
- 📈 **Incidentes por Máquina**: Frequência de falhas
- 🔧 **Manutenção Preventiva vs Corretiva**: Proporção e efetividade
- 👷 **Performance dos Operadores**: Incidentes por operador
- 🎯 **Taxa de Disponibilidade**: % do tempo operacional

## 🧪 Testes

O projeto inclui testes de qualidade de dados via DBT:

```bash
# Rodar testes
astro dev bash -s scheduler
dbt test --project-dir /usr/local/airflow/dags/dbt/dw_mineiracao
```

Testes implementados:
- ✅ Validação de chaves únicas
- ✅ Validação de NOT NULL
- ✅ Integridade referencial (Foreign Keys)

## 📦 Dependências Principais

```txt
apache-airflow-providers-postgres>=5.0.0
astronomer-cosmos[dbt-postgres]>=1.4.0
dbt-core==1.9.0
dbt-postgres==1.9.0
```

## 🐛 Troubleshooting

### Erro: Connection não encontrada

```bash
# Verificar se a conexão existe
astro dev bash -s scheduler
airflow connections list | grep docker_compose_db
```

### Erro: DBT não encontrado

```bash
# Verificar instalação do DBT
astro dev bash -s scheduler
/usr/local/airflow/dbt_venv/bin/dbt --version
```

### Limpar ambiente e reconstruir

```bash
astro dev stop
docker system prune -af --volumes
astro dev start --no-cache
```

## 👨‍💻 Autor

**Nicolas Nagel**

- GitHub: [@NicolasNagel](https://github.com/NicolasNagel)
- LinkedIn: [Seu LinkedIn]
- Email: seu-email@example.com
