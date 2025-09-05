# Gustavo Duarte Amorim - Matrícula: 202504003 - E-mail: gustavoduarte@discente.ufg.br
# Questão 4 - Jogo Tetris com pygame

# Importando as bibliotecas necessárias
import pygame
import random
import sys

# Inicializando o pygame
pygame.init()

# ---------------------- CONFIGURAÇÕES INICIAIS ----------------------
# Define o tamanho da grade do jogo
GRADE_W = 10  # largura em blocos
GRADE_H = 20  # altura em blocos
BLOCO = 30    # tamanho de cada bloco em pixels

# Espaço reservado para exibir a pontuação acima da grade
ESPACO_TOPO = 50  # pixels

# Calcula o tamanho da janela para caber a grade e o espaço do topo
LARGURA = GRADE_W * BLOCO
ALTURA = GRADE_H * BLOCO + ESPACO_TOPO

# Configura a janela do jogo
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Tetris Game")
RELOGIO = pygame.time.Clock()

# Cores utilizadas
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
CORES = [
    (0, 255, 255),   # Ciano
    (255, 255, 0),   # Amarelo
    (255, 0, 255),   # Magenta
    (0, 255, 0),     # Verde
    (255, 0, 0),     # Vermelho
    (0, 0, 255),     # Azul
    (255, 165, 0)    # Laranja
]

# Formas das peças do Tetris
PECAS = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 0], [0, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]]
]

# ---------------------- CLASSE PRINCIPAL DO JOGO ----------------------
class Tetris:
    def __init__(self):
        # Inicializa a grade do jogo (matriz de zeros)
        self.grade = [[0 for _ in range(GRADE_W)] for _ in range(GRADE_H)]
        # Gera a primeira peça
        self.peca = self.nova_peca()
        # Define a posição inicial da peça
        self.x = GRADE_W // 2 - 1
        self.y = 0
        # Inicializa a pontuação
        self.pontos = 0
        # Variáveis de controle de tempo e velocidade
        self.tempo = 0
        self.velocidade = 500
        # Fonte para exibir textos
        self.fonte = pygame.font.Font(None, 36)

    # Função para gerar uma nova peça aleatória
    def nova_peca(self):
        return random.choice(PECAS)

    # Função para verificar se a posição da peça é válida
    def valido(self, peca, x, y):
        for i in range(len(peca)):
            for j in range(len(peca[i])):
                if peca[i][j]:
                    nx = x + j
                    ny = y + i
                    if nx < 0 or nx >= GRADE_W or ny >= GRADE_H:
                        return False
                    if ny >= 0 and self.grade[ny][nx]:
                        return False
        return True

    # Função para fixar a peça na grade
    def colocar(self):
        for i in range(len(self.peca)):
            for j in range(len(self.peca[i])):
                if self.peca[i][j]:
                    self.grade[self.y + i][self.x + j] = 1
        self.limpar_linhas()
        self.peca = self.nova_peca()
        self.x = GRADE_W // 2 - 1
        self.y = 0
        if not self.valido(self.peca, self.x, self.y):
            return False  # Game Over
        return True

    # Função para limpar linhas completas e atualizar a pontuação
    def limpar_linhas(self):
        linhas = 0
        i = GRADE_H - 1
        while i >= 0:
            if all(self.grade[i]):
                del self.grade[i]
                self.grade.insert(0, [0 for _ in range(GRADE_W)])
                linhas += 1
            else:
                i -= 1
        self.pontos += linhas * 100

    # Função para rotacionar a peça atual
    def rotacionar(self):
        linhas = len(self.peca)
        colunas = len(self.peca[0])
        nova = [[self.peca[linhas - 1 - j][i] for j in range(linhas)] for i in range(colunas)]
        if self.valido(nova, self.x, self.y):
            self.peca = nova

    # Função para mover a peça
    def mover(self, dx, dy):
        novo_x = self.x + dx
        novo_y = self.y + dy
        if self.valido(self.peca, novo_x, novo_y):
            self.x = novo_x
            self.y = novo_y
            return True
        return False

    # Função para desenhar todos os elementos na tela
    def desenhar(self):
        # Preenche o fundo de preto
        TELA.fill(PRETO)

        # Desenha a pontuação no topo da tela
        texto = self.fonte.render(f"Pontos: {self.pontos}", True, BRANCO)
        texto_rect = texto.get_rect(center=(LARGURA // 2, ESPACO_TOPO // 2))
        TELA.blit(texto, texto_rect)

        # Desenha a grade do jogo
        for i in range(GRADE_H):
            for j in range(GRADE_W):
                x_pos = j * BLOCO
                y_pos = i * BLOCO + ESPACO_TOPO
                cor = CORES[0] if self.grade[i][j] else PRETO
                pygame.draw.rect(TELA, cor, (x_pos, y_pos, BLOCO, BLOCO))
                pygame.draw.rect(TELA, BRANCO, (x_pos, y_pos, BLOCO, BLOCO), 1)

        # Desenha a peça atual
        for i in range(len(self.peca)):
            for j in range(len(self.peca[i])):
                if self.peca[i][j]:
                    x_pos = (self.x + j) * BLOCO
                    y_pos = (self.y + i) * BLOCO + ESPACO_TOPO
                    pygame.draw.rect(TELA, CORES[1], (x_pos, y_pos, BLOCO, BLOCO))
                    pygame.draw.rect(TELA, BRANCO, (x_pos, y_pos, BLOCO, BLOCO), 1)

        # Atualiza a tela
        pygame.display.flip()

    # Função para processar os eventos do teclado e janela
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                return False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    self.mover(-1, 0)
                elif evento.key == pygame.K_RIGHT:
                    self.mover(1, 0)
                elif evento.key == pygame.K_DOWN:
                    self.mover(0, 1)
                elif evento.key == pygame.K_UP:
                    self.rotacionar()
                elif evento.key == pygame.K_SPACE:
                    # Desce a peça até o final
                    while self.mover(0, 1):
                        self.pontos += 1
        return True

    # Função para atualizar o estado do jogo
    def atualizar(self, dt):
        self.tempo += dt
        if self.tempo >= self.velocidade:
            self.tempo = 0
            if not self.mover(0, 1):
                return self.colocar()
        return True

    # Função principal do loop do jogo
    def jogar(self):
        rodando = True
        while rodando:
            dt = RELOGIO.tick(60)
            if not self.processar_eventos():
                break
            if not self.atualizar(dt):
                # Exibe tela de Game Over
                TELA.fill(PRETO)
                game_over = pygame.font.Font(None, 72).render("GAME OVER", True, BRANCO)
                pontos_final = self.fonte.render(f"Pontos: {self.pontos}", True, BRANCO)
                restart = self.fonte.render("Pressione R para reiniciar", True, BRANCO)
                TELA.blit(game_over, (LARGURA // 2 - 150, ALTURA // 2 - 100))
                TELA.blit(pontos_final, (LARGURA // 2 - 80, ALTURA // 2 - 50))
                TELA.blit(restart, (LARGURA // 2 - 120, ALTURA // 2))
                pygame.display.flip()
                esperando = True
                while esperando:
                    for evento in pygame.event.get():
                        if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if evento.type == pygame.KEYDOWN:
                            if evento.key == pygame.K_r:
                                self.__init__()
                                esperando = False
                                break
                            elif evento.key == pygame.K_ESCAPE:
                                pygame.quit()
                                sys.exit()
                continue
            else:
                self.desenhar()
        pygame.quit()

# ---------------------- EXECUÇÃO PRINCIPAL ----------------------
if __name__ == "__main__":
    jogo = Tetris()
    jogo.jogar()