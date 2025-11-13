# Dockerized E-Commerce Data Pipeline

This project is a complete, containerized ETL pipeline that ingests a large e-commerce CSV dataset (Olist Brazilian E-Commerce) into a PostgreSQL database.

The entire system is orchestrated with docker-compose, allowing it to be built and run with a single command.

## Tech Stack

* **Docker & Docker-Compose:** To containerize and orchestrate all services.
* **Python:** For the data ingestion script.
* **Pandas:** For reading the large CSV in chunks and transforming data (e.g., converting to `datetime`).
* **SQLAlchemy:** To connect to and load data into PostgreSQL.
* **PostgreSQL:** As the destination data warehouse.
* **pgAdmin:** As a web-based GUI to connect to and explore the database.

## 🏗️ Project Architecture

This pipeline is defined in the `docker-compose.yaml` file and consists of three main services:

1.  **`pg-ecommerce-db` (PostgreSQL):**
    * A `postgres:13` container that runs the database.
    * Its data is made persistent by mounting a local volume (`./ecommerce-data`), so the data is not lost when the container stops.
    * It runs on a private virtual network (`data-network`).

2.  **`pgadmin` (pgAdmin 4):**
    * A `dpage/pgadmin4` container that runs the pgAdmin web interface.
    * It connects to the `data-network` so it can "see" the `pg-ecommerce-db` service.
    * It is exposed on `http://localhost:8080`.

3.  **`ingest-service` (Python Script):**
    * A custom container built from the `Dockerfile` in this project.
    * It runs the `ingest_data.py` script.
    * It connects to the database using the service name (`pg-ecommerce-db`) as its host.
    * It reads the `olist_orders_dataset.csv` in chunks of 100,000 rows, converts date columns, and loads them into the `orders` table.

## ⚙️ How to Run

**Prerequisites:**
* You must have Docker and Docker-Compose installed.

**Instructions:**

1.  **Download the Data:**
    This project uses the [Olist E-Commerce Dataset from Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce). You must download the data and place the `olist_orders_dataset.csv` file in this project's root folder.

2.  **Build and Run the Pipeline:**
    Run the following single command from your terminal (PowerShell is recommended on Windows). This will build the Python image, start the database & pgAdmin, and then run the ingestion script.

    ```powershell
    docker-compose up --build
    ```

## How to connect to pgadmin and see your data in action

1.  **Use pgAdmin:**
    * Once the pipeline is running, open your web browser and go to: `http://localhost:8080`
    * **Login Email:** `admin@admin.com`
    * **Login Password:** `root`
    * On the dashboard, click **Add Server**.
    * **General tab:** Give it a name (e.g., `My E-Commerce DB`).
    * **Connection tab:**
        * **Host:** `pg-ecommerce-db`
        * **Port:** `5432`
        * **Database:** `ecommerce`
        * **User:** `root`
        * **Password:** `root`
    * Click **Save**. You can now browse the `ecommerce` database and see your `orders` table populated with data

<img width="1918" height="893" alt="Screenshot 2025-11-13 174659" src="https://github.com/user-attachments/assets/5932f4e9-01b1-4b9f-9f2c-98784cd8660c" />
