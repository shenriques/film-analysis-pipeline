'''
Script Summary:

1. create default airflow connections 
2. add custom aws-like connection (configures it to run with minio)
3. add custom spark connection for workflows
'''

import subprocess
import logging

# logging
logging.basicConfig(
    filename='logs/setup_airflow.log',
    level=logging.INFO,
    format='%(levelname)s @ %(asctime)s: %(message)s'
) 

# ensures airflows default connections are created in metadata database 
# airflow uses default connections (http default, smtp default etc) to do base functionality e.g. send email, access http endpoint
create_command = ["airflow", "connections", "create-default-connections"]
subprocess.run(create_command)

# defines a custom connection for an aws type service
conn_id = "aws_default"
conn_type = "aws"
access_key = "minio"
secret_key = "minio123"
region_name = "us-east-1"
endpoint_url = "http://minio:9000"


# Construct the extra JSON
extra = {
    "aws_access_key_id": access_key,
    "aws_secret_access_key": secret_key,
    "region_name": region_name,
    "host": endpoint_url,
}

# converts extra to JSON by ensuring double quotes are valid
extra_json = str(extra).replace("'", '"')

# adds a new connection to airflow using the CLI
command = [
    "airflow",
    "connections",
    "add",
    conn_id,
    "--conn-type",
    conn_type,
    "--conn-extra",
    extra_json,
]

subprocess.run(command)

# adds a connection for spark 
def add_airflow_connection():
    connection_id = "spark-conn"
    connection_type = "spark"
    host = "spark://192.168.0.1"
    port = "7077"
    cmd = [
        "airflow",
        "connections",
        "add",
        connection_id,
        "--conn-host",
        host,
        "--conn-type",
        connection_type,
        "--conn-port",
        port,
    ]

    result = subprocess.run(cmd, capture_output=True, text=True) # captures and formats output for logging
    if result.returncode == 0:
        logging.info(f"Successfully added {connection_id} connection")
    else:
        logging.info(f"ERROR: Failed to add {connection_id} connection due to: {result.stderr}")


add_airflow_connection()