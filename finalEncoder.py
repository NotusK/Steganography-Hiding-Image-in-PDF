from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfReader
import PyPDF2
from reportlab.lib.pagesizes import letter
import base64
import json

#Function to get the medatada of PDF's
def get_pdf_metadata(pdf_file):
    # Create a PdfReader object
    pdf_reader = PdfReader(pdf_file)

    # Get metadata
    metadata = {
        'Title': pdf_reader.metadata.get('/Title', "Tidak ada judul"),
        'Author': pdf_reader.metadata.get('/Author', "Tidak ada informasi penulis"),
        'Subject': pdf_reader.metadata.get('/Subject', "Tidak ada subjek"),
        'Creator': pdf_reader.metadata.get('/Creator', "Tidak ada pencipta"),
        'Producer': pdf_reader.metadata.get('/Producer', "Tidak ada produsen"),
        'Creation Date': pdf_reader.metadata.get('/CreationDate', "Tidak ada informasi tanggal pembuatan"),
        'Modification Date': pdf_reader.metadata.get('/ModDate', "Tidak ada informasi tanggal modifikasi"),
        'Keywords': pdf_reader.metadata.get('/Keywords', "Tidak ada kata kunci")
    }

    return metadata

def edit_pdf_metadata(input_pdf, output_pdf, new_metadata):
    # Open the input PDF file in read-binary mode
    with open(input_pdf, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()

        # Copy pages and metadata from the input PDF to the output PDF
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # Update metadata
        pdf_writer.add_metadata(new_metadata)

        # Write the updated metadata to the output PDF file
        with open(output_pdf, 'wb') as output_file:
            pdf_writer.write(output_file)


def merge_metadata(old_metadata, new_metadata):
    merged_metadata = old_metadata.copy()  # Make a copy of the old metadata dictionary
    merged_metadata.update(new_metadata)   # Update the old metadata with the new metadata
    return merged_metadata

#Function to put an image in PDF then hiding it
def embed_image_in_pdf(image_path, output_pdf, width=6.5*inch, height=9*inch):
    c = canvas.Canvas(output_pdf, pagesize=A4)

    # Read the image data
    img = ImageReader(image_path)

    # Determine the scaling factor to fit the image within the specified width and height
    img_width, img_height = img.getSize()
    scale_x = width / img_width
    scale_y = height / img_height

    # Scale and draw the image
    c.drawImage(img, 1000, 1000, width=width, height=height * 0.8)

    c.save()


def create_last_page_pdf(metadata, output_pdf):
    # Create a new PDF document
    c = canvas.Canvas(output_pdf, pagesize=letter)

    # Set text color to white (to be hidden)
    c.setFillColorRGB(1, 1, 1)

    # Convert metadata dictionary to a JSON string
    metadata_json = json.dumps(metadata)
        
    # Encrypt message using base64 encoding
    encrypted_message = base64.b64encode(metadata_json.encode()).decode()

    # Replace 'O' with 'S' in the encrypted message
    encrypted_message = encrypted_message.replace('O', 'S')

    # Add the encrypted message as hidden text
    c.drawString(100, 100, encrypted_message)

    # Save the PDF document
    c.save()

def merge_pdf(pdf_files, output_pdf):
    merger = PyPDF2.PdfMerger()
    
    for pdf_file in pdf_files:
        merger.append(pdf_file)
    
    with open(output_pdf, 'wb') as output_file:
        merger.write(output_file)





# Example image to embed
pdf_file_path = "tugas/jurnal.pdf"
output_of_edited_jurnal_metadata_pdf = 'tugas/edited_metadata_jurnal.pdf'
new_metadata = {'/Title': 'Implementasi Metode Prototype dalam Membangun Sistem Informasi Penjualan Online pada Toko Herbal Pahlawan', 
                '/Author': 'Achmad Zuhri Al Muhtadi & Lukman Junaedi', 
                '/Subject': 'Metode Prototype Penjualan Online pada Toko Herbal Pahlawan'}
image_path = "tugas/logo.jpg"
output_first_page_pdf = "tugas/first_page.pdf"
output_last_page_pdf = "tugas/last_page.pdf"
list_of_pdf_files_to_merge = ["tugas/first_page.pdf", "tugas/edited_metadata_jurnal.pdf", "tugas/last_page.pdf"]
output_of_merged_jurnal_logo_pdf = "tugas/encrypt_result.pdf"



old_metadata = get_pdf_metadata(pdf_file_path)
edit_pdf_metadata(pdf_file_path, output_of_edited_jurnal_metadata_pdf, new_metadata)
edited_metadata = get_pdf_metadata(output_of_edited_jurnal_metadata_pdf)
merged_metadata = merge_metadata(old_metadata, edited_metadata)
embed_image_in_pdf(image_path, output_first_page_pdf)
create_last_page_pdf(merged_metadata, output_last_page_pdf)
merge_pdf(list_of_pdf_files_to_merge, output_of_merged_jurnal_logo_pdf)


