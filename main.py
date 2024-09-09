from fastapi import FastAPI, UploadFile, File
import subprocess
import shutil
import os

app = FastAPI()

@app.get("/")
async def hello():
    return {"hello" : "world"}

@app.post("/convert-to-md/")
async def convert_to_md(file: UploadFile = File(...)):
    # Save the uploaded file temporarily
    input_file = f"/tmp/{file.filename}"
    with open(input_file, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Convert the file to markdown using pandoc
    output_file = f"/tmp/{os.path.splitext(file.filename)[0]}.md"
    subprocess.run(["pandoc", input_file, "-o", output_file])

    # Read the converted markdown content
    with open(output_file, "r") as f:
        markdown_content = f.read()

    # Clean up the temporary files
    os.remove(input_file)
    os.remove(output_file)

    return {"filename": file.filename, "markdown": markdown_content}
