from pypdf import PdfReader

def extract_text_from_pdf(pdf_path,output_path):
    reader = PdfReader(pdf_path)
    with open(output_path, mode='w',encoding='utf-8')as file:
        for i, page in enumerate(reader.pages):
            txt_data = page.extract_text()
            if txt_data:
                file.write(f"\n---page{i + 1}\n")
                file.write(txt_data)
                file.write("\n")

