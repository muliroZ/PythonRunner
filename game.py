import pygame
import sys
import json
import os
import random

# ==============================================================
#  CONSTANTES — altere esses valores para ver o jogo mudar!
# ==============================================================
LARGURA        = 900
ALTURA         = 500
FPS            = 60

GRAVIDADE      = 0.6       # força que puxa o jogador pra baixo a cada frame
FORCA_PULO     = -13       # impulso negativo aplicado ao pular (negativo = sobe)
CHAO_Y         = 380       # posição Y do chão

VEL_INICIAL    = 5         # velocidade inicial dos obstáculos
ACELERACAO     = 0.002     # quanto o jogo acelera a cada frame
MAX_OBSTACULOS = 3         # máximo de obstáculos simultâneos na tela

ARQUIVO_SCORES = os.path.join(os.path.dirname(__file__), "scores.json")

# ==============================================================
#  CORES
# ==============================================================
PRETO      = (10,  10,  30)
AMARELO    = (226, 185, 111)
BRANCO     = (230, 230, 230)
CINZA      = (60,  60,  90)
CINZA_CLR  = (100, 100, 130)
VERMELHO   = (220, 80,  80)
VERDE      = (80,  200, 120)
AZUL_ESC   = (22,  33,  62)
AZUL_MED   = (15,  52,  96)
LARANJA    = (230, 140, 50)

# ==============================================================
#  FUNÇÕES DE SCOREBOARD (JSON)
# ==============================================================
def carregar_scores():
    """Lê o arquivo scores.json e retorna a lista de pontuações."""
    try:
        with open(ARQUIVO_SCORES, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def salvar_score(nome, pontuacao):
    """Adiciona nova pontuação, ordena e salva no JSON."""
    scores = carregar_scores()
    scores.append({"nome": nome, "pontuacao": int(pontuacao)})
    # ordena do maior para o menor — conceito de sort()
    scores.sort(key=lambda x: x["pontuacao"], reverse=True)
    scores = scores[:10]  # guarda só o top 10
    with open(ARQUIVO_SCORES, "w") as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)
    return scores

# ==============================================================
#  CLASSE JOGADOR
# ==============================================================
class Jogador:
    LARGURA  = 44
    ALTURA   = 52
    X_FIXO   = 100  # jogador não se move no eixo X

    def __init__(self):
        self.x          = self.X_FIXO
        self.y          = float(CHAO_Y - self.ALTURA)
        self.vel_y      = 0.0
        self.no_chao    = True
        # animação de corrida
        self.frame_anim = 0
        self.tick_anim  = 0

    def pular(self):
        """Aplica FORCA_PULO se o jogador estiver no chão."""
        if self.no_chao:
            self.vel_y   = FORCA_PULO
            self.no_chao = False

    def update(self):
        """Atualiza física a cada frame — o coração da mecânica de pulo."""
        # 1. gravidade aumenta velocidade vertical
        self.vel_y += GRAVIDADE
        # 2. posição atualiza com base na nova velocidade
        self.y     += self.vel_y

        # 3. trava no chão
        if self.y >= CHAO_Y - self.ALTURA:
            self.y       = float(CHAO_Y - self.ALTURA)
            self.vel_y   = 0.0
            self.no_chao = True

        # animação de pernas
        self.tick_anim += 1
        if self.tick_anim >= 8:
            self.tick_anim  = 0
            self.frame_anim = (self.frame_anim + 1) % 4

    def rect(self):
        """Retorna o retângulo de colisão (AABB)."""
        return pygame.Rect(self.x + 4, int(self.y) + 4,
                           self.LARGURA - 8, self.ALTURA - 4)

    def draw(self, surface):
        ix = self.x
        iy = int(self.y)
        f  = self.frame_anim

        # sombra
        pygame.draw.ellipse(surface, CINZA,
                            (ix + 6, CHAO_Y - 6, 34, 10))

        # pernas animadas
        perna_esq_y = iy + 36 + (4 if f in (0, 2) else -4)
        perna_dir_y = iy + 36 + (4 if f in (1, 3) else -4)
        pygame.draw.rect(surface, AMARELO,  (ix + 10, perna_esq_y, 10, 18), border_radius=4)
        pygame.draw.rect(surface, AMARELO,  (ix + 24, perna_dir_y, 10, 18), border_radius=4)

        # corpo
        pygame.draw.rect(surface, AMARELO,  (ix + 6, iy + 14, 32, 28), border_radius=6)

        # braços
        braco_y = iy + 18 + (2 if f in (0, 2) else -2)
        pygame.draw.rect(surface, AMARELO,  (ix - 2, braco_y, 10, 8), border_radius=3)
        pygame.draw.rect(surface, AMARELO,  (ix + 36, braco_y + 4, 10, 8), border_radius=3)

        # cabeça
        pygame.draw.rect(surface, AMARELO,  (ix + 8, iy, 28, 22), border_radius=8)

        # olho
        olho_x = ix + 28
        olho_y = iy + 7
        pygame.draw.circle(surface, BRANCO, (olho_x, olho_y), 5)
        pygame.draw.circle(surface, PRETO,  (olho_x + 1, olho_y + 1), 2)

        # boca
        pygame.draw.rect(surface, LARANJA, (ix + 16, iy + 15, 12, 4), border_radius=2)

# ==============================================================
#  CLASSE OBSTÁCULO
# ==============================================================
class Obstaculo:
    def __init__(self, x, velocidade):
        self.largura    = random.randint(22, 36)
        self.altura     = random.randint(36, 70)
        self.x          = float(x)
        self.y          = CHAO_Y - self.altura
        self.velocidade = velocidade
        # variação visual
        self.cor        = random.choice([
            (60, 150, 80), (50, 130, 70), (40, 110, 60)
        ])
        self.n_hastes   = random.randint(1, 3)

    def update(self):
        """Move o obstáculo da direita pra esquerda — ilusão de movimento."""
        self.x -= self.velocidade

    def rect(self):
        """Retângulo de colisão AABB."""
        return pygame.Rect(int(self.x), self.y, self.largura, self.altura)

    def fora_da_tela(self):
        return self.x + self.largura < 0

    def draw(self, surface):
        ox = int(self.x)
        oy = self.y

        # tronco do cacto
        pygame.draw.rect(surface, self.cor,
                         (ox, oy, self.largura, self.altura), border_radius=6)
        pygame.draw.rect(surface, (self.cor[0]-10, self.cor[1]+20, self.cor[2]-10),
                         (ox + 4, oy, self.largura - 8, self.altura), border_radius=4)

        # hastes laterais
        for i in range(self.n_hastes):
            lado = 1 if i % 2 == 0 else -1
            haste_y = oy + self.altura // 3 + i * 14
            haste_w = 14
            haste_h = 10
            haste_x = ox + (self.largura if lado == 1 else -haste_w)
            pygame.draw.rect(surface, self.cor,
                             (haste_x, haste_y, haste_w, haste_h), border_radius=4)
            pygame.draw.rect(surface, self.cor,
                             (haste_x + (0 if lado == 1 else haste_w - 6),
                              haste_y - 8, 6, haste_h + 4), border_radius=3)

# ==============================================================
#  FUNÇÃO AUXILIAR — desenha texto com sombra
# ==============================================================
def draw_text(surface, texto, fonte, cor, x, y, centro=False):
    img = fonte.render(texto, True, cor)
    rect = img.get_rect()
    if centro:
        rect.centerx = x
    else:
        rect.x = x
    rect.y = y
    surface.blit(img, rect)

# ==============================================================
#  TELA DE GAME OVER / INPUT DE NOME
# ==============================================================
def tela_game_over(surface, clock, fonte_g, fonte_m, fonte_p, score, scores):
    nome       = ""
    salvo      = False
    scores_att = scores

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if not salvo:
                    if event.key == pygame.K_RETURN and nome.strip():
                        scores_att = salvar_score(nome.strip(), score)
                        salvo      = True
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    elif len(nome) < 16 and event.unicode.isprintable():
                        nome += event.unicode
                else:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        return  # volta ao menu

        surface.fill(PRETO)

        # painel central
        painel = pygame.Rect(LARGURA // 2 - 220, 60, 440, 370)
        pygame.draw.rect(surface, AZUL_ESC, painel, border_radius=12)
        pygame.draw.rect(surface, AZUL_MED, painel, 2, border_radius=12)

        draw_text(surface, "GAME OVER", fonte_g, VERMELHO, LARGURA // 2, 80, centro=True)
        draw_text(surface, f"Pontuação: {int(score)}", fonte_m, AMARELO,
                  LARGURA // 2, 140, centro=True)

        if not salvo:
            draw_text(surface, "Digite seu nome:", fonte_p, BRANCO,
                      LARGURA // 2, 200, centro=True)
            # caixa de input
            input_rect = pygame.Rect(LARGURA // 2 - 130, 225, 260, 36)
            pygame.draw.rect(surface, AZUL_MED, input_rect, border_radius=6)
            pygame.draw.rect(surface, AMARELO,  input_rect, 2, border_radius=6)
            cursor = "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else " "
            draw_text(surface, nome + cursor, fonte_p, BRANCO,
                      LARGURA // 2, 230, centro=True)
            draw_text(surface, "ENTER para salvar", fonte_p, CINZA_CLR,
                      LARGURA // 2, 278, centro=True)
        else:
            draw_text(surface, "Placar salvo!", fonte_p, VERDE,
                      LARGURA // 2, 200, centro=True)
            draw_text(surface, "SPACE para continuar", fonte_p, CINZA_CLR,
                      LARGURA // 2, 230, centro=True)

        # top 5
        draw_text(surface, "TOP 5", fonte_p, AMARELO, LARGURA // 2, 310, centro=True)
        for i, entrada in enumerate(scores_att[:5]):
            medalha = ["#1", "#2", "#3", "#4", "#5"][i]
            cor_pos  = [AMARELO, (180,180,180), (180,120,60), BRANCO, BRANCO][i]
            linha = f"{medalha}  {entrada['nome']:<14} {entrada['pontuacao']:>6}"
            draw_text(surface, linha, fonte_p, cor_pos,
                      LARGURA // 2 - 140, 335 + i * 22)

        pygame.display.flip()

# ==============================================================
#  TELA INICIAL
# ==============================================================
def tela_inicial(surface, clock, fonte_g, fonte_m, fonte_p, scores):
    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_UP):
                    return

        surface.fill(PRETO)

        # chão decorativo
        pygame.draw.rect(surface, AZUL_MED, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
        pygame.draw.line(surface, CINZA, (0, CHAO_Y), (LARGURA, CHAO_Y), 2)

        # cacto decorativo
        pygame.draw.rect(surface, (60, 150, 80), (700, CHAO_Y - 60, 28, 60), border_radius=6)
        pygame.draw.rect(surface, (60, 150, 80), (714, CHAO_Y - 80, 28, 40), border_radius=6)

        draw_text(surface, "ENDLESS RUNNER", fonte_g, AMARELO, LARGURA // 2, 80, centro=True)
        draw_text(surface, "Mostra Interativa de Computação", fonte_p, CINZA_CLR,
                  LARGURA // 2, 148, centro=True)

        draw_text(surface, "SPACE  /  SETA CIMA  para pular", fonte_m, BRANCO,
                  LARGURA // 2, 210, centro=True)

        # instrução
        pulsa = abs((pygame.time.get_ticks() % 1000) - 500) / 500
        cor_p = (int(180 + 50 * pulsa), int(160 + 25 * pulsa), int(80 + 30 * pulsa))
        draw_text(surface, "Pressione SPACE para jogar", fonte_p, cor_p,
                  LARGURA // 2, 270, centro=True)

        # scoreboard
        if scores:
            draw_text(surface, "RECORDES", fonte_p, AMARELO, LARGURA // 2, 330, centro=True)
            for i, entrada in enumerate(scores[:5]):
                cor_i = [AMARELO, (180,180,180), (180,120,60), BRANCO, BRANCO][i]
                draw_text(surface, f"#{i+1}  {entrada['nome']:<14} {entrada['pontuacao']:>6}",
                          fonte_p, cor_i, LARGURA // 2 - 120, 358 + i * 22)

        pygame.display.flip()

# ==============================================================
#  LOOP PRINCIPAL DO JOGO
# ==============================================================
def jogar(surface, clock, fonte_g, fonte_m, fonte_p):
    jogador      = Jogador()
    obstaculos   = []
    score        = 0.0
    velocidade   = VEL_INICIAL
    timer_obs    = 0
    intervalo    = random.randint(80, 140)
    rodando      = True
    # partículas de poeira
    particulas   = []

    # fundo — camadas de "montanhas" paralaxe simples
    nuvens = [(random.randint(0, LARGURA), random.randint(40, 160), random.randint(60, 130))
              for _ in range(6)]

    while rodando:
        clock.tick(FPS)

        # ---- EVENTOS ----
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    jogador.pular()

        # ---- UPDATE ----
        jogador.update()
        velocidade += ACELERACAO
        score      += velocidade * 0.04

        # spawn de obstáculos
        timer_obs += 1
        if timer_obs >= intervalo:
            timer_obs  = 0
            intervalo  = random.randint(55, 130)
            if len(obstaculos) < MAX_OBSTACULOS:
                obstaculos.append(Obstaculo(LARGURA + 20, velocidade))

        for obs in obstaculos:
            obs.update()
        obstaculos = [o for o in obstaculos if not o.fora_da_tela()]

        # partículas de poeira ao correr
        if jogador.no_chao and random.random() < 0.4:
            particulas.append({
                "x": float(jogador.x + 10),
                "y": float(CHAO_Y - 4),
                "vx": random.uniform(-2.5, -0.5),
                "vy": random.uniform(-1.5, 0),
                "vida": random.randint(12, 22)
            })
        for p in particulas:
            p["x"] += p["vx"]; p["y"] += p["vy"]; p["vida"] -= 1
        particulas = [p for p in particulas if p["vida"] > 0]

        # ---- COLISÃO AABB ----
        r_jogador = jogador.rect()
        for obs in obstaculos:
            r_obs = obs.rect()
            # as 4 condições do AABB
            if (r_jogador.right  > r_obs.left  and
                r_jogador.left   < r_obs.right  and
                r_jogador.bottom > r_obs.top    and
                r_jogador.top    < r_obs.bottom):
                rodando = False

        # ---- DRAW ----
        surface.fill(PRETO)

        # céu degradê simples (retas horizontais)
        for i in range(80):
            c = int(10 + i * 1.8)
            pygame.draw.line(surface, (c, c, c + 30), (0, i * 5), (LARGURA, i * 5), 5)

        # nuvens (paralaxe lenta)
        for idx, (nx, ny, nw) in enumerate(nuvens):
            nuvens[idx] = ((nx - 0.3) % (LARGURA + 160) - 160, ny, nw)
            pygame.draw.ellipse(surface, (50, 55, 80), (nx, ny, nw, 28))
            pygame.draw.ellipse(surface, (55, 60, 88), (nx + 18, ny - 12, nw - 30, 28))

        # chão
        pygame.draw.rect(surface, AZUL_MED, (0, CHAO_Y, LARGURA, ALTURA - CHAO_Y))
        pygame.draw.line(surface, CINZA_CLR, (0, CHAO_Y), (LARGURA, CHAO_Y), 2)

        # linhas de velocidade no chão
        for i in range(0, LARGURA, 80):
            offset = int(pygame.time.get_ticks() * velocidade * 0.05) % 80
            lx = (i - offset) % LARGURA
            pygame.draw.line(surface, CINZA,
                             (lx, CHAO_Y + 10), (lx + 30, CHAO_Y + 10), 2)

        # partículas
        for p in particulas:
            alpha = max(0, p["vida"] * 10)
            r = max(1, p["vida"] // 4)
            pygame.draw.circle(surface, CINZA, (int(p["x"]), int(p["y"])), r)

        # obstáculos e jogador
        for obs in obstaculos:
            obs.draw(surface)
        jogador.draw(surface)

        # HUD
        draw_text(surface, f"Score: {int(score)}", fonte_m, AMARELO, 16, 14)
        draw_text(surface, f"Vel: {velocidade:.1f}", fonte_p, CINZA_CLR, 16, 46)
        draw_text(surface, "SPACE = pular", fonte_p, CINZA_CLR, LARGURA - 170, 14)

        # barra de velocidade
        barra_max = 200
        barra_val = min(barra_max, int((velocidade - VEL_INICIAL) / 10 * barra_max))
        pygame.draw.rect(surface, CINZA, (LARGURA - 174, 40, barra_max, 8), border_radius=4)
        pygame.draw.rect(surface, LARANJA, (LARGURA - 174, 40, barra_val, 8), border_radius=4)
        draw_text(surface, "vel", fonte_p, CINZA_CLR, LARGURA - 194, 38)

        pygame.display.flip()

    return int(score)

# ==============================================================
#  MAIN
# ==============================================================
def main():
    pygame.init()
    surface = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Endless Runner — DCExt III")
    clock   = pygame.display.get_surface()
    clock   = pygame.time.Clock()

    fonte_g = pygame.font.SysFont("monospace", 42, bold=True)
    fonte_m = pygame.font.SysFont("monospace", 22, bold=True)
    fonte_p = pygame.font.SysFont("monospace", 16)

    scores  = carregar_scores()

    while True:
        tela_inicial(surface, clock, fonte_g, fonte_m, fonte_p, scores)
        score  = jogar(surface, clock, fonte_g, fonte_m, fonte_p)
        tela_game_over(surface, clock, fonte_g, fonte_m, fonte_p, score, scores)
        scores = carregar_scores()

if __name__ == "__main__":
    main()
