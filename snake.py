# imports
import sys, subprocess
subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
import pygame, random, time, os, winsound
### 1-1. 게임 사전 설정
# 게임에 대한 기본적인 설정에 대한 변수
# fps 조절 및 fps 카운터
fps = 15
fps_controller = pygame.time.Clock()
fps_increase = 0
# 창 크기
frame = (720, 480)
# 색깔 정의 (Red, Green, Blue)
# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
orange = pygame.Color(255, 127, 0)
yellow = pygame.Color(255, 255, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
navy = pygame.Color(0, 0, 127)
purple = pygame.Color(255, 0, 255)
rainbow = [red, orange, yellow, green, blue, navy, purple]
# Game 관련 변수
score1 = 0
score2 = 0
mode = 0

snake_pos1 = [320, 200]
snake_body1 = [
    [snake_pos1[0], snake_pos1[1]],
    [snake_pos1[0] - 10, snake_pos1[1]],
    [snake_pos1[0] - 20, snake_pos1[1]],
]
snake_color1 = green

if mode == 1:
    snake_pos2 = [-1, -1]
else:
    snake_pos2 = [400, 280]
snake_body2 = [
    [snake_pos2[0], snake_pos2[1]],
    [snake_pos2[0] + 10, snake_pos2[1]],
    [snake_pos2[0] + 20, snake_pos2[1]],
]
snake_color2 = blue

food_pos = [
    random.randrange(1 + 12, (frame[0] // 10) - 14) * 10,
    random.randrange(1, (frame[1] // 10)) * 10,
]
food_spawn = True
direction1 = "RIGHT1"
direction2 = "LEFT2"
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
#게임종료
def quitgame():
  pygame.quit()
    sys.exit()

#기능을 수행하는 버튼
class button:
  def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
      main_window.blit(img_act, (x_act, y_act))
      if click[0] and action != None:
        pygame.delay(1000)
        action()
    else:
      main_window.blit(img_in, (x,y))

def mainmenu():
  menu = True
  while menu:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quitgame()
    main_window.fill(black)

    titletext = main_window.blit(titleImg, (220,150))
    /////////////

# (r, g, b)받아서 뱀 색 변경하는 함수
def snake_color_change(r, g, b, num):
    global snake_color1, snake_color2
    if num == 1:
        snake_color1 = pygame.Color(r, g, b)
    elif num == 2:
        snake_color2 = pygame.Color(r, g, b)
# Score
def show_score(window, size, choice, color, font, fontsize):
    # Score를 띄우기 위한 설정입니다.
    score_font = pygame.font.SysFont(font, fontsize)
    if mode == 1:
        score_surface = score_font.render("Score:" + str(score1), True, color)
        score_rect = score_surface.get_rect()
        # Game over 상황인지 게임중 상황인지에 따라 다른 위치를 선정
        if choice == 1:
            score_rect.midtop = (size[0] / 13, 15)
        else:
            score_rect.midtop = (size[0] / 2, size[1] / 1.25)
        # 설정한 글자를 window에 복사
        window.blit(score_surface, score_rect)
    elif mode == 2:
        score_surface1 = score_font.render(f"Player1:{score1}", True, color)
        score_surface2 = score_font.render(f"Player2:{score2}", True, color)
        score_rect1 = score_surface1.get_rect()
        score_rect2 = score_surface2.get_rect()
        if choice == 1:
            score_rect1.midtop = (size[0] / 13, 10)
            score_rect2.midtop = (size[0] / 13, 26)
        else:
            score_rect1.center = (size[0] / 2, size[1] / 1.3)
            score_rect2.center = (size[0] / 2, size[1] / 1.2)
        window.blit(score_surface1, score_rect1)
        window.blit(score_surface2, score_rect2)
# Game Over
def game_over(window, size):
    win = 0
    if out1 == out2:
        if out1 == 0:
            win = 0
        else:
            win = 3
    elif out1 == 0:
        win = 1
    else:
        win = 2
    # 'Game Over'문구를 띄우기 위한 설정입니다.
    my_font = pygame.font.SysFont("times new roman", 90)
    if win == 0:
        game_over_surface = my_font.render("Game Over", True, red)
    elif win == 3:
        game_over_surface = my_font.render("Draw!", True, red)
    else:
        game_over_surface = my_font.render(f"Player{win} Wins!", True, red)
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
    quitgame()

# Keyboard input
def get_keyboard1(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    if direction1 != "DOWN1" and key == pygame.K_UP:
        return "UP1"
    if direction1 != "UP1" and key == pygame.K_DOWN:
        return "DOWN1"
    if direction1 != "RIGHT1" and key == pygame.K_LEFT:
        return "LEFT1"
    if direction1 != "LEFT1" and key == pygame.K_RIGHT:
        return "RIGHT1"
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    return cur_dir
def get_keyboard2(key, cur_dir):
    # WASD, 방향키를 입력 받으면 해당 방향으로 이동합니다.
    # 방향이 반대방향이면 무시합니다.
    if direction2 != "DOWN2" and key == ord("w"):
        return "UP2"
    if direction2 != "UP2" and key == ord("s"):
        return "DOWN2"
    if direction2 != "RIGHT2" and key == ord("a"):
        return "LEFT2"
    if direction2 != "LEFT2" and key == ord("d"):
        return "RIGHT2"
    # 모두 해당하지 않다면 원래 방향을 돌려줍니다.
    return cur_dir
# Game이 동작하기 위한 메인 코드
# 초기화합니다.
# Initialize
main_window = Init(frame)
# 반짝거리는 무지개 뱀
# rainbow_idx = 0
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
                direction1 = get_keyboard1(event.key, direction1)
                direction2 = get_keyboard2(event.key, direction2)
    # 승자가리는 변수 지정
    out1 = out2 = 0
    # 실제로 뱀의 위치를 옮깁니다.
    if direction1 == "UP1":
        snake_pos1[1] -= 10
    if direction1 == "DOWN1":
        snake_pos1[1] += 10
    if direction1 == "LEFT1":
        snake_pos1[0] -= 10
    if direction1 == "RIGHT1":
        snake_pos1[0] += 10
    if mode == 2:
        if direction2 == "UP2":
            snake_pos2[1] -= 10
        if direction2 == "DOWN2":
            snake_pos2[1] += 10
        if direction2 == "LEFT2":
            snake_pos2[0] -= 10
        if direction2 == "RIGHT2":
            snake_pos2[0] += 10
    # 우선 증가시키고 음식의 위치가 아니라면 마지막을 뺍니다.
    snake_body1.insert(0, list(snake_pos1))
    if snake_pos1[0] == food_pos[0] and snake_pos1[1] == food_pos[1]:
        score1 += 1
        # 스코어 3점 오를때마다 속도 증가함
        if fps_increase == 3:
            fps += 1
            fps_increase %= 3
        else:
            fps_increase += 1
        food_spawn = False
        snake_color_change(
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256),
            num=1,
        )
    else:
        snake_body1.pop()
    snake_body2.insert(0, list(snake_pos2))
    if snake_pos2[0] == food_pos[0] and snake_pos2[1] == food_pos[1]:
        score2 += 1
        # 스코어 3점 오를때마다 속도 증가함
        if fps_increase == 3:
            fps += 1
            fps_increase %= 3
        else:
            fps_increase += 1
        food_spawn = False
        snake_color_change(
            random.randrange(0, 256),
            random.randrange(0, 256),
            random.randrange(0, 256),
            num=2,
        )
    else:
        snake_body2.pop()
    # 음식이 없다면 음식을 랜덤한 위치에 생성합니다.
    if not food_spawn:
        # 임시로 음식 먹을때마다 색 바뀌게 만들었음
        while food_spawn == False:
            food_spawn = True
            food_pos = [
                random.randrange(1 + 12, (frame[0] // 10) - 14) * 10,
                random.randrange(1, (frame[1] // 10)) * 10,
            ]
            # 만약 음식 생성 위치에 장애물이 있다면 다른곳에 음식을 생성함
            for obstacle in obstacle_pos:
                if food_pos == obstacle:
                    food_spawn = False
                    break
        # 장애물
        for obstacle in obstacle_pos:
            if snake_pos1[0] == obstacle[0] and snake_pos1[1] == obstacle[1]:
                game_over(main_window, frame)
    elif mode == 2:
        # 바깥 벽
        if snake_pos1[0] < 0 + 120 or snake_pos1[0] > frame[0] - 10 - 120:
            out1 = 1
            game_over(main_window, frame)
        if snake_pos1[1] < 0 or snake_pos1[1] > frame[1] - 10:
            out1 = 1
            game_over(main_window, frame)
        if snake_pos2[0] < 0 + 120 or snake_pos2[0] > frame[0] - 10 - 120:
            out2 = 1
            game_over(main_window, frame)
        if snake_pos2[1] < 0 or snake_pos2[1] > frame[1] - 10:
            out2 = 1
            game_over(main_window, frame)

        # 뱀끼리의 몸 충돌
        for block in snake_body1[1:]:
            if snake_pos1[0] == block[0] and snake_pos1[1] == block[1]:
                out1 = 1
                game_over(main_window, frame)
            if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
                out2 = 1
                game_over(main_window, frame)

        for block in snake_body2[1:]:
            if snake_pos1[0] == block[0] and snake_pos1[1] == block[1]:
                out1 = 1
                game_over(main_window, frame)
            if snake_pos2[0] == block[0] and snake_pos2[1] == block[1]:
                out2 = 1
                game_over(main_window, frame)
        # 장애물과의 충돌
        for obstacle in obstacle_pos:
            if snake_pos1[0] == obstacle[0] and snake_pos1[1] == obstacle[1]:
                out1 = 1
                game_over(main_window, frame)
            if snake_pos2[0] == obstacle[0] and snake_pos2[1] == obstacle[1]:
                out2 = 1
                game_over(main_window, frame)
    # 점수를 띄워줍니다.
    show_score(main_window, frame, 1, white, "consolas", 20)
    pygame.display.update()
    # 해당 FPS만큼 대기
    fps_controller.tick(fps)
