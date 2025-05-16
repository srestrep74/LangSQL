FROM python:3.11-slim

# Workdir
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Expose the port
EXPOSE 8000
# Start the server
CMD ["uvicorn", "app:app", "--host", "0.0.0", "--port", "8000"]