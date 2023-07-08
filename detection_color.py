import argparse
import cv2
import pandas as pd

# Create an argument parser to take the image path from the command line
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-i', '--image', required=True, help='Image Path')
args = vars(arg_parser.parse_args())
image_path = args['image']

# Read the image with OpenCV
image = cv2.imread(image_path)

# Declare global variables
clicked = False
r = g = b = x_pos = y_pos = 0

# Read the CSV file with pandas and give names to each column
column_names = ['color', 'color_name', 'hex', 'R', 'G', 'B']
color_data = pd.read_csv('colors.csv', names=column_names, header=None)

# Function to calculate the minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum_distance = float('inf')
    for i in range(len(color_data)):
        d = abs(R - int(color_data.loc[i, 'R'])) + abs(G - int(color_data.loc[i, 'G'])) + abs(B - int(color_data.loc[i, 'B']))
        if d <= minimum_distance:
            minimum_distance = d
            color_name = color_data.loc[i, 'color_name']
    return color_name

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = image[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)


while True:
    cv2.imshow('image', image)
    if clicked:
        # Draw a rectangle filled with the selected color
        cv2.rectangle(image, (20, 20), (750, 60), (b, g, r), -1)

        # Create a text string to display the color name and RGB values
        text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

        # Put the text on the image
        cv2.putText(image, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colors, display the text in black
        if r + g + b >= 600:
            cv2.putText(image, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when the user hits the 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

cv2.destroyAllWindows()
