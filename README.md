# NYC Taxi Analytics (2015 - 2016) 🚕

<img width="1087" height="172" alt="image" src="https://github.com/user-attachments/assets/98fc6e38-c13d-4d6e-a84f-15d12b3364c5" />

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![DuckDB](https://img.shields.io/badge/DuckDB-Database-yellow)
![Parquet](https://img.shields.io/badge/Data-Parquet-green)
![Status](https://img.shields.io/badge/Status-Online-brightgreen)

## 🧠 Abstract

**NYC Taxi Analytics** é o resultado prático de um desafio proposto pela comunidade **Dados Por Todos**. O objetivo? Mergulhar em dados reais das corridas de táxi de Nova York (com foco no biênio 2015-2016) e construir um dashboard interativo capaz de traduzir números brutos em visões de negócio claras.
Os dados brutos utilizados nesta análise foram extraídos do dataset público [NYC Yellow Taxi Trip Data no Kaggle](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data).

## ⚙️ Core Architecture (Gigabytes vs. RAM)

Para contornar o gargalo de memória ao processar milhões de registros, a arquitetura foi otimizada trocando o processamento em memória por consultas eficientes em disco.

```mermaid
graph TD
    A[Dados Brutos CSV] -->|Conversão Parquet| B[Armazenamento Otimizado 16MB]
    B -->|Consultas SQL Diretas| C[DuckDB]
    C -->|Processamento de Dados| D[Pandas & Plotly]
    D -->|Visualização Interativa| E[Streamlit Dashboard]
```

* **Parquet sobre CSV:** A substituição do formato reduziu drasticamente o peso dos dados.
* **O poder do DuckDB:** Consultas diretas nos arquivos otimizados, analisando mais de 500 mil registros de forma rápida sem esgotar a RAM da máquina.

## 🚀 Key Features & Insights

Com o pipeline de dados otimizado, o dashboard revela os padrões ocultos da operação:

* **Corridas de "Tiro Curto":** A grande maioria das viagens dura menos de 20 minutos, com distância média de 4,8 km e tarifa média de $11.84.
  <details>
  <summary>Visualizar Gráfico</summary>
  <img width="1087" height="378" alt="image" src="https://github.com/user-attachments/assets/ce661f70-00a4-41bb-8671-907c73edba34" />
  </details>

* **A Cidade Que Não Dorme:** O pico da demanda ocorre no início da noite (18h-20h), com aumento expressivo no volume nas sextas e sábados devido ao fluxo de lazer noturno.
  <details>
  <summary>Visualizar Gráfico</summary>
  <img width="1088" height="326" alt="image" src="https://github.com/user-attachments/assets/e87f8097-4b3e-4212-8921-b94e436e5a91" />
  </details>

* **Concorrência e Pagamentos:** Mercado equilibrado (47.5% vs 52.5% entre os dois principais fornecedores da cidade). Além disso, a era do cartão de crédito domina quase que totalmente a preferência em relação ao dinheiro físico.
  <details>
  <summary>Visualizar Gráfico</summary>
  <img width="1115" height="330" alt="image" src="https://github.com/user-attachments/assets/01902760-628e-4602-8589-31d9e866faa4" />
  </details>

## 🛠️ Repository Structure

```bash
TAXI NY/
├── dados/                       # Diretório de dados
│   ├── dados_amostra.parquet    # Amostra de dados reduzida
│   └── dados_taxi_processados.parquet # Base consolidada
├── dashboard.py                 # Interface principal do Streamlit
├── main.py                      # Pipeline de processamento de dados
└── requirements.txt             # Dependências (DuckDB, Streamlit, etc)
```

## 💻 Quick Start (Local & Cloud)

**Acesso Rápido na Nuvem:**
👉 **[Acessar o NYC Taxi Dashboard](https://nyc-taxi-dashboard-0.streamlit.app/)**

**Rodando Localmente:**
1. Faça o Clone deste repositório em sua máquina.
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Linux/Mac: source .venv/bin/activate
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Execute o dashboard via Streamlit:
   ```bash
   streamlit run dashboard.py
   ```

## 📄 License

Distribuído sob a Licença MIT.
