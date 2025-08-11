# 1. Use an official and lightweight Python image as the base
FROM python:3.10-slim

# 2. Create a working directory inside the container
WORKDIR /app

# 3. Copy the requirements file into the container
COPY requirements.txt .

# 4. Install the Python requirements
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the project's code into the container
COPY . .

# 6. Expose the port the application runs on
EXPOSE 8000

# 7. Define the command that should be executed when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]