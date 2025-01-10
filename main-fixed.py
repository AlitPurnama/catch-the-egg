import pygame
import random
import math

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Simulasi Game Berbasis Vektor")
pygame.mixer.init()

# Warna
white = (255, 255, 255)
black = (0, 0, 0)


# Fungsi menghitung magnitudo vektor
def magnitude(vector):
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)


# Fungsi normalisasi vektor
def normalize(vector):
    mag = magnitude(vector)
    if mag == 0:
        return (0, 0)
    return (vector[0] / mag, vector[1] / mag)


def play_music():
    pygame.mixer.music.load("sounds/Sketchbook 2024-03-30_01_L01.ogg")
    pygame.mixer.music.play(loops=-1)


def stop_music():
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()


catch_egg = pygame.mixer.Sound("sounds/catch.wav")
miss_sound = pygame.mixer.Sound("sounds/miss.wav")


def sound_effect(type: str):
    if type == "miss":
        miss_sound.play()
    elif type == "catch":
        catch_egg.play()


# Kelas untuk telur
class Egg:
    def __init__(self):
        self.image = pygame.image.load("assets/egg.png")  # Gambar telur
        self.rect = self.image.get_rect()  # Mendapatkan rect dari gambar
        self.speed = 5  # Kecepatan tetap
        self.direction = normalize((random.uniform(-1, 1), 1))  # Arah diagonal acak
        self.reset()

    def fall(self):
        # Perhitungan posisi baru dengan metode move_ip
        self.rect.move_ip(
            self.direction[0] * self.speed, self.direction[1] * self.speed
        )

    def reset(self):
        self.rect.topleft = (random.randint(0, screen_width - self.rect.width), 0)
        self.direction = normalize(
            (random.uniform(-1, 1), 1)
        )  # Reset arah diagonal acak

    def get_hitbox(self):
        # Mengurangi ukuran hitbox telur
        return self.rect.inflate(-100, -100)  # Mengurangi lebar dan tinggi hitbox


# Kelas untuk keranjang
class Basket:
    def __init__(self):
        self.image = pygame.image.load("assets/basket.png")  # Gambar keranjang
        self.rect = self.image.get_rect()  # Mendapatkan rect dari gambar
        self.rect.y = screen_height - self.rect.height  # Posisi keranjang di bawah
        self.speed = 10  # Kecepatan tetap

    def move(self, direction):
        if direction == "left" and self.rect.x > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.x < screen_width - self.rect.width:
            self.rect.x += self.speed

    def get_hitbox(self):
        # Mengurangi ukuran hitbox keranjang
        return self.rect.inflate(-10, -30)  # Mengurangi lebar dan tinggi hitbox


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
            sound_effect("catch")
            egg.reset()  # Reset telur jika ditangkap

        # Reset telur jika jatuh di bawah layar atau keluar dari batas horizontal
        if egg.rect.y > screen_height or egg.rect.x < 0 or egg.rect.x > screen_width:
            sound_effect("miss")
            egg.reset()

        # Menggambar objek
        screen.fill(white)
        screen.blit(egg.image, (egg.rect.x, egg.rect.y))
        screen.blit(basket.image, (basket.rect.x, basket.rect.y))

        # Menampilkan skor
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, black)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    stop_music()
    pygame.quit()


if __name__ == "__main__":
    main()
