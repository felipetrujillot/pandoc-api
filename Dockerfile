# Use a base image with pandoc
FROM python:3.11-slim

WORKDIR /app

COPY ./app /app

RUN apt-get update && apt-get install -y pandoc

# Install FastAPI and Uvicorn
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the port
EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
