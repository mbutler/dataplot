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
    
def save_image_as_png(image_data, png_filename):
    image = Image.open(image_data)
    image.save(png_filename, 'PNG')

def save_image_to_pdf(image_data, pdf_filename):
    # Create a PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Define image size and position
    image_width = 400  # Adjust as needed
    image_height = 400  # Adjust as needed
    x_position = (letter[0] - image_width) / 2  # Center horizontally
    y_position = (letter[1] - image_height) / 2 + 75  # Center vertically

    # Draw the image onto the PDF
    c.drawImage(ImageReader(image_data), x_position, y_position, width=image_width, height=image_height)

    # Save the PDF
    c.save()

def save_image(image_data, format, original_filename):
    if format == 'pdf':
        pdf_filename = original_filename.replace('.html', '.pdf')
        save_image_to_pdf(image_data, pdf_filename)
    elif format == 'png':
        png_filename = original_filename.replace('.html', '.png')
        save_image_as_png(image_data, png_filename)
    else:
        print(f"Unsupported format: {format}")

# Iterate over all HTML files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r') as file:
            html_content = file.read()

        base64_image = extract_base64_image(html_content)
        if base64_image:
            image_data = io.BytesIO(base64.b64decode(base64_image))
            save_image(image_data, 'pdf', filename)  # Or 'png' based on requirement
        else:
            print(f"No base64 encoded image found in {filename}.")
