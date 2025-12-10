# Gunakan image Python resmi yang ringan
FROM python:3.10-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode aplikasi ke container
COPY . .

# Expose port 8000 (Port default FastAPI/Uvicorn)
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port $PORT"]

