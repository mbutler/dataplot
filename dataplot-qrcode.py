import os
import segno
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth

# Function to generate PDF from text content
def generate_pdf(text_content, pdf_filename):
    # Generate QR code and save to in-memory buffer
    qrcode = segno.make(text_content, micro=False)
    out = io.BytesIO()
    qrcode.save(out, scale=10, dark="#000000", light="#FFFFFF", kind="png")
    out.seek(0)

    # Create a PDF
    c = canvas.Canvas(pdf_filename, pagesize=letter)

    # First Page: QR Code
    # Define image size and position for QR code
    image_width = 600  # Adjust as needed
    image_height = 600  # Adjust as needed
    x_position = (letter[0] - image_width) / 2  # Center horizontally
    y_position = (letter[1] - image_height) / 2 + 75  # Center vertically

    # Draw the QR code image onto the PDF
    c.drawImage(ImageReader(out), x_position, y_position, width=image_width, height=image_height)

    # Add text (filename without the .pdf extension)
    text_x_position = 200  # Adjust as needed
    text_y_position = 50   # Adjust as needed
    display_filename = os.path.basename(pdf_filename).replace('.pdf', '')
    c.drawString(text_x_position, text_y_position, display_filename)

    # Create a new page for the text content
    c.showPage()

    # Second Page: Text Content
    # Set up the text object
    text = c.beginText(50, letter[1] - 100)
    text.setFont("Courier", 12)
    lineHeight = 14  # Adjust as needed
    max_width = 500  # Width for wrapping

    # Process the text content line by line
    for line in text_content.split('\n'):
        current_line = ''
        for word in line.split():
            # Check if adding the next word exceeds the max width
            if stringWidth(current_line + word, "Helvetica", 12) <= max_width:
                current_line += word + ' '
            else:
                # Add the current line to the text object and start a new line
                text.textLine(current_line)
                current_line = word + ' '
        # Add the last line of the paragraph
        text.textLine(current_line)

    # Draw the text object
    c.drawText(text)

    # Save the PDF
    c.save()

# Iterate over all .txt files in the current directory
for filename in os.listdir('.'):
    if filename.endswith('.txt'):
        with open(filename, 'r') as f:
            text_content = f.read()

        pdf_filename = filename.replace('.txt', '.pdf')
        generate_pdf(text_content, pdf_filename)
