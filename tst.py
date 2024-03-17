import requests
from PyPDF2 import PdfReader

# URL of the PDF file
pdf_url = "https://www.iitk.ac.in/wc/data/IPC_186045.pdf"

# Function to download PDF and extract text
def download_and_convert_to_text(pdf_url, output_file_path):
    # Download the PDF file
    response = requests.get(pdf_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Save the PDF content to a local file
        with open("temp.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)

        # Open the downloaded PDF file
        with open("temp.pdf", "rb") as pdf_file:
            # Create a PDF reader object
            pdf_reader = PdfReader(pdf_file)

            # Initialize an empty string to store the extracted text
            text_content = ""

            # Iterate through each page in the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Extract the text from the current page
                page = pdf_reader.pages[page_num]
                text_content += page.extract_text()

        # Save the extracted text to a text file
        with open(output_file_path, "w", encoding="utf-8") as output_file:
            output_file.write(text_content)

        print(f"Text extracted and saved to {output_file_path}")

    else:
        print(f"Failed to download the PDF. Status code: {response.status_code}")

# Specify the output file path for the text file
output_txt_file_path = "output.txt"

# Call the function to download and convert the PDF to text
download_and_convert_to_text(pdf_url, output_txt_file_path)
