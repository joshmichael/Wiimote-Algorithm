import cwiid
import sys
import pygame
import time
import math

def connect_to_wiimote():
    print('Put Wiimote in discoverable mode now (press 1+2)...')
    wiimote = None
    while not wiimote:
        try:
            wiimote = cwiid.Wiimote()
        except RuntimeError:
            pass
    return wiimote

def calculate_roll(x, z):
    # Calculate the roll angle in radians
    roll_radians = math.atan2(x - 124, z - 124)
    # Convert the roll angle to degrees
    roll_degrees = math.degrees(roll_radians)
    # Normalize the roll angle to be within 0-360 degrees
    roll_degrees = (roll_degrees + 360) % 360
    return roll_degrees

def correct_coordinates_for_roll(x, y, roll):
    roll_radians = math.radians(roll)
    corrected_x = x * math.cos(roll_radians) - y * math.sin(roll_radians)
    corrected_y = x * math.sin(roll_radians) + y * math.cos(roll_radians)
    return corrected_x, corrected_y

def lerp(current, target, factor):
    return (1 - factor) * current + factor * target

def main():
    midpoint_x = 0
    midpoint_y = 0

    # Initialize previous positions and velocities
    prev_x, prev_y = 0, 0
    velocity_x, velocity_y = 0, 0
    friction = 0.95

    wiimote = connect_to_wiimote()
    # Enable IR, Button & Accelerometer reporting
    wiimote.rpt_mode = cwiid.RPT_IR | cwiid.RPT_BTN | cwiid.RPT_ACC
    start_time = time.time()

    pygame.init()
    WIDTH = 1920
    HEIGHT = 1000
    FPS = 144
    pygame.display.set_caption('Wiimote Dot')
    gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                wiimote.close()
                sys.exit()

        # Default colour
        dot_colour = (255, 255, 255)

        wiimote.enable(cwiid.FLAG_MESG_IFC)
        buttons = wiimote.state['buttons']
        if (buttons & cwiid.BTN_B):
            dot_colour = (255, 0, 0)
        else:
            dot_colour = (255, 255, 255)

        elapsed_time = time.time() - start_time
        if elapsed_time >= 1 / 200:
            # Get the raw accelerometer data
            acc_data = wiimote.state['acc']

            # Extract the x and z values
            x = acc_data[cwiid.X]
            z = acc_data[cwiid.Z]

            # Calculate the roll angle
            roll = calculate_roll(x, z)

            # Process IR messages
            messages = wiimote.get_mesg()
            valid_src = False
            x_values = []
            y_values = []
            for mesg in messages:
                if mesg[0] == cwiid.MESG_IR:
                    for src in mesg[1]:
                        if src:
                            valid_src = True
                            x, y = src['pos']
                            x_values.append(-x + 500 + center_x)
                            y_values.append(y - 400 + center_y)

            if valid_src:
                # Correct the coordinates for roll angle
                corrected_x_values = []
                corrected_y_values = []
                for i in range(len(x_values)):
                    corrected_x, corrected_y = correct_coordinates_for_roll(x_values[i] - center_x, y_values[i] - center_y, roll)
                    corrected_x_values.append(corrected_x + center_x)
                    corrected_y_values.append(corrected_y + center_y)

                # Calculate velocity
                velocity_x = lerp(midpoint_x, sum(corrected_x_values) / len(corrected_x_values), 0.2) - prev_x
                velocity_y = lerp(midpoint_y, sum(corrected_y_values) / len(corrected_y_values), 0.2) - prev_y

                # Update position
                midpoint_x += velocity_x
                midpoint_y += velocity_y

                # Store current position for next frame
                prev_x = midpoint_x
                prev_y = midpoint_y
            else:
                # No IR data, move dot based on previous velocity
                midpoint_x += velocity_x
                midpoint_y += velocity_y

                # Apply friction to velocity
                velocity_x *= friction
                velocity_y *= friction
            start_time = time.time()
        
        # Clear the screen
        gameDisplay.fill((0, 0, 0))

        # Draw the dot with coordinates
        pygame.draw.circle(gameDisplay, dot_colour, (int(midpoint_x), int(midpoint_y)), 10)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()