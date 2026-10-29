### Função que permite ao usuário continuar ou encerrar o programa, retornando uma função específica até o usuário decidir sair
__all__ = ['continuar']

### Função para calcular um novo aparelho ou encerrar o programa
def continuar(msg_repetir, msg_encerramento, funcao):
    while True:
        try:
            ### Pergunta ao usuário se ele deseja continuar e verifica a resposta
            resposta = input(msg_repetir).strip().lower()

            ### Se o usuário quiser continuar, chama a função utilizada anteriormente
            if resposta == 's':
                funcao()
            ### Se o usuário não quiser continuar, encerra o loop e exibe a mensagem de encerramento
            elif resposta == 'n':
                if msg_encerramento is not None:
                    print(f"\n{msg_encerramento}")
                break
            ### Se a resposta não for válida, informa o usuário e continua o loop
            else:
                print("\n⚠️  Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.")
                continue

        ### Trata erros de entrada, como caracteres inválidos ou exceções inesperadas
        except Exception as e:
            print(f"\n❌  Ocorreu um erro: {e}")
            print("Por favor, tente novamente.")
            continue