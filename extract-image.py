import os
import re
import base64
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def extract_base64_image(html_content):
    # Regular expression to find base64 encoded images
    pattern = r'src="data:image\/png;base64,(.*?)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    else:
        return None

def save_image_to_pdf(image_data, pdf_filename):
    # Create a PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Define image size and position
    image_width = 500  # Adjust as needed
    image_height = 500  # Adjust as needed
    x_position = (letter[0] - image_width) / 2  # Center horizontally
    y_position = (letter[1] - image_height) / 2 + 75  # Center vertically

    # Draw the image onto the PDF
    c.drawImage(ImageReader(image_data), x_position, y_position, width=image_width, height=image_height)

    # Add text (filename)
    text_x_position = 110  # Adjust as needed
    text_y_position = 120   # Adjust as needed
    hash_value = "13c78c707b010724cd9e1f596b58246a2c829384fc8a8a4b49aa38b3fddfc1c2"
    c.drawString(text_x_position, text_y_position, os.path.basename(hash_value))

    # Save the PDF
    c.save()

# Iterate over all HTML files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        # Open and read the HTML file
        with open(filename, 'r') as file:
            html_content = file.read()

        # Extract and decode the base64 image
        base64_image = extract_base64_image(html_content)
        if base64_image:
            image_data = io.BytesIO(base64.b64decode(base64_image))
            pdf_filename = filename.replace('.html', '.pdf')
            save_image_to_pdf(image_data, pdf_filename)
        else:
            print(f"No base64 encoded image found in {filename}.")
