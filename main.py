import pygame
import random


# 'Земля' на экране
def land_in_g():
    screen.blit(land, (l_x, 600))
    screen.blit(land, (l_x + 504, 600))


# Создание самих 2 труб (верхней и нижней)
def cr_tubes():
    tube_pos = random.randrange(300, 550)
    down = tube_s.get_rect(midtop=(500, tube_pos))
    top = tube_s.get_rect(midbottom=(500, tube_pos - 250))
    return down, top


# Движение труб
def mv_tubes(tubes):
    for i in tubes:
        i.centerx -= 3
    visible_tubes = [j for j in tubes if j.right > -50]
    return visible_tubes


# Трубы на экране
def tubes_in_g(tubes):
    for i in tubes:
        if i.bottom >= 768:
            screen.blit(tube_s, i)
        else:
            flip_tube = pygame.transform.flip(tube_s, False, True)
            screen.blit(flip_tube, i)


# Проверка столкновений или на выход за границы
def checking(tubes):
    global scoring
    for i in tubes:
        if bird_rect.colliderect(i):
            hit_sound.play()
            scoring = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 600:
        scoring = True
        return False

    return True


# Анимация птички
def bird_anim():
    bird_change = bird_frames[bird_ind]
    bird_change_rect = bird_change.get_rect(center=(100, bird_rect.centery))
    return bird_change, bird_change_rect


# Количество баллов
def scores(game_state):
    if game_state == 'main_game':
        score_in_g = game_font.render(str(int(score)), True, color)
        score_rect = score_in_g.get_rect(center=(216, 100))
        screen.blit(score_in_g, score_rect)
    if game_state == 'game_over':
        score_in_g = game_font.render(f'Score: {int(score)}', True, color)
        score_rect = score_in_g.get_rect(center=(216, 100))
        screen.blit(score_in_g, score_rect)

        high_score_in_g = game_font.render(f'High score: {int(high_score)}', True, color)
        high_score_rect = high_score_in_g.get_rect(center=(216, 50))
        screen.blit(high_score_in_g, high_score_rect)


# Обновление рекорда
def updt_score(sc, h_sc):
    if sc > h_sc:
        h_sc = sc
    return h_sc


# Проверка на набор баллов
def tube_score_check():
    global score, scoring

    if spis_of_tubes:
        for i in spis_of_tubes:
            if 95 < i.centerx < 105 and scoring:
                score += 1
                score_sound.play()
                scoring = False
            if i.centerx < 0:
                scoring = True


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((432, 768))
    clock = pygame.time.Clock()
    game_font = pygame.font.Font('Font.ttf', 40)
    pygame.display.set_caption('Flappy Bird')
    icon = pygame.image.load('icon.jpg')
    pygame.display.set_icon(icon)

    background = pygame.image.load('background-day.png').convert()
    background = pygame.transform.scale(background, (432, 768))

    land = pygame.image.load('base.png').convert()
    land = pygame.transform.scale(land, (504, 168))
    l_x = 0

    running = True

    bird_fall = 0.25
    bird_mv = 0
    bird_1 = pygame.image.load('yellowbird-1.png').convert_alpha()
    bird_1 = pygame.transform.scale(bird_1, (51, 36))

    bird_2 = pygame.image.load('yellowbird-2.png').convert_alpha()
    bird_2 = pygame.transform.scale(bird_2, (51, 36))

    bird_3 = pygame.image.load('yellowbird-3.png').convert_alpha()
    bird_3 = pygame.transform.scale(bird_3, (51, 36))

    bird_frames = [bird_1, bird_2, bird_3]
    bird_ind = 0
    bird_surface = bird_frames[bird_ind]
    bird_rect = bird_surface.get_rect(center=(100, 412))

    active = False
    score = 0
    high_score = 0
    scoring = True

    tube_s = pygame.image.load('tube-green.png')
    tube_s = pygame.transform.scale(tube_s, (78, 480))
    spis_of_tubes = []

    pygame.time.set_timer(pygame.USEREVENT, 1200)

    game_over = pygame.image.load('message.png').convert_alpha()
    game_over = pygame.transform.scale(game_over, (276, 461))
    game_over_rect = game_over.get_rect(center=(216, 360))
    color = pygame.Color('white')

    flap_sound = pygame.mixer.Sound('flap_sound.wav')
    hit_sound = pygame.mixer.Sound('hit_sound.wav')
    score_sound = pygame.mixer.Sound('score_sound.wav')
    score_sound_countdown = 100

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Если нажата кнопка и игра идет (то есть мы играем)
                if event.key == pygame.K_SPACE and active:
                    bird_mv = 0
                    bird_mv -= 7
                    flap_sound.play()

                # Если нажата кнопка и игра не идет (то есть мы начинаем заново)
                if event.key == pygame.K_SPACE and not active:
                    active = True
                    spis_of_tubes.clear()
                    bird_rect.center = (100, 300)
                    bird_mv = 0
                    score = 0

            # Если игра идет
            if event.type == pygame.USEREVENT:
                spis_of_tubes.extend(cr_tubes())

                if bird_ind < 2:
                    bird_ind += 1
                else:
                    bird_ind = 0

                bird_surface, bird_rect = bird_anim()

        screen.blit(background, (0, 0))

        # Если птичка не упала или не врезалась
        if active:
            bird_mv += bird_fall
            bird_rect.centery += bird_mv
            screen.blit(bird_surface, bird_rect)
            active = checking(spis_of_tubes)

            spis_of_tubes = mv_tubes(spis_of_tubes)
            tubes_in_g(spis_of_tubes)

            tube_score_check()
            scores('main_game')
        # Иначе
        else:
            screen.blit(game_over, game_over_rect)
            high_score = updt_score(score, high_score)
            scores('game_over')

        # Движение 'земли'
        l_x -= 1
        land_in_g()
        if l_x <= -504:
            l_x = 0

        pygame.display.flip()
        clock.tick(120)
    pygame.quit()