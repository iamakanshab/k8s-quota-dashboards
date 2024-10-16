FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY src/ /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "main.py"]
