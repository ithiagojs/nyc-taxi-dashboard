import duckdb as dd

RAW_DATA_PATH = 'yellow_tripdata_*.csv'
FULL_OUTPUT = 'dados_taxi_processados.parquet'
SAMPLE_OUTPUT = 'dados_amostra.parquet'
ROW_LIMIT = 500000
SAMPLE_SIZE = 150000


def process_taxi_data():
    con = dd.connect(database=':memory:')

    query = f"""
        SELECT
            *,
            date_diff('minute', tpep_pickup_datetime, tpep_dropoff_datetime) AS duration_minutes,
            (trip_distance / (NULLIF(duration_minutes, 0) / 60.0)) AS avg_speed_mph
        FROM read_csv_auto('{RAW_DATA_PATH}', union_by_name=True)
        WHERE passenger_count > 0
          AND trip_distance > 0
          AND fare_amount > 0
          AND pickup_longitude BETWEEN -74.3 AND -73.6
          AND pickup_latitude BETWEEN 40.5 AND 40.9
          AND duration_minutes BETWEEN 1 AND 180
        LIMIT {ROW_LIMIT}
    """

    con.sql(f"CREATE TABLE taxi_data AS {query}")
    con.sql(f"COPY taxi_data TO '{FULL_OUTPUT}' (FORMAT PARQUET)")
    con.sql(f"COPY (SELECT * FROM taxi_data USING SAMPLE {SAMPLE_SIZE} ROWS) TO '{SAMPLE_OUTPUT}' (FORMAT PARQUET)")

    print(f"Sucesso: {FULL_OUTPUT} e {SAMPLE_OUTPUT} gerados.")
    con.table('taxi_data').project('duration_minutes, avg_speed_mph, trip_distance').limit(5).show()


if __name__ == "__main__":
    process_taxi_data()
