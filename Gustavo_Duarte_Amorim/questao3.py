# Gustavo Duarte Amorim - Matrícula: 202504003 - E-mail: gustavoduarte@discente.ufg.br
# Questão 3 - Análise de dados climáticos (ClimaPy)

import numpy as np
import pandas as pd
import os

### Função para gerar dados de temperatura por meio do NumPy utilizando a função uniform
def gerar_dados_temperatura():
    np.random.seed(42)
    temperaturas = np.round(np.random.uniform(10, 35, 30), 1)
    return temperaturas

### Função para calcular estatísticas
def calcular_estatisticas(temperaturas):
    media = np.mean(temperaturas)
    mediana = np.median(temperaturas)
    desvio_padrao = np.std(temperaturas)
    variacao_termica = np.max(temperaturas) - np.min(temperaturas)
    return media, mediana, desvio_padrao, variacao_termica

### Função que cria um DataFrame com os dados de temperatura, média e diferença
def criar_dataframe(temperaturas, media):
    dias = []
    temp = []
    dif = []
    for i in range(30):
        dias.append(i+1)
        temp.append(temperaturas[i])
        dif.append(round(temperaturas[i] - media, 1))
    df = pd.DataFrame({'Dia': dias, 'Temperatura (°C)': temp, 'Diferença para a média': dif})
    return df

### Função que adiciona a classificação térmica ao DataFrame de acordo com a temperatura
def adicionar_classificacao_termica(df):
    classificacoes = []
    for t in df['Temperatura (°C)']:
        if t < 18:
            classificacoes.append('Frio')
        elif t <= 25:
            classificacoes.append('Agradável')
        else:
            classificacoes.append('Quente')
    df['Classificação térmica'] = classificacoes
    return df

### Função que conta os dias de acordo com a classificação térmica
def contar_dias_por_classificacao(df):
    contagem = {}
    for c in df['Classificação térmica']:
        if c in contagem:
            contagem[c] += 1
        else:
            contagem[c] = 1
    return contagem

### Função que encontra os 5 dias mais quentes e mais frios
def encontrar_dias_extremos(df):
    mais_quentes = df.sort_values('Temperatura (°C)', ascending=False).head(5)
    mais_frios = df.sort_values('Temperatura (°C)').head(5)
    return mais_quentes, mais_frios

### Função que classifica a relação dos dias extremos com a média
def classificacao_relacao_media(dias_extremos):
    relacoes = []
    for d in dias_extremos['Diferença para a média']:
        if d > 0:
            relacoes.append('Acima da média mensal')
        elif d < 0:
            relacoes.append('Abaixo da média mensal')
        else:
            relacoes.append('Exatamente na média')
    dias_extremos['Relação com a média'] = relacoes
    return dias_extremos

### Função que exporta o relatório em formato TXT com as informações analisadas
def exportar_relatorio_txt(df, media, mediana, desvio_padrao, variacao_termica):
    nome_arquivo = 'relatorio_temperaturas.txt'
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        f.write('📊 Análise de Temperaturas Diárias 📊\n')
        f.write('='*50 + '\n')
        f.write('\n📈 Estatísticas principais:\n')
        f.write(f'  • Média das temperaturas: {media:.1f}°C\n')
        f.write(f'  • Mediana das temperaturas: {mediana:.1f}°C\n')
        f.write(f'  • Desvio padrão: {desvio_padrao:.2f}°C\n')
        f.write(f'  • Variação térmica: {variacao_termica:.1f}°C\n')
        contagem = contar_dias_por_classificacao(df)

        ### Adiciona contagem de dias por classificação térmica
        f.write('\n🔢 Contagem de dias por classificação térmica:\n')
        for c in contagem:
            f.write(f"  • Dias '{c}': {contagem[c]}\n")

        ### Adiciona temperaturas diárias
        f.write('\n🌡️ Temperaturas diárias:\n')
        for i in range(len(df)):
            f.write(f"  Dia {df.iloc[i]['Dia']}: {df.iloc[i]['Temperatura (°C)']}°C | Diferença p/ média: {df.iloc[i]['Diferença para a média']} | {df.iloc[i]['Classificação térmica']}\n")
        mais_quentes, mais_frios = encontrar_dias_extremos(df)

        ### Adiciona os 5 dias mais quentes e frios
        f.write('\n🔥 5 dias mais quentes:\n')
        for i in range(len(mais_quentes)):
            f.write(f"  Dia {int(mais_quentes.iloc[i]['Dia'])}: {mais_quentes.iloc[i]['Temperatura (°C)']}°C | {mais_quentes.iloc[i]['Classificação térmica']}\n")
        f.write('\n❄️ 5 dias mais frios:\n')
        for i in range(len(mais_frios)):
            f.write(f"  Dia {int(mais_frios.iloc[i]['Dia'])}: {mais_frios.iloc[i]['Temperatura (°C)']}°C | {mais_frios.iloc[i]['Classificação térmica']}\n")
        
        ### Adiciona a relação dos dias extremos com a média
        f.write('\n📋 Relação dos dias extremos com a média:\n')
        dias_extremos = pd.concat([mais_quentes, mais_frios])
        dias_extremos = classificacao_relacao_media(dias_extremos)
        for i in range(len(dias_extremos)):
            f.write(f"  Dia {int(dias_extremos.iloc[i]['Dia'])}: {dias_extremos.iloc[i]['Temperatura (°C)']}°C | {dias_extremos.iloc[i]['Classificação térmica']} | Diferença: {dias_extremos.iloc[i]['Diferença para a média']} | {dias_extremos.iloc[i]['Relação com a média']}\n")
    return nome_arquivo

### Função que exibe os resultados de forma organizada e resumida
def mostrar_resultados(df, media, mediana, desvio_padrao, variacao_termica):
    print("\n📊 Análise de Temperaturas Diárias - Resumo 📊")
    print("=" * 50)
    print("\n📈 Estatísticas principais:")
    print(f"  • Média das temperaturas: {media:.1f}°C")
    print(f"  • Mediana das temperaturas: {mediana:.1f}°C")
    print(f"  • Desvio padrão: {desvio_padrao:.2f}°C")
    print(f"  • Variação térmica: {variacao_termica:.1f}°C")
    
    # Mostrar apenas contagem de dias por classificação
    contagem = contar_dias_por_classificacao(df)
    print("\n🔢 Contagem de dias por classificação térmica:")
    for c in contagem:
        print(f"  • Dias '{c}': {contagem[c]}")
    
    # Informação resumida sobre temperaturas extremas
    mais_quentes, mais_frios = encontrar_dias_extremos(df)
    print(f"\n🔥 Temperatura mais alta: {df['Temperatura (°C)'].max()}°C (Dia {df['Temperatura (°C)'].idxmax()+1})")
    print(f"❄️ Temperatura mais baixa: {df['Temperatura (°C)'].min()}°C (Dia {df['Temperatura (°C)'].idxmin()+1})")
    
    # Gerar relatório completo em TXT
    print("\n📑 Gerando relatório detalhado em TXT...")
    caminho = exportar_relatorio_txt(df, media, mediana, desvio_padrao, variacao_termica)
    print(f"✅ Relatório detalhado gerado com sucesso! Arquivo: {os.path.abspath(caminho)}")
    print("   Consulte o arquivo para análise completa das temperaturas.")

def main():
    print("\nBem-vindo ao ClimaPy! 🌤️")
    print("Este programa irá gerar e analisar dados de temperatura para um mês. 📊")
    temperaturas = gerar_dados_temperatura()
    print("\nDados de temperatura gerados com sucesso! ✅")
    print("Foram geradas 30 temperaturas médias diárias entre 10°C e 35°C.")
    media, mediana, desvio_padrao, variacao_termica = calcular_estatisticas(temperaturas)
    df = criar_dataframe(temperaturas, media)
    df = adicionar_classificacao_termica(df)
    mostrar_resultados(df, media, mediana, desvio_padrao, variacao_termica)

if __name__ == "__main__":
    main()