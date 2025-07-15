# Use an official slim Python runtime as a parent image
FROM python:3.10-slim

# Ensure output is sent straight to the terminal (no buffering)
ENV PYTHONUNBUFFERED=1

# Set a default PORT (Railway will override this)
ENV PORT=5000

# Create and switch to the app directory
WORKDIR /app

# Copy and install dependencies first (leverages Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port (for documentation; Railway uses the env var)
EXPOSE $PORT

# Use sh -c so that $PORT is expanded at runtime
CMD ["sh", "-c", "gunicorn main:app -b 0.0.0.0:$PORT --timeout 120"]
