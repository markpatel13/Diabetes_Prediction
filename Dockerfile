# 1) Use a lightweight Python base image
FROM python:3.11-slim

# 2) Set working directory inside the container
WORKDIR /app

# 3) Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4) Copy the entire project into the container
COPY . .

# 5) Expose ports for FastAPI and Streamlit
EXPOSE 8000
EXPOSE 8501

# 6) Default command: run the start script
CMD ["bash", "start.sh"]