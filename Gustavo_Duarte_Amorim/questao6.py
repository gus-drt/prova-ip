### Gustavo Duarte Amorim - Matrícula: 202504003 - E-mail: gustavoduarte@discente.ufg.br
### Questão 6 - Dashboard em tempo real das 100 principais criptomoedas do mundo

### Importando as bibliotecas necessárias como pycoingecko para acessar a API da CoinGecko, pandas para manipulação de dados e streamlit para criar o dashboard
import streamlit as st
from pycoingecko import CoinGeckoAPI
import pandas as pd

### Configura o título e layout do dashboard
st.set_page_config(page_title="Dashboard Criptomoedas", layout="wide")
st.markdown("""
<div style='text-align: center;'>
    <img src='https://upload.wikimedia.org/wikipedia/commons/4/46/Bitcoin.svg' width='80'/>
</div>
<h1 style='text-align: center;'>Dashboard das 100 principais Criptomoedas</h1>
<div style='display: flex; justify-content: center; margin-bottom: 20px;'>
    <span style='font-size: 1.2em; max-width: 700px; text-align: center;'>
    Este dashboard exibe em tempo real as 100 principais criptomoedas do mundo, com dados de preço, valor de mercado e variação nas últimas 24h. Você pode atualizar manualmente e visualizar os números de forma clara e centralizada.
    </span>
</div>
""", unsafe_allow_html=True)

cg = CoinGeckoAPI()

### Função para obter os dados das 100 principais criptomoedas
@st.cache_data(ttl=60)
def get_top_100_cryptos():
    data = cg.get_coins_markets(vs_currency='usd', order='market_cap_desc', per_page=100, page=1)
    df = pd.DataFrame(data)
    df = df[["market_cap_rank", "name", "symbol", "current_price", "market_cap", "price_change_percentage_24h"]]
    df = df.rename(columns={
        "market_cap_rank": "Rank",
        "name": "Nome",
        "symbol": "Símbolo",
        "current_price": "Preço (USD)",
        "market_cap": "Market Cap",
        "price_change_percentage_24h": "% 24h"
    })
    # Formatação dos valores monetários
    df["Preço (USD)"] = df["Preço (USD)"].apply(lambda x: f'$ {x:,.2f}'.replace(",", "."))
    df["Market Cap"] = df["Market Cap"].apply(lambda x: f'$ {x:,.0f}'.replace(",", "."))
    # Formatação da variação percentual
    df["% 24h"] = df["% 24h"].apply(lambda x: f'{x:.2f}%' if pd.notnull(x) else "-")
    return df

### Botão para atualizar os dados manualmente
if st.button("Atualizar Dados"):
    st.cache_data.clear()

### Obtém os dados das 100 principais criptomoedas
df = get_top_100_cryptos()

# Cemtraliza os dados dentro do dataframe
st.dataframe(df.style.set_properties(**{'text-align': 'center'}), use_container_width=True)
st.markdown("---")
st.caption("Fonte: CoinGecko API | Atualização automática a cada 1 minuto ou manual pelo botão acima.")