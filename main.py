import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menangkap Telur")

# Inisialisasi mixer untuk memutar lagu
pygame.mixer.init()

# Warna
white = (255, 255, 255)


# Kelas untuk telur
class Egg:
    def __init__(self):
        self.image = pygame.image.load("assets/egg.png")  # Gambar telur
        self.rect = self.image.get_rect()  # Mendapatkan rect dari gambar
        self.reset()

    def fall(self):
        self.rect.y += 5  # Kecepatan jatuh

    def reset(self):
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = 0

    def get_hitbox(self):
        # Mengurangi ukuran hitbox telur
        return self.rect.inflate(-100, -100)  # Mengurangi lebar dan tinggi hitbox


# Kelas untuk keranjang
class Basket:
    def __init__(self):
        self.image = pygame.image.load("assets/basket.png")  # Gambar keranjang
        self.rect = self.image.get_rect()  # Mendapatkan rect dari gambar
        self.rect.y = screen_height - self.rect.height  # Posisi keranjang di bawah

    def move(self, direction):
        if direction == "left" and self.rect.x > 0:
            self.rect.x -= 10
        elif direction == "right" and self.rect.x < screen_width - self.rect.width:
            self.rect.x += 10

    def get_hitbox(self):
        # Mengurangi ukuran hitbox keranjang
        return self.rect.inflate(-10, -30)  # Mengurangi lebar dan tinggi hitbox


# Fungsi untuk memutar lagu secara loop / berulang ulang
def play_music():
    pygame.mixer.music.load("sounds/Sketchbook 2024-03-30_01_L01.ogg")
    pygame.mixer.music.play(loops=-1)


catch_egg = pygame.mixer.Sound("sounds/catch.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")


def sound_effect(type: str):
    if type == "miss":
        miss_sound.play()
    elif type == "catch":
        catch_egg.play()


# Fungsi utama
def main():
    clock = pygame.time.Clock()
    basket = Basket()
    egg = Egg()
    score = 0
    running = True
    play_music()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            basket.move("left")
        if keys[pygame.K_RIGHT]:
            basket.move("right")

        egg.fall()

        # Deteksi tabrakan menggunakan hitbox yang lebih kecil
        if egg.get_hitbox().colliderect(basket.get_hitbox()):
            score += 1
            egg.reset()  # Reset telur jika ditangkap
            sound_effect("catch")

        # Reset telur jika jatuh di bawah layar
        if egg.rect.y > screen_height:
            egg.reset()
            sound_effect("miss")

        # Menggambar objek
        screen.fill(white)
        screen.blit(egg.image, (egg.rect.x, egg.rect.y))
        screen.blit(basket.image, (basket.rect.x, basket.rect.y))

        pygame.display.flip()

        clock.tick(30)

    pygame.mixer.music.stop()
    pygame.quit()


if __name__ == "__main__":
    main()
