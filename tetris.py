import pygame
import random
import copy
import sys

CELL = 42
H = 15
W = 10
FPS = 30
size = width, height = W * CELL, H * CELL
size2 = 680, 680
screen2 = pygame.display.set_mode(size2)
screen = pygame.Surface(size)

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()

    board = list()
    for y in range(H):
        for x in range(W):
            board.append(pygame.Rect(x * CELL, y * CELL, CELL, CELL))

    pos_figures = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                   [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                   [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                   [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, -1)],
                   [(0, 0), (0, -1), (0, 1), (1, -1)],
                   [(0, 0), (0, -1), (0, 1), (-1, 0)]]

    figures = list()
    for pos_fig in pos_figures:
        figures.append([pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in pos_fig])

    form_fig = pygame.Rect(0, 0, CELL - 2, CELL - 2)

    figure = copy.deepcopy(random.choice(figures))
    figure_next = copy.deepcopy(random.choice(figures))

    background = pygame.image.load('data/fon2.jpg').convert()
    color_score = pygame.Color('#CD8C95')
    color_record = pygame.Color('#473C8B')
    color_instr = pygame.Color('#BCEE68')
    font = pygame.font.Font('data/font.ttf', 40)
    font2 = pygame.font.Font('data/font.ttf', 20)
    font3 = pygame.font.Font('data/font.ttf', 10)
    instr1_view = font2.render('right >', True, color_instr)
    instr2_view = font2.render('left <', True, color_instr)
    instr3_view = font2.render('rotate ^', True, color_instr)
    instr4_view = font2.render('down', True, color_instr)
    instr5_view = font3.render('v', True, color_instr)
    score_view = font.render('score', True, color_score)
    record_view = font.render('record', True, color_record)
    score = 0
    lines = 0
    scores = {0: 0, 1: 10, 2: 20, 3: 30, 4: 40, 5: 50, 6: 60, 7: 70, 8: 80, 9: 90, 10: 100,
              11: 110, 12: 120, 13: 130, 14: 140, 15: 150, 16: 160, 17: 170, 18: 180,
              19: 190, 20: 200}


    def get_records():
        try:
            with open('record') as file:
                return file.readline()
        except FileNotFoundError:
            with open('record', 'w') as file:
                file.write('0')


    def update_records(rec, sc):
        record = max(int(rec), sc)
        with open('record', 'w') as file:
            file.write(str(record))


    sp_figures = list()
    for i in range(H):
        sp_figures.append([0 for j in range(W)])


    def borders():
        if figure[i].x > W - 1 or figure[i].x < 0:
            return False
        elif figure[i].y > H - 1 or sp_figures[figure[i].y][figure[i].x]:
            return False
        return True


    def get_color():
        return (random.randrange(40, 256),
                random.randrange(40, 256), random.randrange(40, 256))


    color = get_color()
    color_next = get_color()
    speed_figs, count, limit = 60, 0, 1800


    def terminate():
        pygame.quit()
        sys.exit()


    def start_screen():
        fon = pygame.image.load('data/fon3.jpg').convert()
        screen2.blit(fon, (0, 0))
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.KEYDOWN or \
                        event.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            clock.tick(FPS)


    start_screen()

    running = True
    while running:
        screen2.blit(background, (0, 0))
        moving = 0
        rotate = False
        screen2.blit(screen, (25, 25))
        screen.fill(pygame.Color('black'))
        rec = get_records()

        # управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # w += 1
                # if w == 1:
                #    start_screen(w)
                if event.key == pygame.K_RIGHT:
                    moving = 1
                elif event.key == pygame.K_LEFT:
                    moving = -1
                elif event.key == pygame.K_DOWN:
                    limit = 100
                elif event.key == pygame.K_UP:
                    rotate = True

        # движение по оси х
        old_figure = copy.deepcopy(figure)
        for i in range(4):
            figure[i].x += moving
            if not borders():
                figure = copy.deepcopy(old_figure)
                pygame.display.flip()
                break

        # движение по оси у
        count += speed_figs
        if count > limit:
            count = 0
            old_figure = copy.deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not borders():
                    for j in range(4):
                        sp_figures[old_figure[j].y][old_figure[j].x] = color
                        figure = figure_next
                        color = color_next
                    figure_next = copy.deepcopy(random.choice(figures))
                    pygame.display.flip()
                    color_next = get_color()
                    limit = 1800
                    break

        # вращение фигуры
        vrazch = figure[0]
        if rotate:
            for i in range(4):
                y = figure[i].x - vrazch.x
                x = figure[i].y - vrazch.y
                figure[i].y = vrazch.y + y
                figure[i].x = vrazch.x - x
                if not borders():
                    figure = copy.deepcopy(old_figure)
                    break

        # проверка линий
        floor = H - 1
        lines = 0
        for i in range(H - 1, -1, -1):
            n = 0
            for j in range(W):
                if sp_figures[i][j]:
                    n += 1
                sp_figures[floor][j] = sp_figures[i][j]
            if n < W:
                floor -= 1
            else:
                lines += 1
        score += scores[lines]

        # размещение надписей
        screen2.blit(score_view, (490, 520))
        screen2.blit(font.render(str(score), True, pygame.Color('#BCEE68')), (545, 570))
        screen2.blit(record_view, (490, 420))
        screen2.blit(font.render(str(rec), True, pygame.Color('#BCEE68')), (545, 470))
        screen2.blit(instr1_view, (450, 20))
        screen2.blit(instr2_view, (570, 20))
        screen2.blit(instr3_view, (450, 55))
        screen2.blit(instr4_view, (570, 55))
        screen2.blit(instr5_view, (650, 67))


        # отрисовка сетки
        for recs in board:
            pygame.draw.rect(screen, (100, 100, 100), recs, 1)

        # отрисовка фигуры
        for i in range(4):
            form_fig.x = figure[i].x * CELL
            form_fig.y = figure[i].y * CELL
            pygame.draw.rect(screen, color, form_fig)

        # отрисовка поля
        for y, row in enumerate(sp_figures):
            for x, col in enumerate(row):
                if col:
                    form_fig.y, form_fig.x = y * CELL, x * CELL
                    pygame.draw.rect(screen, col, form_fig)

        # следующая фигура
        for i in range(4):
            pygame.display.flip()
            form_fig.x = figure_next[i].x * CELL + 360
            form_fig.y = figure_next[i].y * CELL + 180
            pygame.draw.rect(screen2, color_next, form_fig)

        # конец игры
        for i in range(W):
            if sp_figures[0][i]:
                update_records(rec, score)
                pygame.display.flip()
                sp_figures = list()
                for i in range(H):
                    sp_figures.append([0 for j in range(W)])
                speed_figs, count, limit = 60, 0, 1800
                score = 0
                for i_rect in board:
                    pygame.draw.rect(screen, get_color(), i_rect)
                    screen2.blit(screen, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
        pygame.display.flip()
        clock.tick(FPS)
