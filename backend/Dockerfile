# backend/Dockerfile

FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app app
# ✅ Next line ensures Python always knows your /app folder is the module root.
# Also You need __init__.py in /app folder, so Python treats your app directory as a proper package
ENV PYTHONPATH=/app 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
