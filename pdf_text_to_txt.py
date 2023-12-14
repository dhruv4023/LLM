import PyPDF2

def pdf_to_text(input_pdf_path, output_txt_path):
    with open(input_pdf_path, 'rb') as pdf_file:
        print(pdf_file)
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Create a text file to write the extracted text
        with open(output_txt_path, 'w', encoding='utf-8') as txt_file:
            # Iterate through all pages in the PDF
            for page_num in range(len(pdf_reader.pages)):
                # Get the text content of the current page
                page = pdf_reader.pages[page_num]
                text = page.extract_text()

                # Write the text to the text file
                txt_file.write(text)


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        print(pdf)
        pdf_reader =PyPDF2.PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    print("---------------------------------------------------------------------------------------------------------")
    print(len(text))
    print("---------------------------------------------------------------------------------------------------------")
    return text

if __name__ == "__main__":
    input_pdf_path = "IPC_186045_pgs_15_20.pdf"
    output_txt_path = "output.txt"

    print("start...")
    # print(get_pdf_text(["IPC_186045.pdf"]))
    pdf_to_text(input_pdf_path, output_txt_path)
    print("done")
