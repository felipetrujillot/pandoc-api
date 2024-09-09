# Use a base image with pandoc
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install -y pandoc

# Install FastAPI and Uvicorn
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY . .

# Expose the port
EXPOSE 8001

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
