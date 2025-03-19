import pygame
import random
import sys

# เริ่มต้น pygame
pygame.init()

# ตั้งค่าหน้าจอ
WIDTH, HEIGHT = 800, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BIRD KUM SI WOW")

# โหลดไฟล์เสียง
score_sound = pygame.mixer.Sound('Background/SOUND/SCORE.mp3')
hit_sound = pygame.mixer.Sound('Background/SOUND/DEATH.mp3')
jump_sound = pygame.mixer.Sound('Background/SOUND/Cartoon Jump Sound Effect.mp3')
game_over_sounds = [
    pygame.mixer.Sound('Background/SOUND/To Be Continued.mp3'),
    pygame.mixer.Sound('Background/SOUND/AUNInwza007.mp3'),  # เสียง Game Over อื่นๆ
    pygame.mixer.Sound('Background/SOUND/AUN1.mp3')
]  # เพิ่มเสียง Game Over เพิ่มเติมในลิสต์

# ปรับระดับเสียงของแต่ละเสียง
score_sound.set_volume(0.020)  # ปรับเสียงของ SCORE
hit_sound.set_volume(0.4)    # ปรับเสียงของ HIT
jump_sound.set_volume(0.020)   # ปรับเสียงของ JUMP
for sound in game_over_sounds:
    sound.set_volume(0.7)  # ปรับเสียง Game Over

# เพลงพื้นหลัง
pygame.mixer.music.load('Background/SOUND/We are.mp3')  # ใส่ไฟล์เพลงที่ต้องการ
pygame.mixer.music.set_volume(0.29)  # ปรับระดับเสียงเพลงพื้นหลัง

# โหลดภาพพื้นหลัง
background = pygame.image.load('Background/SKY.jpg')
background = pygame.transform.scale(background, (800, 650))

# โหลดภาพนก
bird_img = pygame.image.load('Background/Fighter.png')
bird_img = pygame.transform.scale(bird_img, (90, 50))

# โหลดภาพท่อ
pipe_img = pygame.image.load('Background/pipe.png')
pipe_width = 100
pipe_img = pygame.transform.scale(pipe_img, (pipe_width, HEIGHT))
pipe_img_flipped = pygame.transform.flip(pipe_img, False, True)

# สี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
NEON_GREEN = (57, 255, 20)
NEON_BLUE = (0, 160, 255)

# ตัวแปรของเกม
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10
score = 0
high_score = 0
last_score = 0  # เก็บคะแนนล่าสุดก่อนตาย

pipe_gap = 200
pipe_velocity = 4

# ฟอนต์แสดงคะแนน
font = pygame.font.SysFont("Arial", 25)
game_over_font = pygame.font.SysFont("Arial", 64)

# ตัวจับเวลา
clock = pygame.time.Clock()

def draw_bird(x, y):
    screen.blit(bird_img, (x, y))

def create_pipe():
    height = random.randint(100, HEIGHT - pipe_gap - 100)
    top_pipe = pygame.Rect(WIDTH, 0, pipe_width, height)
    bottom_pipe = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe[0].x -= pipe_velocity
        pipe[1].x -= pipe_velocity

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_img_flipped, (pipe[0].x, pipe[0].bottom - HEIGHT))
        screen.blit(pipe_img, (pipe[1].x, pipe[1].top))

def reset_game():
    global bird_y, bird_velocity, score
    bird_y = HEIGHT // 2
    bird_velocity = 0
    score = 0
    return [create_pipe()]

def show_game_over():
    screen.blit(background, (0, 0))

    game_over_text = game_over_font.render("GAME OVER", True, NEON_BLUE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 5))

    score_box = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 3, 100, 130)
    pygame.draw.rect(screen, WHITE, score_box, border_radius=10)
    pygame.draw.rect(screen, BLACK, score_box, 2)

    score_text = font.render("SCORE", True, RED)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 3 + 10))

    score_value = font.render(str(last_score), True, BLACK)
    screen.blit(score_value, (WIDTH // 2 - score_value.get_width() // 2, HEIGHT // 3 + 40))

    best_text = font.render("BEST", True, RED)
    screen.blit(best_text, (WIDTH // 2 - best_text.get_width() // 2, HEIGHT // 3 + 70))

    best_value = font.render(str(high_score), True, BLACK)
    screen.blit(best_value, (WIDTH // 2 - best_value.get_width() // 2, HEIGHT // 3 + 100))

    retry_text = font.render("Press R to Restart", True, NEON_GREEN)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2 + 50))

    quit_text = font.render("Press Q to Quit", True, NEON_BLUE)
    screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 90))

    pygame.display.flip()

def game_loop():
    global bird_y, bird_velocity, score, high_score, last_score

    pipes = reset_game()
    run_game = True

    # เริ่มเพลงพื้นหลังเมื่อเริ่มเกม
    pygame.mixer.music.load('Background/SOUND/We are.mp3')  # เปลี่ยนเป็นเพลงที่ต้องการ
    pygame.mixer.music.play(-1, 0.0)  # เริ่มเพลงซ้ำ

    while run_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
                    jump_sound.play()
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

        bird_velocity += gravity
        bird_y += bird_velocity

        if bird_y <= 0:
            bird_y = 0
            bird_velocity = 0
        if bird_y >= HEIGHT - bird_img.get_height():
            bird_y = HEIGHT - bird_img.get_height()
            bird_velocity = 0

        move_pipes(pipes)
        if pipes[0][0].x < -pipe_width:
            pipes.pop(0)
            pipes.append(create_pipe())
            score += 1
            score_sound.play()

        bird_rect = pygame.Rect(bird_x, bird_y, bird_img.get_width(), bird_img.get_height())
        for pipe in pipes:
            if pipe[0].colliderect(bird_rect) or pipe[1].colliderect(bird_rect):
                last_score = score
                if score > high_score:
                    high_score = score

                # เลือกเสียง Game Over แบบสุ่ม
                random_game_over_sound = random.choice(game_over_sounds)
                random_game_over_sound.play()
                # ตรวจสอบว่าเสียง Game Over ที่สุ่มขึ้นมาเล่นเสร็จแล้วหรือยัง
                if not pygame.mixer.get_busy():
                    random_game_over_sound.play()  # เล่นเสียงเกมโอเวอร์

                show_game_over()

                waiting = True
                pygame.mixer.music.stop()  # หยุดเพลงเมื่อเกมจบ

                while waiting:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                pygame.mixer.stop()  # หยุดเสียงทั้งหมดก่อนเริ่มใหม่
                                random_game_over_sound.stop()  # หยุดเสียง Game Over
                                pygame.mixer.music.play(-1, 0.0)  # เล่นเพลงพื้นหลังใหม่หลังจากรีเซ็ต
                                pipes = reset_game()
                                score = 0
                                waiting = False

                            elif event.key == pygame.K_q:
                                pygame.quit()
                                sys.exit()

        screen.blit(background, (0, 0))
        draw_bird(bird_x, bird_y)
        draw_pipes(pipes)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        pygame.display.update()
        clock.tick(60)

game_loop()
