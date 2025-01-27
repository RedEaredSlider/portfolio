import PyPDF2
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def add_text_to_pdf(input_pdf_path, output_pdf_path, text, position=(500, 10)):
    """
    Adds a specified text to each page of a PDF at a given position.

    Args:
        input_pdf_path (str): Path to the input PDF file.
        output_pdf_path (str): Path to the output PDF file.
        text (str): Text to add to the PDF.
        position (tuple): Coordinates (x, y) for placing the text on the page.
    """
    # Read the input PDF
    reader = PyPDF2.PdfReader(input_pdf_path)
    writer = PyPDF2.PdfWriter()

    # Loop through each page
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]

        # Create a new PDF with the text
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=letter)
        x, y = position

        # Draw the text at the specified position
        can.drawString(x, y, str(text))
        can.save()

        # Move to the beginning of the StringIO buffer
        packet.seek(0)

        # Read the new PDF with the text
        new_pdf = PyPDF2.PdfReader(packet)
        new_page = new_pdf.pages[0]

        # Merge the new PDF with the original page
        page.merge_page(new_page)

        # Add the page to the writer object
        writer.add_page(page)

    # Write the output PDF
    with open(output_pdf_path, "wb") as output_pdf:
        writer.write(output_pdf)

# Example usage
input_pdf_path = r"C:\Path\To\Input\SampleInput.pdf"  # Update with your input PDF file path
output_pdf_path = r"C:\Path\To\Output\SampleOutput.pdf"  # Update with your output PDF file path
text = "123-45-6789"  # Update with the text you want to add
position = (500, 10)  # Optional: Update the position of the text if needed

add_text_to_pdf(input_pdf_path, output_pdf_path, text, position)
