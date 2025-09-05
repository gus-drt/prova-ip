# Gustavo Duarte Amorim - Matrícula: 202504003 - E-mail: gustavoduarte@discente.ufg.br
# Questão 2 - Programa de gestão financeira (GestorPy)

import funcoes as fun
import pandas as pd
import os

### Vairiáveis globais
metas_gastos = {}
lancamentos = []

### Função para definir metas de gastos mensais através de um loop while que solicita o input do usuário
def definir_meta():
    while True:
        categoria = input('📂  Digite o nome da categoria: ').strip()
        if not categoria:
            print('\n⚠️  Nome da categoria não pode ser vazio.')
            continue
        if not categoria.isalpha():
            print('\n⚠️  Nome da categoria deve conter apenas letras.')
            continue
        try:
            meta = float(input(f"💰  Digite a meta de gasto para '{categoria}' R$: "))
            if meta < 0:
                print('\n⚠️  O valor da meta não pode ser negativo.')
                continue
            metas_gastos[categoria] = meta
            print(f"✅  Meta de: R$ {meta:.2f} | Categoria: {categoria}.")
            break
        except ValueError:
            print('\n❌  Valor inválido. Por favor, digite um número para a meta.')

### Função para solicitar a definição de metas de gastos mensais e verificar se o usuário deseja continuar
def solicitar_metas():
    print('\nℹ️  Definição de Metas de Gastos Mensais')
    fun.continuar("\n💰  Deseja adicionar uma meta de gastos? (s/n): ",
                  "✅  Metas de gastos definidas.",
                  definir_meta)
    if not metas_gastos:
        print('\n⚠️  Nenhuma meta de gasto foi definida. O relatório de comparação com metas não será completo.')

### Função para registrar os lançamentos financeiros que usa um loop while para definir o número de lançamentos
### e um loop for para registrar cada lançamento
def registrar_lancamentos():
    print('\n💳  Registro de Lançamentos Financeiros')
    ### Loop para definir o número de lançamentos financeiros
    while True:
        try:
            qtd_lancamentos = int(input('🤖  Digite o número total de lançamentos financeiros que deseja registrar: '))
            if qtd_lancamentos < 0:
                print('\n⚠️  O número de lançamentos não pode ser negativo.')
                continue
            break
        except ValueError:
            print('\n❌  Entrada inválida. Por favor, digite um número inteiro.')
    
    ### Loop para registrar cada lançamento financeiro
    for i in range(qtd_lancamentos):
        print(f'\n💳  Lançamento {i + 1}')
        while True:
            try:
                valor = float(input('💰  Valor da despesa: R$ '))
                if valor < 0:
                    print('\n⚠️  O valor da despesa não pode ser negativo.')
                    continue
                break
            except ValueError:
                print('\n❌  Valor inválido. Por favor, digite um número.')
        while True:
            categoria = input('📂  Categoria da despesa: ').strip()
            if not categoria:
                print('\n⚠️  Nome da categoria não pode ser vazio.')
                continue
            if metas_gastos and categoria not in metas_gastos:
                print(f"\nℹ️  A categoria '{categoria}' não possui uma meta definida. Categorias com metas: {', '.join(metas_gastos.keys())}")
            break
        while True:
            descricao = input('📝  Descrição da despesa (ex: Mercado, Transporte, Internet): ').strip()
            if not descricao:
                print('\n⚠️  A descrição não pode ser vazia.')
                continue
            lancamentos.append({'valor': valor, 'categoria': categoria, 'descricao': descricao})
            print('✅  Lançamento registrado com sucesso!')
            break

def exportar_relatorio_txt(df_lancamentos, df_gastos_cat, total_despesas, cat_maior_gasto):
    with open('relatorio_financeiro.txt', 'w', encoding='utf-8') as f:
        f.write('📊 Relatório de Controle Financeiro Mensal 📊\n')
        f.write('='*50 + '\n')
        f.write(f'\n💰 Total de Despesas no Mês: R$ {total_despesas:.2f}\n')
        f.write(f"\n📂 Categoria com Maior Gasto: {cat_maior_gasto}\n")

        ### Iteração para exibir os gastos por categoria
        f.write('\n📂 Gastos por Categoria:\n')
        for _, row in df_gastos_cat.iterrows():
            f.write(f"  - {row['categoria']}: R$ {row['valor']:.2f}\n")

        ### Iteração para exibir a média de gastos por categoria
        f.write('\n💵 Média de Gastos por Categoria (por lançamento):\n')
        for _, row in df_gastos_cat.iterrows():
            f.write(f"  - {row['categoria']}: R$ {row['media_gasto_cat']:.2f} (Total de {row['num_lancamentos']} lançamento(s))\n")
        
        if metas_gastos:
            f.write('\n📊  Análise Comparativa com Metas:\n')
            ### Itera sobre as categorias e valores para comparar com as metas
            for categoria, meta in metas_gastos.items():
                gasto_cat_atual = df_gastos_cat[df_gastos_cat['categoria'] == categoria]['valor'].sum()
                if gasto_cat_atual == 0 and meta > 0:
                    f.write(f"  - {categoria}: Meta R$ {meta:.2f}. | ℹ️  Nenhum gasto registrado nesta categoria.\n")
                elif gasto_cat_atual <= meta:
                    f.write(f"  - {categoria}: Meta R$ {meta:.2f}, Gasto R$ {gasto_cat_atual:.2f}. | ✅  Você está DENTRO da meta!\n")
                else:
                    f.write(f"  - {categoria}: Meta R$ {meta:.2f}, Gasto R$ {gasto_cat_atual:.2f}. | ⚠️  ATENÇÃO! Você ULTRAPASSOU a meta em R$ {gasto_cat_atual - meta:.2f}.\n")
            
            cat_com_gastos = set(df_lancamentos['categoria'].unique())
            cat_sem_metas_com_gastos = cat_com_gastos - set(metas_gastos.keys())
            
            ### Verifica se há categorias com gastos mas sem metas definidas
            if cat_sem_metas_com_gastos:
                f.write('\nℹ️  Observação: As seguintes categorias tiveram gastos mas não possuem metas definidas:\n')
                ### Itera sobre as categorias e valores para exibir os gastos sem metas
                for cat in cat_sem_metas_com_gastos:
                    gasto_cat_sem_meta = df_gastos_cat[df_gastos_cat['categoria'] == cat]['valor'].sum()
                    f.write(f"  - {cat}: Gasto R$ {gasto_cat_sem_meta:.2f}\n")
        else:
            f.write('\nℹ️  Nenhuma meta de gastos foi definida para comparação.\n')
    return 'relatorio_financeiro.txt'

def analisar_despesas():
    ### Verifica se há lançamentos financeiros registrados
    if not lancamentos:
        print('\nℹ️  Nenhum lançamento financeiro foi registrado. Não há o que analisar.')
        return
    
    ### Cria um DataFrame a partir dos lançamentos financeiros se houver
    df_lancamentos = pd.DataFrame(lancamentos)
    total_despesas = df_lancamentos['valor'].sum()
    df_gastos_cat = df_lancamentos.groupby('categoria')['valor'].sum().reset_index()

    print('\n ------ 📊 Análise Financeira ------ ')
    print(f'\n💰  Total de Despesas no Mês: R$ {total_despesas:.2f}')

    ### Iteração para exibir os gastos por categoria
    print('\n📂  Gastos por Categoria:')
    for _, row in df_gastos_cat.iterrows():
        print(f"  - {row['categoria']}: R$ {row['valor']:.2f}")
    qtd_lancamentos_cat = df_lancamentos.groupby('categoria')['descricao'].count().reset_index(name='num_lancamentos')
    df_gastos_cat = pd.merge(df_gastos_cat, qtd_lancamentos_cat, on='categoria')
    df_gastos_cat['media_gasto_cat'] = df_gastos_cat['valor'] / df_gastos_cat['num_lancamentos']

    ### Iteração para exibir a média de gastos por categoria
    print('\n💵 Média de Gastos por Categoria (por lançamento):')
    for _, row in df_gastos_cat.iterrows():
        print(f"  - {row['categoria']}: R$ {row['media_gasto_cat']:.2f} (Total de {row['num_lancamentos']} lançamento(s))")
    if not df_gastos_cat.empty:
        cat_maior_gasto = df_gastos_cat.loc[df_gastos_cat['valor'].idxmax()]['categoria']
        valor_maior_gasto = df_gastos_cat['valor'].max()
        print(f"\n📂  Categoria com Maior Gasto: {cat_maior_gasto} (R$ {valor_maior_gasto:.2f})")
    else:
        cat_maior_gasto = 'Nenhuma (sem gastos)'
        print('\n📂  Categoria com Maior Gasto: Nenhuma (sem gastos)')

    ### Verifica se há metas para gastos e exibe a comparação entre gastos e metas
    if metas_gastos:
        print('\n📊  Análise Comparativa com Metas:')
        ### Itera sobre as categorias e valores para comparar com as metas
        for categoria, meta in metas_gastos.items():
            gasto_cat_atual = df_gastos_cat[df_gastos_cat['categoria'] == categoria]['valor'].sum()
            if gasto_cat_atual == 0 and meta > 0:
                print(f"  - {categoria}: Meta R$ {meta:.2f}. | ℹ️  Nenhum gasto registrado nesta categoria.")
            elif gasto_cat_atual <= meta:
                print(f"  - {categoria}: Meta R$ {meta:.2f}, Gasto R$ {gasto_cat_atual:.2f}. | ✅  Você está DENTRO da meta!")
            else:
                print(f"  - {categoria}: Meta R$ {meta:.2f}, Gasto R$ {gasto_cat_atual:.2f}. | ⚠️  ATENÇÃO! Você ULTRAPASSOU a meta em R$ {gasto_cat_atual - meta:.2f}.")
        cat_com_gastos = set(df_lancamentos['categoria'].unique())
        cat_sem_metas_com_gastos = cat_com_gastos - set(metas_gastos.keys())

        ### Verifica se há categorias com gastos mas sem metas definidas
        if cat_sem_metas_com_gastos:
            print('\nℹ️  Observação: As seguintes categorias tiveram gastos mas não possuem metas definidas:')
            ### Itera sobre as categorias e valores para exibir os gastos sem metas
            for cat in cat_sem_metas_com_gastos:
                gasto_cat_sem_meta = df_gastos_cat[df_gastos_cat['categoria'] == cat]['valor'].sum()
                print(f"  - {cat}: Gasto R$ {gasto_cat_sem_meta:.2f}")
    else:
        print('\nℹ️  Nenhuma meta de gastos foi definida para comparação.')
        
    ### Exporta o relatório em formato TXT
    print('\n📑 Gerando relatório em TXT...')
    caminho = exportar_relatorio_txt(df_lancamentos, df_gastos_cat, total_despesas, cat_maior_gasto)
    print(f'✅ Relatório gerado com sucesso! Arquivo: {os.path.abspath(caminho)}')

def main():
    ### 1. Exibe mensagem de boas-vindas e instruções
    print("\n🤗  Bem-vindo ao GestorPy. Seu Sistema de Controle de Finanças Pessoais!" \
          "\n💰  Este programa irá ajudá-lo a gerenciar suas finanças pessoais, registrando seus gastos e comparando-os com suas metas mensais." \
          "\n📊  Siga as instruções para inserir os dados corretamente. Vamos começar? 😉")

    print('\nℹ️  Instruções:')
    print('⚠️  Utilize pontos (.) para separar os decimais e evite usar vírgulas (,). Exemplo: 10.50' \
          '\n⚠️  As categorias de gastos podem ser definidas livremente, mas é recomendável usar categorias comuns como: Alimentação, Transporte, Lazer, etc.')
    ### 2. Chama a função para definir metas de gastos
    solicitar_metas()
    
    ### 3. Chama a função para registrar os lançamentos financeiros
    registrar_lancamentos()

    ### 4. Chama a função para analisar os lançamentos financeiros
    analisar_despesas()

    ### 5. Finaliza o programa e exibe mensagem de agradecimento
    print('\n🤗  Obrigado por usar o GestorPy!')

if __name__ == "__main__":
    main()