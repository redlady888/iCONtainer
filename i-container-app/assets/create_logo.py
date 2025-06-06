import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import os

# Create a high-tech looking logo for i-CONtainer
def create_logo():
    # Create a new image with a dark background
    width, height = 500, 200
    image = Image.new('RGBA', (width, height), (20, 20, 30, 255))
    draw = ImageDraw.Draw(image)
    
    # Add a violet accent
    draw.rectangle([(0, height-10), (width, height)], fill=(128, 0, 255, 255))
    
    # Create a circular container icon
    center_x, center_y = width // 3, height // 2
    radius = 60
    draw.ellipse((center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius), 
                 outline=(128, 0, 255, 255), width=3)
    
    # Add some tech-looking elements
    for i in range(3):
        angle = np.pi * 2 * i / 3
        x1 = center_x + int(radius * 1.2 * np.cos(angle))
        y1 = center_y + int(radius * 1.2 * np.sin(angle))
        x2 = center_x + int(radius * 1.5 * np.cos(angle))
        y2 = center_y + int(radius * 1.5 * np.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=(128, 0, 255, 255), width=2)
    
    # Add text
    try:
        # Try to use a system font
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 40)
    except IOError:
        # Fall back to default font
        font = ImageFont.load_default()
    
    draw.text((width // 2, center_y - 20), "i-CONtainer", 
              fill=(255, 255, 255, 255), font=font, anchor="mm")
    
    # Add slogan
    try:
        small_font = ImageFont.truetype("DejaVuSans.ttf", 20)
    except IOError:
        small_font = ImageFont.load_default()
    
    draw.text((width // 2, center_y + 20), "taste without waste", 
              fill=(200, 200, 200, 255), font=small_font, anchor="mm")
    
    # Save the image
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    image.save(logo_path)
    print(f"Logo created and saved to {logo_path}")
    return logo_path

if __name__ == "__main__":
    create_logo()

