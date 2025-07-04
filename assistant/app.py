import streamlit as st
import os
import psycopg2
import pandas as pd
from agent import ask_ai

# Configurações da página
st.set_page_config(page_title="🌤️ Clima em Natal - Assistente IA", layout="wide")
st.title("🌤️ Painel de Clima em Natal - Assistente IA")

# Variáveis de conexão
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weather")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

# Conexão com o banco
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def run_query(query: str, params=None) -> pd.DataFrame:
    with get_connection() as conn:
        return pd.read_sql_query(query, conn, params=params)

# Campo de pergunta para IA
user_question = st.text_input("🧠 Pergunte algo sobre o clima em Natal:")
with st.expander("💡 Exemplos de perguntas que você pode fazer"):
    st.markdown("""
### 🌡️ **Temperatura**
- Qual foi a maior temperatura registrada?
- Qual é a média de temperatura dos últimos 7 dias?
- Quantas vezes a temperatura ficou abaixo de 20°C este mês?
- Qual era a temperatura às 15h do dia 1º de julho de 2025?

### 💨 **Vento**
- Qual foi a maior velocidade do vento registrada?
- Qual a direção predominante dos ventos nos últimos dias?
- Qual a média da velocidade do vento nos últimos 10 dias?

### 🌅 **Dia ou Noite**
- Quantas medições foram feitas durante o dia?
- Quantas vezes o clima foi registrado como noite nos últimos 5 dias?
- Qual foi a temperatura mais alta registrada durante o dia?

### 🕒 **Datas e horários**
- Quais foram os registros climáticos mais recentes?
- Me mostre os dados de clima do dia 2 de julho de 2025
- Qual o clima registrado nas últimas 24 horas?

### 🌎 **Localização**
- Qual é a elevação da estação de medição?
- Qual a latitude e longitude dos dados registrados?

### 🧠 **Perguntas gerais**
- Está fazendo calor em Natal hoje?
- Os ventos estão fortes esta semana?
- A temperatura média aumentou ou diminuiu nos últimos dias?
    """)


if user_question:
    with st.spinner("Consultando IA..."):
        resposta = ask_ai(user_question)
        st.success(resposta)

# DASHBOARD
st.markdown("---")
st.header("📊 Análises Climáticas de Natal")

col1, col2 = st.columns(2)

# COLUNA 1
with col1:
    st.subheader("🌡️ Temperatura Atual")
    temp_atual = run_query("""
        SELECT temperature_celsius, measurement_datetime 
        FROM natal_weather_records
        ORDER BY measurement_datetime DESC
        LIMIT 1
    """)

    st.metric("Temperatura", f"{temp_atual['temperature_celsius'].iloc[0]} °C")
    st.caption(f"Última medição: {temp_atual['measurement_datetime'].iloc[0].strftime('%d/%m/%Y %H:%M')}")

    st.subheader("📈 Temperatura Média do Dia")
    media_temp = run_query("""
        SELECT ROUND(AVG(temperature_celsius), 2) AS media
        FROM natal_weather_records
        WHERE measurement_datetime::date = CURRENT_DATE
    """)
    st.write(f"📊 Temperatura média hoje: **{media_temp['media'].iloc[0]} °C**")

    st.subheader("🌡️ Máxima e Mínima Hoje")
    extremos = run_query("""
        SELECT 
            MAX(temperature_celsius) AS maxima,
            MIN(temperature_celsius) AS minima
        FROM natal_weather_records
        WHERE measurement_datetime::date = CURRENT_DATE
    """)
    st.write(f"🔥 Máxima: **{extremos['maxima'].iloc[0]} °C**")
    st.write(f"❄️ Mínima: **{extremos['minima'].iloc[0]} °C**")

# COLUNA 2
with col2:
    st.subheader("💨 Velocidade Média do Vento Hoje")
    vento = run_query("""
        SELECT ROUND(AVG(wind_speed_kmh), 2) AS media_vento
        FROM natal_weather_records
        WHERE measurement_datetime::date = CURRENT_DATE
    """)
    st.write(f"🍃 Média: **{vento['media_vento'].iloc[0]} km/h**")

    st.subheader("🧭 Direção Média do Vento")
    direcao = run_query("""
        SELECT ROUND(AVG(wind_direction_degrees), 0) AS direcao_media
        FROM natal_weather_records
        WHERE measurement_datetime::date = CURRENT_DATE
    """)
    st.write(f"🧭 Direção média: **{direcao['direcao_media'].iloc[0]}°**")

    st.subheader("📊 Condições Climáticas Mais Comuns")
    codigos = run_query("""
        SELECT weather_condition_code, COUNT(*) AS total
        FROM natal_weather_records
        GROUP BY weather_condition_code
        ORDER BY total DESC
        LIMIT 5
    """)
    st.dataframe(codigos.rename(columns={"weather_condition_code": "Código", "total": "Ocorrências"}))

# Rodapé
st.markdown("---")
st.caption("💻 Desenvolvido por Tiago Oliveira com dados da API METEO.")
