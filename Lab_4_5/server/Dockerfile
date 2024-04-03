FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files, excluding the dist/ directory
COPY . .

# Copy the dist/ directory to /app/dist/
COPY dist/ /app/dist/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]