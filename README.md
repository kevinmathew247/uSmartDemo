# uSmart Technical Task

This project is a technical task to demonstrate how to consume data from a CSV file, perform basic outlier detection, and insert the data into a PostgreSQL database. The application is containerized using Docker.

## Prerequisites

- Docker

## Setup and Running the Application

1. Clone the repository:

   gh repo clone kevinmathew247/uSmartDemo

2. Set Up a Virtual Environment

It is recommended to use a virtual environment to manage dependencies.

For Windows:
```
python -m venv venv
venv\Scripts\activate
```

For MacOS/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

3. Install Dependencies

With the virtual environment activated, install the required dependencies:
```
pip install -r requirements.txt
```

4. Configure the Database

Ensure that PostgreSQL is installed and running. Update the DATABASE_URL in the app.py file with your PostgreSQL credentials:
```
DATABASE_URL = "postgresql://postgres:password@postgres:5432/postgres"
```


5.	Build and start the Docker containers:

    docker-compose up --build

6.	The Flask application will be available at http://localhost:4000.

7. Test the Application

Open your browser and go to http://localhost:4000/test to ensure the application is running.

## Usage

1.	Open Postman or any other API client.
2.	Use the POST method to upload a CSV file to http://localhost:4000/upload as shown below. 

If there are no outliers present the file will upload with a response message 'File successfully processed and inserted into the database'.

![alt text](./images/1665CDD4-7805-4C31-9723-A1F303F40B1D.jpeg)

If there are any outliers in the file, then the error 'Outliers detected' will be returned as shown below.

![alt text](./images/4470740E-0C3B-4835-BEE1-4B6984F03B7A.jpeg)

To view the new table follow the steps below:

Step 1: List Running Containers
```
docker ps
```

This command will list all running Docker containers. Look for the PostgreSQL container and note its container ID or name.

Step 2: Access the PostgreSQL Container
Use the container ID or name from the previous step to access the container.
```
docker exec -it < container_id_or_name> bash
```
Replace the ‹container_id_or_name> with the actual ID or name of your PostgreSQL container.

Step 3: Connect to PostgreSQL Database
Inside the container, connect to the PostgreSQL database using the psql command-line tool:
```
psql -U postgres -d postgres
```

• -U postgres specifies the PostgreSQL user (in this case, postgres).
• -d postgres specifies the database to connect to (in this case I have set that also as postgres).

Step 4: List Tables
Once connected to the database, list all tables:
```
\dt
```

Step 5: Query the Table

To view data in the uploaded _data table:

```
SELECT * FROM uploaded_data;
```



![alt text](./images/FF612435-333E-4BBC-8849-0863C915AB9C.jpeg)

Below is an image of the column types created in the new table:

![alt text](./images/48251DC9-5B48-4306-BD70-F668C7FBAF66_4_5005_c.jpeg)

which can be viewed by running the command:

```
\d+ uploaded_data 
```
## Testing

Two test CSV files are provided in the tests directory:

	•	test_1.csv: A valid file with no outliers.
	•	test_2.csv: A file with an outlier.