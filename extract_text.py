from docx import Document

doc = Document("Sushma_Yadav_Data_Engineer_Resume.docx")

text_parts = []
for para in doc.paragraphs:
    if para.text.strip():
        text_parts.append(para.text)

full_text = "\n".join(text_parts)
print("Total characters extracted:", len(full_text))
print()
print("First 300 characters:")
print(full_text[:300])
