from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

app = Flask(__name__)

# Database configuration
DATABASE_URL = "postgresql://postgres:password@postgres:5432/postgres"

# SQLAlchemy base
Base = declarative_base()

# Define your SQLAlchemy model
class UploadedData(Base):
    __tablename__ = 'uploaded_data'

    id = Column(Integer, primary_key=True)
    timestamp_column = Column(DateTime)  # Use DateTime for timestamp column
    value = Column(Integer)
    category = Column(String)

# Create engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    df = pd.read_csv(file)

    # Perform outlier detection and schema inference
    if detect_outliers(df):
        return "Outliers detected", 400

    table_name = 'uploaded_data'

    # Create the table if it doesn't exist
    Base.metadata.create_all(engine)

    # Insert data into the database
    insert_data(df, table_name)

    return "File successfully processed and inserted into the database", 200

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'Test route'}), 200

def detect_outliers(df):
    # Use IQR method to detect outliers
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        if ((df[col] < lower_bound) | (df[col] > upper_bound)).any():
            return True
    return False

def insert_data(df, table_name):
    # Detect the format of the timestamp column
    timestamp_column = df.columns[df.columns.str.contains('timestamp', case=False)].tolist()[0]
    timestamp_format = detect_timestamp_format(df[timestamp_column])

    # Convert timestamp column to datetime format using the detected format
    df[timestamp_column] = pd.to_datetime(df[timestamp_column], format=timestamp_format)
    
    # Convert DataFrame to list of dictionaries
    data_to_insert = df.to_dict(orient='records')

    # Bulk insert into the database using SQLAlchemy
    session.bulk_insert_mappings(UploadedData, data_to_insert)
    session.commit()

def detect_timestamp_format(series):
    # Attempt to detect the format of timestamps in the series
    formats_to_check = ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M', '%Y-%m-%d']
    for fmt in formats_to_check:
        try:
            pd.to_datetime(series, format=fmt)
            return fmt
        except ValueError:
            continue
    # If no format is detected, raise an error or handle as necessary
    raise ValueError("Timestamp format not detected or not supported")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)