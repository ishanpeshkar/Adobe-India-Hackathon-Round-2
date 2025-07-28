FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY process_pdfs.py .
COPY document_outline_model.pkl .

# Create input/output folders
RUN mkdir -p /app/input /app/output

CMD ["python", "process_pdfs.py"]