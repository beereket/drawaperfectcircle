import pygame
from math_operations import *

# Initialize Pygame
pygame.init()

#SCREEN
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Paint Program")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 170, 51)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# TEXT
textfont = pygame.font.SysFont('Broadway', 50)
text = textfont.render('Bereket', True, 'white')

# Set up drawing variables
radius = 12
drawing = False
color = BLACK

# Setting up the fonts
font = pygame.font.SysFont("Broadway", 50)
font_msg = pygame.font.SysFont("Broadway", 20)
font_col = (0, 0, 0)

percent_text = font.render(str(""), True, BLUE)
close_text = font_msg.render("Too close to the dot!", True, RED)
status_text = font_msg.render("0", True, RED)

start = 0
start_pos = (0, 0)

# Create a list to store all the elements drawn on the screen
percent = 0
elements = []
POS = {(1, 1)}
sum = 0

#BEST_SCORE
best_score = 0
best_color = (0, 0, 0)

#STATUS
status_circ = 0
status_close = 0
status_wrongside = 0
status_default = 0
status_newscore = 0
status_timeUp = 0
negative_percent = 0
start_countdown = 1
time_up_count = 1
time_up_ticks = 0

# Game loop
while True:
    screen.fill((20, 20, 20))
    screen.blit(text, (0, 0))

    if start_countdown:
        start_ticks = 0
        start_ticks = pygame.time.get_ticks()
        start_countdown = 0
        tick_pos = pygame.mouse.get_pos()

    if time_up_count:
        time_up_ticks = 0
        time_up_ticks = pygame.time.get_ticks()
        time_up_count = 0

    timeUp_seconds = (pygame.time.get_ticks() - time_up_ticks)/1000
    seconds = (pygame.time.get_ticks() - start_ticks)/1000


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if start:
            start = 0
            start_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Initialize drawing parameters
            elements = []
            start, drawing = 1, 1
            negative_percent = 0
            status_wrongside = 0
            status_default = 0
            status_timeUp = 0
            timeUp_seconds = 0
            status_newscore = 0
            time_up_count = 1

            pos = pygame.mouse.get_pos()
            # Check if the mouse is inside the circle
            if radi(start_pos) <= 100:
                status_circ = 1
            # Create a new circle element and add it to the list of elements
            element = {"type": "circle", "color": color, "radius": radius, "pos": pos}
            elements.append(element)

        elif event.type == pygame.MOUSEBUTTONUP:
            # Check if the score is higher than the best score
            if percent > best_score and not status_timeUp:
                status_newscore = 1
                best_score = percent
                best_color = font_col
            # Check if the score is default (no errors or new high score)
            elif not (status_timeUp or status_wrongside or status_circ):
                status_default = 1

            # Reset drawing parameters
            radius = 8
            percent = 0
            POS = {(1, 1)}
            drawing = False

        elif event.type == pygame.MOUSEMOTION and drawing:
            # Check if time is up
            if timeUp_seconds > 9:
                status_timeUp = 1
                drawing = 0
            # Update the radius based on the mouse motion
            if seconds > 0.008:
                seconds = 0
                start_countdown = 1
                if tick_pos == pos:
                    if radius < 12:
                        radius += 1
                else:
                    if radius > 2:
                        radius -= 1

            pos = pygame.mouse.get_pos()
            # Check if the mouse is inside the circle or outside the range
            if radi(pos) <= 10:
                status_circ = 1
                status_default = 0
            # Update the circle color based on the mouse position
            if ABS_ERROR(start_pos, pos) < 25:
                circle_color = GREEN
            elif ABS_ERROR(start_pos, pos) > 25 and ABS_ERROR(start_pos, pos) < 35:
                circle_color = YELLOW
            else:
                circle_color = (255, 0, 0)

            lenn = len(POS) // 2
            if len(POS) > 13:
                # Compute the percent score
                for i in POS:
                    sum += ABS_ERROR(i, start_pos)
                temp = (sum / (lenn + 1))
                sum = 0
                percent = (1 - temp / radi(start_pos) * 0.7)
                # Update the font color based on the percent score
                if percent > 0.7:
                    font_col = (int(255 - (((percent - 0.7) / 0.3) * 255)), int(((percent - 0.7) / 0.3) * 255), 0)
                else:
                    font_col = (255, 0, 0)
                # Check if the percent score is negative
                if percent < 0:
                    negative_percent = 1
                    status_wrongside = 1

                if negative_percent:
                    percent_text = font.render('XX:xx%', True, font_col)
                else:
                    percent_text = font.render(str(round(percent * 100, 2)) + '%', True, font_col)

            # Get the previous position of the mouse from the last element in the list of elements
            prev_pos = elements[-1]["pos"]

            # Calculate the distance between the current and previous mouse positions
            distance = max(abs(pos[0] - prev_pos[0]), abs(pos[1] - prev_pos[1]))

            # Create a series of intermediate points along the line between the current and previous mouse positions
            for i in range(distance):
                # Calculate the x and y coordinates of the current intermediate point
                x = int(prev_pos[0] + (pos[0] - prev_pos[0]) * float(i) / distance)
                y = int(prev_pos[1] + (pos[1] - prev_pos[1]) * float(i) / distance)

                # Create a new circle element for the current intermediate point and add it to the list of elements
                element = {"type": "circle", "color": circle_color, "radius": radius, "pos": (x, y)}
                elements.append(element)

                # Add the current intermediate point to the set of positions
                POS.add((x, y))

    # Draw the screen
    screen.blit(percent_text, (329, 258))
    pygame.draw.circle(screen, (255, 255, 255), (400, 300), 6, width=0)

    if status_timeUp and not status_wrongside and not status_default:
        status_text = font_msg.render("Too slow", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
    elif status_newscore and not status_wrongside and not status_default and not status_close:
        status_text = font_msg.render("New best score", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
    elif status_wrongside:
        status_text = font_msg.render("Wrong side!", True, (0, 255, 0))
        screen.blit(status_text, (300, 340))
        drawing = 0
    elif status_default and not status_wrongside and not status_circ:
        status_text = font_msg.render("Best: ", True, WHITE)
        bst_2 = font_msg.render(str(round(best_score * 100, 2)) + '%', True, best_color)
        screen.blit(status_text, (340, 340))
        screen.blit(bst_2, (410, 340))
    elif status_close and not drawing and not status_wrongside and not status_circ:
        screen.blit(close_text, (300, 340))
    else:
        status_close = 0
    if status_circ and not status_wrongside and not status_default:
        screen.blit(close_text, (300, 340))
        drawing = 0
        status_circ = 0
        status_close = 1

    for element in elements:
        if element["type"] == "circle":
            pygame.draw.circle(screen, element["color"], element["pos"], element["radius"])

    pygame.display.flip()