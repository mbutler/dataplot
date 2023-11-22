import os
import segno
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

# Function to generate PDF from text content
def generate_pdf(text_content, pdf_filename):
    # Generate QR code and save to in-memory buffer
    qrcode = segno.make(text_content, micro=False)
    out = io.BytesIO()
    qrcode.save(out, scale=10, dark="#000000", light="#FFFFFF", kind="png")
    out.seek(0)

    # Create a PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # Define image size and position
    image_width = 600  # Adjust as needed
    image_height = 600  # Adjust as needed
    x_position = (letter[0] - image_width) / 2  # Center horizontally
    y_position = (letter[1] - image_height) / 2 + 75  # Center vertically

    # Draw the QR code image onto the PDF
    c.drawImage(ImageReader(out), x_position, y_position, width=image_width, height=image_height)

    # Add text (filename)
    text_x_position = 175  # Adjust as needed
    text_y_position = 50   # Adjust as needed
    c.drawString(text_x_position, text_y_position, os.path.basename(pdf_filename))

    # Save the PDF
    c.save()

# Iterate over all .txt files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            text_content = f.read()

        pdf_filename = filename.replace('.txt', '.pdf')
        generate_pdf(text_content, pdf_filename)
