from fastapi import FastAPI, UploadFile, File,Query,Form
import subprocess
import shutil
import os
import pymupdf4llm
import random
from tempfile import NamedTemporaryFile

app = FastAPI()

@app.get("/")
async def hello():
    return {"hello" : "world"}


@app.post("/pdf-to-md/")
async def convert_pdf_to_md(file: UploadFile = File(...)):

    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        # Write the uploaded file content to the temp file
        temp_file.write(await file.read())
        temp_file_path = temp_file.name
    
    # Convert the temporary PDF file to Markdown
    with open(temp_file_path, "rb") as pdf_file:
        md_text = pymupdf4llm.to_markdown(pdf_file)
    
    # Optionally, delete the temporary file if it's no longer needed
    os.remove(temp_file_path)

    return {"markdown": md_text}

@app.post("/docx-to-md/")
async def convert_to_md(file: UploadFile = File(...)):

    random_number = str(random.randint(10000, 99999))

    # Save the uploaded file temporarily
    input_file = f"/tmp/{random_number}.docx"
    with open(input_file, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Convert the file to markdown using pandoc
    output_file = f"/tmp/{os.path.splitext(random_number)[0]}.md"
    subprocess.run(["pandoc", input_file, "-o", output_file])

    # Read the converted markdown content
    with open(output_file, "r") as f:
        markdown_content = f.read()

    # Clean up the temporary files
    os.remove(input_file)
    os.remove(output_file)

    return {"markdown": markdown_content}
