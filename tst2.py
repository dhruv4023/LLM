link_arr=["https://www.indiacode.nic.in/bitstream/123456789/2338/1/A1882-04.pdf","https://registration.uk.gov.in/files/Stamp_Act_Eng.pdf","https://dolr.gov.in/sites/default/files/THE%20LAND%20ACQUISITION%20ACT.pdf","https://www.indiacode.nic.in/bitstream/123456789/13236/1/the_registration_act%2C_1908.pdf","https://www.indiacode.nic.in/bitstream/123456789/5615/1/muslim_marriages_registration_act%2C_1981.pdf","https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf","https://www.icsi.edu/media/webmodules/companiesact2013/COMPANIES%20ACT%202013%20READY%20REFERENCER%2013%20AUG%202014.pdf","https://www.indiacode.nic.in/bitstream/123456789/15351/1/iea_1872.pdf","https://www.iitk.ac.in/wc/data/IPC_186045.pdf","https://lddashboard.legislative.gov.in/sites/default/files/A1955-25_1.pdf","https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050195.pdf","""https://sclsc.gov.in/theme/front/pdf/ACTS%20FINAL/THE%20CODE%20OF%20CIVIL%20PROCEDURE,%201908.pdf""","https://ncwapps.nic.in/acts/TheIndianChristianMarriageAct1872-15of1872.pdf","https://www.indiacode.nic.in/bitstream/123456789/2347/1/190907.pdf","https://www.indiacode.nic.in/bitstream/123456789/2280/1/A1869-04.pdf","https://www.indiacode.nic.in/bitstream/123456789/15480/1/special_marriage_act.pdf"]


link_arr[9]="https://highcourtchd.gov.in/hclscc/subpages/pdf_files/4.pdf"

link_arr=['https://www.indiacode.nic.in/bitstream/123456789/2338/1/A1882-04.pdf', 'https://registration.uk.gov.in/files/Stamp_Act_Eng.pdf', 'https://dolr.gov.in/sites/default/files/THE%20LAND%20ACQUISITION%20ACT.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/13236/1/the_registration_act%2C_1908.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/5615/1/muslim_marriages_registration_act%2C_1981.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/2187/2/A187209.pdf', 'https://www.icsi.edu/media/webmodules/companiesact2013/COMPANIES%20ACT%202013%20READY%20REFERENCER%2013%20AUG%202014.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/15351/1/iea_1872.pdf', 'https://www.iitk.ac.in/wc/data/IPC_186045.pdf', 'https://highcourtchd.gov.in/hclscc/subpages/pdf_files/4.pdf', 'https://cdnbbsr.s3waas.gov.in/s380537a945c7aaa788ccfcdf1b99b5d8f/uploads/2023/05/2023050195.pdf', 'https://sclsc.gov.in/theme/front/pdf/ACTS%20FINAL/THE%20CODE%20OF%20CIVIL%20PROCEDURE,%201908.pdf', 'https://ncwapps.nic.in/acts/TheIndianChristianMarriageAct1872-15of1872.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/2347/1/190907.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/2280/1/A1869-04.pdf', 'https://www.indiacode.nic.in/bitstream/123456789/15480/1/special_marriage_act.pdf']
# print(link_arr)
# # for i in link_arr:
#     # print(i)
# import os
# import requests
# from urllib.parse import urlparse

# def download_pdfs(pdf_links, output_folder):
#     # Create the output folder if it doesn't exist
#     os.makedirs(output_folder, exist_ok=True)

#     for pdf_link in pdf_links:
#         try:
#             # Download the PDF file
#             response = requests.get(pdf_link)
#             if response.status_code == 200:
#                 # Extract the filename from the URL
#                 url_path = urlparse(pdf_link).path
#                 filename = os.path.join(output_folder, os.path.basename(url_path))

#                 # Save the PDF content to a local file
#                 with open(filename, "wb") as pdf_file:
#                     pdf_file.write(response.content)

#                 print(f"Downloaded {filename}")
#             else:
#                 print(f"Failed to download {pdf_link}. Status code: {response.status_code}")

#         except Exception as e:
#             print(f"Error downloading {pdf_link}: {str(e)}")

# # Example list of PDF links
# pdf_links = [
#     "https://www.example.com/pdf1.pdf",
#     "https://www.example.com/pdf2.pdf",
#     # Add more PDF links as needed
# ]

# # Specify the output folder for downloaded PDFs
# output_folder = "DataSourceFiles"

# # # Call the function to download PDFs
# # download_pdfs(link_arr, output_folder)

