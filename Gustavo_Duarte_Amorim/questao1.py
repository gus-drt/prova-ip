# Gustavo Duarte Amorim - Matrícula: 202504003 - E-mail: gustavoduarte@discente.ufg.br
# Questão 1 - Programa de cálculo de consumo de energia elétrica (EletroPy)

## Realizando as importações necessárias
import funcoes as fun

## Definindo as funções necessárias para executar o programa
### Função para registrar a entrada de dados do aparelho (com a função calcular_consumo_mensal()) e fornecer output do consumo
def entrada_consumo():
    while True:
        ### Chama a função de cálculo de consumo mensal e verifica se o retorno é válido
        consumo = calcular_consumo_mensal(0, 0)
        if consumo is not None:
            print(f"\n⚡  O consumo mensal do aparelho é de: {consumo:.2f} kWh")
            break
        ### Se o retorno for None, significa que houve um erro na entrada de dados e o loop continua
        else:
            print("Tente novamente.")
            continue

### Função para calcular o consumo mensal
def calcular_consumo_mensal(potencia=None, horas=None):
    try:
        ### Solicita ao usuário a potência do aparelho e verifica se a entrada é válida
        entrada_pot = input("\nDigite a potência do aparelho em kW: ")
        if ',' in entrada_pot:
            print("\n⚠️  Por favor, use ponto (.) em vez de vírgula (,) para separar os decimais.")
            return None

        potencia = float(entrada_pot)

        if potencia <= 0:
            print("\n⚠️  A potência deve ser um número positivo entre 1kW e 10kW (1000W = 1kW).")
            return None
        elif potencia > 10:
            print("\n⚠️  Este valor é muito alto para um equipamento residencial.")
            print("⚠️  Por favor, digite um valor entre 1kW e 10kW. (1000W = 1kW)")
            return None

        ### Solicita ao usuário o número de horas que o aparelho fica ligado por dia e verifica se a entrada é válida.
        entrada_horas = input("Digite o número de horas que o aparelho fica ligado por dia: ")
        if ',' in entrada_horas:
            print("\n⚠️  Por favor, use ponto (.) em vez de vírgula (,) para separar os decimais.")
            return None

        horas = float(entrada_horas)

        if horas < 0 or horas > 24:
            print("\n⚠️  O número de horas deve ser entre 0 e 24.")
            return None

    ### Tratamento de exceções para entradas inválidas
    except ValueError as e:
        print(f"\n❌  Por favor, insira um número válido.\nErro: {e}")
        return None

    consumo_mensal = potencia * horas * 30
    return consumo_mensal

### Função para executar o programa
def main():
    ### Mensagem de boas-vindas e instruções
    print("\nBem-vindo à calculadora de consumo EletroPy! 🤗")
    print("Este programa irá ajudá-lo a estimar o consumo mensal de energia elétrica do seu aparelho eletrônico residencial. ⚡")
    print("Por favor, siga as instruções para inserir os dados corretamente. 😉")

    ### Chamada da função de entrada de dados e adição de novos aparelhos
    entrada_consumo()
    fun.continuar("\n🤖  Deseja calcular o consumo de outro aparelho? (s/n): ", 
              "🤗  Obrigado por usar o EletroPy! Até logo! 👋", 
              entrada_consumo)

## Chama a função principal para iniciar o programa
if __name__ == "__main__":
    main()