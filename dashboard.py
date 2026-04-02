import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# --- CONFIGURACOES E CONSTANTES ---
DATA_SOURCE = 'dados_taxi_processados.parquet'
MILES_TO_KM = 1.60934

PAYMENT_MAP = {
    1: "Cartao", 2: "Dinheiro", 3: "Sem Cobranca", 
    4: "Disputa", 5: "Desconhecido", 6: "Anulado"
}

DAYS_PT = {
    "Monday": "Segunda", "Tuesday": "Terca", "Wednesday": "Quarta",
    "Thursday": "Quinta", "Friday": "Sexta", "Saturday": "Sabado", "Sunday": "Domingo"
}

ORDEM_DIAS_PT = ["Segunda", "Terca", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]

# Mapeamento EXAUSTIVO para traduzir todas as colunas da imagem
COL_RENAME_FULL = {
    "VendorID": "Fornecedor",
    "tpep_pickup_datetime_str": "Embarque",
    "passenger_count": "Passageiros",
    "trip_distance": "Distancia (KM)",
    "pickup_longitude": "Long. Embarque",
    "pickup_latitude": "Lat. Embarque",
    "RateCodeID": "Cod. Tarifa",
    "store_and_fwd_flag": "Flag S&F",
    "dropoff_longitude": "Long. Desembarque",
    "dropoff_latitude": "Lat. Desembarque",
    "fare_amount": "Tarifa ($)",
    "extra": "Extra",
    "mta_tax": "Taxa MTA",
    "tip_amount": "Gorjeta",
    "tolls_amount": "Pedagios",
    "improvement_surcharge": "Sobretaxa",
    "total_amount": "Total ($)",
    "duration_minutes": "Duracao (min)",
    "avg_speed_kmh": "Velocidade (km/h)",
    "tipo_pagamento": "Pagamento",
    "hora": "Hora",
    "dia_semana": "Dia"
}

# --- CONFIGURACAO DA PAGINA ---
st.set_page_config(
    page_title="Dashboard Taxi Amarelo NYC",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- ESTILIZACAO CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stMetric {
        background: rgba(255, 255, 255, 0.05);
        padding: 20px; border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .title-text {
        background: linear-gradient(90deg, #ffcc33, #ffd700, #ffffff);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 3rem;
    }
    .subtitle-text { color: #a0a0a0; font-size: 1.1rem; margin-bottom: 2rem; }
    div[data-testid="stMetricValue"] { font-size: 2.2rem; font-weight: 700; color: #ffcc33; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_and_process_data():
    try:
        con = duckdb.connect()
        df = con.sql(f"SELECT * FROM '{DATA_SOURCE}'").df()
        
        # Processamento de Tempo
        df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
        df["hora"] = df["tpep_pickup_datetime"].dt.hour
        df["dia_semana"] = df["tpep_pickup_datetime"].dt.day_name().map(DAYS_PT)
        df["tpep_pickup_datetime_str"] = df["tpep_pickup_datetime"].dt.strftime("%d/%m/%Y %H:%M")
        
        # Conversoes e Arredondamentos
        df["trip_distance"] = (df["trip_distance"] * MILES_TO_KM).round(2)
        df["avg_speed_kmh"] = (df["avg_speed_mph"] * MILES_TO_KM).round(2)
        df["tipo_pagamento"] = df["payment_type"].map(PAYMENT_MAP).fillna("Outro")
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# --- INTERFACE PRINCIPAL ---
df_raw = load_and_process_data()

if not df_raw.empty:
    with st.sidebar:
        st.header("Filtros")
        all_passengers = sorted(df_raw["passenger_count"].dropna().unique().tolist())
        passengers = st.multiselect("Numero de Passageiros", options=all_passengers, default=all_passengers)
        hora_range = st.slider("Intervalo de Horario", 0, 23, (0, 23))

    filtered_df = df_raw[
        (df_raw["passenger_count"].isin(passengers)) & 
        (df_raw["hora"].between(hora_range[0], hora_range[1]))
    ]

    st.markdown('<p class="title-text">Taxi Amarelo de NYC</p>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Dashboard de Analise Operacional — Area de Manhattan</p>', unsafe_allow_html=True)

    # Metricas
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total de Corridas", f"{len(filtered_df):,}")
    m2.metric("Distancia Media (KM)", f"{filtered_df['trip_distance'].mean():.2f} km")
    m3.metric("Velocidade Media (KM/H)", f"{filtered_df['avg_speed_kmh'].mean():.2f}")
    m4.metric("Tarifa Media", f"${filtered_df['fare_amount'].mean():.2f}")

    tab_overview, tab_business = st.tabs(["Visao Geral", "Analises de Negocio"])

    with tab_overview:
        col_left, col_right = st.columns(2)
        with col_left:
            st.subheader("Distribuicao da Duracao")
            st.plotly_chart(px.histogram(filtered_df, x="duration_minutes", nbins=30, color_discrete_sequence=["#ffcc33"]), use_container_width=True)
        with col_right:
            st.subheader("Distancia vs Tarifa")
            st.plotly_chart(px.scatter(filtered_df.sample(min(2000, len(filtered_df))), x="trip_distance", y="fare_amount", color_discrete_sequence=["#ffd700"]), use_container_width=True)
        
        st.markdown("---")
        st.subheader("Amostra de Registros Processados (100 primeiros)")
        
        # Filtro de colunas e renomeação
        excluir = {"tpep_pickup_datetime", "avg_speed_mph", "payment_type", "tpep_dropoff_datetime"}
        cols_show = [c for c in filtered_df.columns if c not in excluir]
        df_display = filtered_df[cols_show].head(100).rename(columns=COL_RENAME_FULL)
        
        # Converte colunas de contagem e ID para inteiro (remove o .0)
        cols_int = ["Passageiros", "Hora", "Fornecedor", "Cod. Tarifa"]
        for c in cols_int:
            if c in df_display.columns:
                df_display[c] = df_display[c].fillna(0).astype(int)

        # Regra automática para formatar TODAS as colunas decimais com 2 casas
        float_cols = df_display.select_dtypes(include=['float64', 'float32']).columns
        format_dict = {col: "{:.2f}" for col in float_cols}

        st.dataframe(
            df_display.style.format(format_dict).background_gradient(cmap="YlOrRd", subset=["Tarifa ($)"]), 
            use_container_width=True
        )

    with tab_business:
        st.markdown("### Analises de Negocio")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**1. Picos de Demanda por Hora**")
            df_hora = filtered_df.groupby("hora").size().reset_index(name="Corridas")
            st.plotly_chart(px.bar(df_hora, x="hora", y="Corridas", color_discrete_sequence=["#ffcc33"]), use_container_width=True)
        with c2:
            st.markdown("**2. Volume por Dia da Semana**")
            df_dia = filtered_df.groupby("dia_semana").size().reindex(ORDEM_DIAS_PT).reset_index(name="Corridas")
            st.plotly_chart(px.bar(df_dia, x="dia_semana", y="Corridas", color_discrete_sequence=["#ffd700"]), use_container_width=True)

        c3, c4 = st.columns(2)
        with c3:
            st.markdown("**3. Participacao de Mercado por Fornecedor**")
            df_vendor = filtered_df.groupby("VendorID").size().reset_index(name="Corridas")
            df_vendor["VendorID"] = df_vendor["VendorID"].apply(lambda x: f"Fornecedor {x}")
            st.plotly_chart(px.pie(df_vendor, names="VendorID", values="Corridas", hole=0.4, color_discrete_sequence=["#ffcc33", "#ffa500"]), use_container_width=True)
        with c4:
            st.markdown("**4. Distribuicao por Tipo de Pagamento**")
            df_pag = filtered_df.groupby("tipo_pagamento").size().reset_index(name="Corridas").sort_values("Corridas", ascending=False)
            st.plotly_chart(px.bar(df_pag, x="tipo_pagamento", y="Corridas", color_discrete_sequence=["#ffcc33"]), use_container_width=True)
else:
    st.warning("Nenhum dado carregado. Verifique o caminho do arquivo parquet.")