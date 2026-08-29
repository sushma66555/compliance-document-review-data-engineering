import openpyxl

wb = openpyxl.load_workbook("non-classes-dataset-list 8.xlsx")
sheet = wb.active

text_parts = []
for row in sheet.iter_rows(values_only=True):
    row_text = " | ".join(str(cell) for cell in row if cell is not None)
    if row_text.strip():
        text_parts.append(row_text)

full_text = "\n".join(text_parts)
print("Total characters extracted:", len(full_text))
print()
print("First 300 characters:")
print(full_text[:300])