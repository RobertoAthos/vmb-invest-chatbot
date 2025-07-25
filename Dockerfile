# Use Python 3.12 slim image for better performance
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better Docker layer caching
COPY pyproject.toml ./

# Install dependencies directly (quoted to handle version constraints)
RUN pip install --no-cache-dir "crewai[tools]>=0.148.0,<1.0.0" "streamlit>=1.28.0" "python-dotenv>=1.0.0" "jq>=1.6.0"

# Copy the entire project
COPY . .

# Add the src directory to Python path so imports work
ENV PYTHONPATH=/app/src

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose Streamlit default port
EXPOSE 8501

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Run the Streamlit application via run_ui.py
CMD ["python", "src/demo_bot/run_ui.py"]