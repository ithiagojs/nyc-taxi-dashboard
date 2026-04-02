# 🚕 NYC Taxi Analytics (2015 - 2016)

<img width="1087" height="172" alt="image" src="https://github.com/user-attachments/assets/98fc6e38-c13d-4d6e-a84f-15d12b3364c5" />

Este projeto é o resultado prático de um desafio proposto pela comunidade **Dados Por Todos**. O objetivo? Mergulhar em dados reais das corridas de táxi de Nova York (com foco no biênio 2015-2016) e construir um dashboard interativo capaz de traduzir números brutos em visões de negócio claras.

**Fonte dos Dados:** Os dados brutos utilizados nesta análise foram extraídos do dataset público [NYC Yellow Taxi Trip Data no Kaggle](https://www.kaggle.com/datasets/elemento/nyc-yellow-taxi-trip-data).

### Uma espiada nos dados (pós-processamento)

Para você entender a estrutura do que estamos analisando, aqui está uma amostra dos registros já limpos e otimizados pelo Python, prontos para a visualização:

<img width="1075" height="326" alt="image" src="https://github.com/user-attachments/assets/ff73a022-4d04-4b8c-bf9c-ff3530c4911c" />

### O Desafio Técnico (Gigabytes vs. RAM)

No começo, o plano era simples: baixar os arquivos CSV e fazer a análise usando o bom e velho Pandas. Acontece que a realidade bateu na porta: o volume de informações (milhões de linhas) simplesmente esgotava a memória RAM do meu computador.

Para contornar esse gargalo e conseguir processar mais de **500 mil registros** de forma rápida, precisei mudar a rota da minha abordagem:

1. **Tchau pro CSV, Oi pro Parquet:** Substituir o formato dos arquivos reduziu drasticamente o peso dos dados, comprimindo-os para cerca de incríveis 16MB.
2. **O poder do DuckDB:** Passei a fazer as consultas (queries) direto no arquivo otimizado. Assim, consegui analisar todo o volume de dados sem precisar carregar tudo na memória da máquina de uma vez. O resultado foi um processamento rápido e sem travamentos.

### O que os dados contaram? 

Com o pipeline de dados otimizado, o dashboard começou a revelar os padrões ocultos da operação de táxis em NY.

#### 1. Corridas de "tiro curto"

As primeiras visualizações nos ajudam a entender o perfil físico da operação. Os gráficos mostram que a operação é de altíssimo giro:

<img width="1087" height="378" alt="image" src="https://github.com/user-attachments/assets/ce661f70-00a4-41bb-8671-907c73edba34" />

* **Alto giro:** A grande maioria das viagens dura menos de 20 minutos.
* **Ticket Baixo:** A distância média é de apenas 4,8 km, o que resulta em uma tarifa média baixa de $11.84, como pode ser confirmado na alta densidade de pontos no início do gráfico de dispersão.

#### 2. A cidade que não dorme (mas sai à noite)

Analisando o comportamento temporal, fica claro que o pico da demanda não acontece nas manhãs comerciais, mas sim no início da noite e nos finais de semana:

<img width="1088" height="326" alt="image" src="https://github.com/user-attachments/assets/e87f8097-4b3e-4212-8921-b94e436e5a91" />

* **Horário Nobre:** O maior volume de corridas acontece entre 18h e 20h.
* **Efeito Fim de Semana:** Há um aumento expressivo no volume nas sextas-feiras e sábados, mostrando que o fluxo de lazer noturno impacta a demanda de forma mais agressiva do que o horário de trabalho.

#### 3. Concorrência Equilibrada e o Fim do Dinheiro Físico

Por fim, analisamos a operação de mercado e como o dinheiro troca de mãos:

<img width="1115" height="330" alt="image" src="https://github.com/user-attachments/assets/01902760-628e-4602-8589-31d9e866faa4" />

* **Mercado Rachado:** O mercado é bastante equilibrado, com o total de viagens dividido quase que pela metade (47.5% vs 52.5%) entre os dois principais fornecedores da cidade.
* **A Era do Cartão:** O cartão de crédito domina quase que totalmente a preferência de pagamento dos passageiros em relação ao dinheiro físico. Pagamentos em dinheiro se tornaram absoluta minoria.

### 🛠️ Ferramentas Utilizadas

* **Python e Streamlit:** Construção da interface e deploy do dashboard.
* **DuckDB e Parquet:** A dupla responsável pelo armazenamento otimizado e consultas SQL de alta performance direto nos arquivos.
* **Pandas e Plotly:** Tratamento refinado dos dados e criação de toda a camada visual dos gráficos dinâmicos.

###  Acesse o Projeto

Você pode interagir com o dashboard rodando direto no seu navegador através do link abaixo:

👉 **[Acessar o NYC Taxi Dashboard](https://nyc-taxi-dashboard-0.streamlit.app/)**

