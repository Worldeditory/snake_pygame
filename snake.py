# imports
import sys, subprocess

subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])

import pygame, random, time

### 1-1. 게임 사전 설정
# 게임에 대한 기본적인 설정에 대한 변수

# fps 조절 및 fps 카운터
fps = 15
fps_controller = pygame.time.Clock()

# 창 크기
frame = (720, 480)

# 색깔 정의 (Red, Green, Blue)
# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Game 관련 변수
snake_pos = [100, 50]
snake_body = [[100, 50], [100 - 10, 50], [100 - (2 * 10), 50]]

food_pos = [
    random.randrange(1, (frame[0] // 10)) * 10,
    random.randrange(1, (frame[1] // 10)) * 10,
]
food_spawn = True

direction = "RIGHT"

score = 0

obstacle_pos = []

# 장애물 생성할 때 임시로 사용할 변수
obstacle_x = 0
obstacle_y = 0

### 1-2. Pygame 초기화
# Pygame을 사용하기 위해 창 크기, 제목 등을 주어 초기화를 해줍니다.


def Init(size):
    # 초기화 후 error 확인
    check_errors = (
        pygame.init()
    )  # pygame.init() example output -> (6, 0) / 두번째 항목이 error의 수를 알려줌

    if check_errors[1] > 0:
        print(f"[!] Had {check_errors[1]} errors when initialising game, exiting...")
        sys.exit(-1)
    else:
        print("[+] Game successfully initialised")

    # pygame.display로 제목, window size를 설정하고 초기화
    pygame.display.set_caption("Snake Example with PyGame")
    game_window = pygame.display.set_mode(size)
    return game_window


### 1-3. 기본 logic 함수 모음
# 게임을 플레이하기 위해 필요한 함수들의 모음


# Score
def show_score(window, size, choice, color, font, fontsize):
    # Score를 띄우기 위한 설정입니다.
    score_font = pygame.font.SysFont(font, fontsize)
    score_surface = score_font.render("Score : " + str(score), True, color)
    score_rect = score_surface.get_rect()

    # Game over 상황인지 게임중 상황인지에 따라 다른 위치를 선정합니다.
    if choice == 1:
        score_rect.midtop = (size[0] / 10, 15)
    else:
        score_rect.midtop = (size[0] / 2, size[1] / 1.25)

    # 설정한 글자를 window에 복사합니다.
    window.blit(score_surface, score_rect)


# Game Over
def game_over(window, size):
    # 'Game Over'문구를 띄우기 위한 설정입니다.
    my_font = pygame.font.SysFont("times new roman", 90)
    game_over_surface = my_font.render("Game Over", True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (size[0] / 2, size[1] / 4)

    # window를 검은색으로 칠하고 설정했던 글자를 window에 복사합니다.
    window.fill(black)
    window.blit(game_over_surface, game_over_rect)

    # 'show_score' 함수를 부릅니다.
    show_score(window, size, 0, green, "times", 20)

    # 그려진 화면을 실제로 띄워줍니다.
    pygame.display.flip()

    # 3초 기다린 후 게임을 종료합니다.
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Keyboard input
def get_keyboard(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    if direction != "DOWN" and key == pygame.K_UP or key == ord("w"):
        return "UP"
    if direction != "UP" and key == pygame.K_DOWN or key == ord("s"):
        return "DOWN"
    if direction != "RIGHT" and key == pygame.K_LEFT or key == ord("a"):
        return "LEFT"
    if direction != "LEFT" and key == pygame.K_RIGHT or key == ord("d"):
        return "RIGHT"
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    return cur_dir


# Game이 동작하기 위한 메인 코드


# 초기화합니다.
# Initialize
main_window = Init(frame)

while True:
    # 게임에서 event를 받아옵니다.
    for event in pygame.event.get():
        # 종료시 실제로 프로그램을 종료합니다.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # esc 키를 눌렀을떄 종료 신호를 보냅니다.
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            else:
                # 입력 키로 방향을 얻어냅니다.
                direction = get_keyboard(event.key, direction)

    # 실제로 뱀의 위치를 옮깁니다.
    if direction == "UP":
        snake_pos[1] -= 10
    if direction == "DOWN":
        snake_pos[1] += 10
    if direction == "LEFT":
        snake_pos[0] -= 10
    if direction == "RIGHT":
        snake_pos[0] += 10

    # 우선 증가시키고 음식의 위치가 아니라면 마지막을 뺍니다.
    snake_body.insert(0, list(snake_pos))
    if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    # 음식이 없다면 음식을 랜덤한 위치에 생성합니다.
    if not food_spawn:
        while food_spawn == False:
            food_spawn = True
            food_pos = [
                random.randrange(1, (frame[0] // 10)) * 10,
                random.randrange(1, (frame[1] // 10)) * 10,
            ]
            # 만약 음식 생성 위치에 장애물이 있다면 다른곳에 음식을 생성함
            for obstacle in obstacle_pos:
                if food_pos == obstacle:
                    food_spawn = False
                    break

        # 장애물을 생성함
        while 1:
            obstacle_x = random.randrange(1, (frame[0] // 10)) * 10
            obstacle_y = random.randrange(1, (frame[1] // 10)) * 10
            if [obstacle_x, obstacle_y] != food_pos:
                obstacle_pos.append([obstacle_x, obstacle_y])
                break

    # 우선 게임을 검은 색으로 채우고 뱀의 각 위치마다 그림을 그립니다.
    main_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(main_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # 음식을 그립니다.
    pygame.draw.rect(main_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    # 장애물을 그립니다
    for obstacle in obstacle_pos:
        pygame.draw.rect(
            main_window, red, pygame.Rect(obstacle[0], obstacle[1], 10, 10)
        )

    # Game Over 상태를 확인합니다.

    # 바깥 벽 충돌
    if snake_pos[0] < 0 or snake_pos[0] > frame[0] - 10:
        game_over(main_window, frame)
    if snake_pos[1] < 0 or snake_pos[1] > frame[1] - 10:
        game_over(main_window, frame)

    # 뱀의 몸 충돌
    for block in snake_body[1:]:
        if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
            game_over(main_window, frame)

    # 점수를 띄우고 보이게 업데이트
    for obstacle in obstacle_pos:
        if snake_pos[0] == obstacle[0] and snake_pos[1] == obstacle[1]:
            game_over(main_window, frame)

    # 점수를 띄워줍니다.
    show_score(main_window, frame, 1, white, "consolas", 20)

    pygame.display.update()

    # 해당 FPS만큼 대기
    fps_controller.tick(fps)
