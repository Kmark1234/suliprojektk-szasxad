import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Autós Játék(Lénárd,Kovács,Bunder)")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Error loading image: {image_path} - {e}")
        return None

opening_image = load_image("opening_image.png")
menu_image = load_image("menu_image.png")
start_button_image = load_image("start_button.png")
car_skins = [
    load_image("car_skin1.png"),
    load_image("car_skin2.png"),
    load_image("car_skin3.png"),
    load_image("car_skin4.png")
]
background = load_image("freepik__retouch__1347.png")

if background:
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

start_button_image = pygame.transform.scale(start_button_image, (400, 300))
car_skins = [pygame.transform.scale(skin, (200, 100)) for skin in car_skins]

car_width, car_height = 5, 5

result_image = None

def show_opening_image():
    screen.blit(opening_image, (0, 0))
    pygame.display.flip()
    pygame.time.wait(600)

def show_menu():
    selected_car = 0
    while True:
        screen.blit(menu_image, (0, 0))

        start_button_rect = screen.blit(start_button_image, (
            (WIDTH // 2) - (start_button_image.get_width() // 2),
            (HEIGHT // 2) - (start_button_image.get_height() // 2)
        ))
        car_rects = []
        for i, car_skin in enumerate(car_skins):
            x = WIDTH // 5 * (i + 1) - 50
            y = HEIGHT - 150
            rect = screen.blit(car_skin, (x, y))
            car_rects.append(rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    return selected_car
                for i, rect in enumerate(car_rects):
                    if rect.collidepoint(event.pos):
                        selected_car = i

        for i, rect in enumerate(car_rects):
            if i == selected_car:
                pygame.draw.rect(screen, WHITE, rect.inflate(10, 10), 3)

        pygame.display.flip()

def run_game(selected_car):
    car_image = pygame.transform.scale(car_skins[selected_car], (50, 50))
    car_x, car_y = 250, 800
    car_speed = 10

    map_borders = [
        pygame.Rect(0, 28, 1200, 100),
        pygame.Rect(0, 0, 100, 1000),
        pygame.Rect(1045, 0, 100, 1000),
        pygame.Rect(0, 870, 1200, 100),
        pygame.Rect(170, 230, 55, 250),
        pygame.Rect(170, 440, 600, 340),
        pygame.Rect(430, 225, 170, 340),
        pygame.Rect(780, 680, 180, 100),
        pygame.Rect(300, 95, 58, 250),
        pygame.Rect(960, 300, 90, 250),
        pygame.Rect(690, 125, 300, 100),
        pygame.Rect(690, 125, 300, 100),
        "1.baloldaltol kezdodo 2. a képernyö tetejétöl kezdodo
        3.szélesség 4. magasság"
    ]

    start_rect = pygame.Rect(250, 800, 50, 50)
    finish_rect = pygame.Rect(500, 150, 50, 50)


    font = pygame.font.SysFont(None, start_rect.width // 4)
    start_text_surface = font.render("START", True, (0, 0, 0))
    start_text_rect = start_text_surface.get_rect(center=start_rect.center)

    font = pygame.font.SysFont(None, finish_rect.width // 4)
    finish_text_surface = font.render("FINISH", True, (0, 0, 0))
    finish_text_rect = finish_text_surface.get_rect(center=finish_rect.center)

    win_image = load_image("plus.png")
    lose_image = load_image("minus.png")
    win_image = pygame.transform.scale(win_image, (200, 100)) if win_image else None
    lose_image = pygame.transform.scale(lose_image, (200, 100)) if lose_image else None

    clock = pygame.time.Clock()
    running = True
    result_image = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            car_y -= car_speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            car_y += car_speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            car_x -= car_speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            car_x += car_speed

        car_rect = pygame.Rect(car_x, car_y, 50, 50)
        hit_border = any(car_rect.colliderect(border) for border in map_borders)

        if hit_border:
            print("Játék vége! Leértél az útról.")
            result_image = lose_image
            running = False

        if car_rect.colliderect(finish_rect):
            print("Győzelem! Végigértél a pályán!")
            result_image = win_image
            running = False

        if result_image is None:
            screen.fill((0, 0, 0))
            screen.blit(background, (0, 0))

            pygame.draw.rect(screen, WHITE, start_rect)
            screen.blit(start_text_surface, start_text_rect)

            pygame.draw.rect(screen, WHITE, finish_rect)
            screen.blit(finish_text_surface, finish_text_rect)


            for border in map_borders:
                pygame.draw.rect(screen, (255, 0, 0), border, 2)
            screen.blit(car_image, (car_x, car_y))

        pygame.display.flip()
        clock.tick(30)

        if result_image:
            screen.fill((0, 0, 0))
            if result_image:
                screen.blit(result_image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000)

if __name__ == "__main__":
    show_opening_image()
    selected_car = show_menu()
    run_game(selected_car)
    pygame.quit()
    sys.exit()
