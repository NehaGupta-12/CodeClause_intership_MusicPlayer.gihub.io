import pygame
import os
from mutagen.mp3 import MP3

# initialize Pygame
pygame.init()

# set the width and height of the window (adjust as needed)
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# create the Pygame window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Music Player")

# set the path to the directory containing your music files
MUSIC_DIRECTORY = r"C:\Users\neha\Desktop\musiclist"

# store the list of music files
music_files = []

# load music files from the directory
for file in os.listdir(MUSIC_DIRECTORY):
    if file.endswith(".mp3"):
        music_files.append(os.path.join(MUSIC_DIRECTORY, file))

# initialize the current music index
current_music_index = 0

# load button images
play_image = pygame.image.load("play.jpg")
pause_image = pygame.image.load("pause.jpg")
previous_image = pygame.image.load("previous.jpg")
next_image = pygame.image.load("next.jpg")
logo = pygame.image.load("logo6.jpg")

# Load background image
background_image = pygame.image.load("back3.jpg")
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))


# scale button images to fit the window
button_width = 50
button_height = 50
play_image = pygame.transform.scale(play_image, (button_width, button_height))
pause_image = pygame.transform.scale(pause_image, (button_width, button_height))
previous_image = pygame.transform.scale(previous_image, (button_width, button_height))
next_image = pygame.transform.scale(next_image, (button_width, button_height))
logo = pygame.transform.scale(logo, (200, 200))

# calculate button positions
play_pos = (WINDOW_WIDTH // 2 - button_width // 2, WINDOW_HEIGHT - button_height - 20)
previous_pos = (play_pos[0] - 100, play_pos[1])
next_pos = (play_pos[0] + 100, play_pos[1])

# font settings for song information and duration
font = pygame.font.Font(None, 24)
text_color = (255, 255, 255)
song_info_pos = (50, 400)
duration_bar_pos = (50, 450)
duration_bar_width = WINDOW_WIDTH - 100
duration_bar_height = 10

# load and play the initial music file
pygame.mixer.music.load(music_files[current_music_index])
pygame.mixer.music.play()
pygame.mixer.music.set_endevent(pygame.USEREVENT)

# game loop
running = True
paused = False
while running:
    # check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # handle end of song event
        if event.type == pygame.USEREVENT:
            current_music_index = (current_music_index + 1) % len(music_files)
            pygame.mixer.music.load(music_files[current_music_index])
            pygame.mixer.music.play()

        # check for mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if play_pos[0] <= mouse_pos[0] <= play_pos[0] + button_width and \
                    play_pos[1] <= mouse_pos[1] <= play_pos[1] + button_height:
                # toggle play/pause
                if paused:
                    pygame.mixer.music.unpause()
                    paused = False
                else:
                    pygame.mixer.music.pause()
                    paused = True

            elif previous_pos[0] <= mouse_pos[0] <= previous_pos[0] + button_width and \
                    previous_pos[1] <= mouse_pos[1] <= previous_pos[1] + button_height:
                # play the previous music file
                current_music_index = (current_music_index - 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_music_index])
                pygame.mixer.music.play()

            elif next_pos[0] <= mouse_pos[0] <= next_pos[0] + button_width and \
                    next_pos[1] <= mouse_pos[1] <= next_pos[1] + button_height:
                # play the next music file
                current_music_index = (current_music_index + 1) % len(music_files)
                pygame.mixer.music.load(music_files[current_music_index])
                pygame.mixer.music.play()

    # get the current position of the music in seconds
    current_time = pygame.mixer.music.get_pos() / 1000

    # get the duration of the current song using Mutagen
    audio = MP3(music_files[current_music_index])
    total_time = audio.info.length

    # render the song information and duration text
    song_info_text = f"Playing: {os.path.basename(music_files[current_music_index])}"
    duration_text = f"{int(current_time)}s / {int(total_time)}s"
    song_info_surface = font.render(song_info_text, True, text_color)
    duration_surface = font.render(duration_text, True, text_color)

    # calculate the width of the duration bar
    duration_bar_width_filled = int(
        (current_time / total_time) * duration_bar_width
    )

    # update the display
    window.blit(background_image, (0, 0))  # fill the window with a dark background color
    window.blit(logo, (WINDOW_WIDTH // 2 - 100, 100))  # adjust the position of the logo
    window.blit(previous_image, previous_pos)
    window.blit(play_image if not paused else pause_image, play_pos)
    window.blit(next_image, next_pos)
    window.blit(song_info_surface, song_info_pos)
    window.blit(duration_surface, (WINDOW_WIDTH - 150, 400))
    pygame.draw.rect(
        window,
        (255, 255, 255),
        pygame.Rect(duration_bar_pos[0], duration_bar_pos[1], duration_bar_width, duration_bar_height),
    )
    pygame.draw.rect(
        window,
        (30, 144, 255),
        pygame.Rect(
            duration_bar_pos[0],
            duration_bar_pos[1],
            duration_bar_width_filled,
            duration_bar_height,
        ),
    )

    pygame.display.update()

# quit pygame
pygame.quit()
