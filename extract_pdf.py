import pdfplumber

with pdfplumber.open("Sushma_Yadav_Data_Engineer_Resume.pdf") as pdf:
    text_parts = []
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)

full_text = "\n".join(text_parts)
print("Total characters extracted:", len(full_text))
print()
print("First 300 characters:")
print(full_text[:300])
