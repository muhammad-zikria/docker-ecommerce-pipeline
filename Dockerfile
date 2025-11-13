FROM python:3.9-slim

RUN pip install pandas sqlalchemy psycopg2-binary

# Setting the "working directory" inside the container
WORKDIR /app

# Default command to run the container
ENTRYPOINT ["python", "ingest_data.py"]