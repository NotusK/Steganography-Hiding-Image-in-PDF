import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import base64
import json
from PyPDF2 import PdfReader

def split_pdf(input_pdf, output_first_page, output_rest_pages, output_last_page):
    # Open the input PDF file
    with open(input_pdf, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer_first_page = PyPDF2.PdfWriter()
        writer_rest_pages = PyPDF2.PdfWriter()
        writer_last_page = PyPDF2.PdfWriter()

        # Add the first page to the first page PDF writer
        first_page = reader.pages[0]
        writer_first_page.add_page(first_page)

        # Add the rest of the pages (except the first and last) to the rest pages PDF writer
        for page_num in range(1, len(reader.pages) - 1):
            page = reader.pages[page_num]
            writer_rest_pages.add_page(page)

        # Add the last page to the last page PDF writer
        last_page = reader.pages[-1]
        writer_last_page.add_page(last_page)

        # Write the PDFs to disk
        with open(output_first_page, 'wb') as output_file:
            writer_first_page.write(output_file)
        
        with open(output_rest_pages, 'wb') as output_file:
            writer_rest_pages.write(output_file)
        
        with open(output_last_page, 'wb') as output_file:
            writer_last_page.write(output_file)

def show_image_from_hidden(input_pdf, output_pdf, image_path):
    # Open the existing PDF
    existing_pdf = canvas.Canvas(input_pdf)

    # Get the dimensions of the existing PDF
    existing_width, existing_height = letter

    # Read the image data
    img = ImageReader(image_path)

    # Create a new PDF canvas
    new_pdf = canvas.Canvas(output_pdf, pagesize=letter)

    # Copy contents from existing PDF to new PDF
    new_pdf.showPage()
    new_pdf.save()

    # Open the new PDF for appending
    new_pdf = canvas.Canvas(output_pdf)

    # Draw the image at the new position
    new_pdf.drawImage(img, 0, 0, width=existing_width, height= existing_height * 0.8)

    # Save the modified PDF
    new_pdf.save()

def extract_hidden_text_from_pdf(pdf_file):
    # Open the PDF file
    with open(pdf_file, 'rb') as file:
        # Create a PdfReader object
        pdf_reader = PdfReader(file)
        
        # Get the first page
        page = pdf_reader.pages[0]
        
        # Extract the hidden text from the page
        hidden_text = page.extract_text().strip()
        
        return hidden_text
    
def decode_hidden_text(hidden_text):
    # Reverse the replacement of 'S' with 'O'
    # decrypted_message = hidden_text.replace('S', 'O')
    
    # Decode the base64 encoded string
    decoded_message = base64.b64decode(hidden_text)
    
    try:
        # Convert the decoded byte string to a string using UTF-8 encoding
        metadata = decoded_message.decode('utf-8')
    except UnicodeDecodeError as e:
        # Handle the UnicodeDecodeError
        print(f"Error decoding message: {e}")
        # Optionally, you can specify how to handle the error, e.g., 'ignore' or 'replace'
        metadata = decoded_message.decode('utf-8', errors='replace')
    
    # Parse the JSON string to a dictionary
    metadata_dict = json.loads(metadata)
    
    return metadata_dict


# Example input PDF
input_pdf = "tugas/encrypt_result.pdf"

# Output filenames for the first page, rest pages, and last page
output_first_page = "tugas_output/first_page.pdf"
output_rest_pages = "tugas_output/jurnal.pdf"
output_last_page = "tugas_output/last_page.pdf"
output_visible_image = "tugas_output/decoded_image.pdf"
image_path = "output/logo.jpg"

# Split the PDF into three parts
split_pdf(input_pdf, output_first_page, output_rest_pages, output_last_page)
show_image_from_hidden(output_first_page, output_visible_image, image_path)

hidden_text = extract_hidden_text_from_pdf(output_last_page)
metadata = decode_hidden_text(hidden_text)
print("Decoded Metadata:")
print(metadata)
