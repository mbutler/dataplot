import os
import re
import base64
import json
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

def extract_article_hash(html_content):
    match = re.search(r'<meta content="(.*?)" name="jwt-block-0"/>', html_content)
    if not match:
        return None

    jwt = match.group(1)

    try:
        _, payload, _ = jwt.split('.')
    except ValueError:
        return None

    try:
        decoded_payload = base64.b64decode(payload + '==')  # Pad with == to ensure correct padding
    except (base64.binascii.Error, ValueError):
        return None

    try:
        payload_data = json.loads(decoded_payload)
        return payload_data.get('article_hash')
    except json.JSONDecodeError:
        return None

def extract_base64_image(html_content):
    # Regular expression to find base64 encoded images
    pattern = r'src="data:image\/png;base64,(.*?)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    else:
        return None
    
def extract_jwt(html_content):
    # Regular expression to find JWT
    pattern = r'jwt=(.*?)"'
    match = re.search(pattern, html_content)
    if match:
        return match.group(1)
    else:
        return None
    
def save_image_as_png(image_data, png_filename):
    image = Image.open(image_data)
    image.save(png_filename, 'PNG')

def save_image_to_pdf(image_data, pdf_filename, article_hash):
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
    c.drawString(text_x_position, text_y_position, os.path.basename(article_hash))

    # Save the PDF
    c.save()

def save_image(image_data, format, original_filename, article_hash):
    if format == 'pdf':
        pdf_filename = original_filename.replace('.html', '.pdf')
        save_image_to_pdf(image_data, pdf_filename, article_hash)
    elif format == 'png':
        png_filename = original_filename.replace('.html', '.png')
        save_image_as_png(image_data, png_filename)
    else:
        print(f"Unsupported format: {format}")

def rename_file_to_article_hash(original_filename, article_hash):
    if article_hash:
        new_filename = f"{article_hash}.html"
        try:
            os.rename(original_filename, new_filename)
            print(f"Renamed '{original_filename}' to '{new_filename}'")
        except OSError as error:
            print(f"Error renaming file: {error}")
    else:
        print(f"Article hash not found for '{original_filename}'. File not renamed.")

# Iterate over all HTML files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r') as file:
            html_content = file.read()

        base64_image = extract_base64_image(html_content)
        article_hash = extract_article_hash(html_content)

        rename_file_to_article_hash(filename, article_hash)

        if base64_image:
            image_data = io.BytesIO(base64.b64decode(base64_image))
            save_image(image_data, 'pdf', filename, article_hash)  # Or 'png' based on requirement
        else:
            print(f"No base64 encoded image found in {filename}.")
