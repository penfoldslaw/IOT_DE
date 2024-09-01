from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from uuid import uuid4

# Connecting to the Docker container
cluster = Cluster(['localhost'], port=9042)
session = cluster.connect()

# Creating a keyspace (if not already created)
session.execute("""
CREATE KEYSPACE IF NOT EXISTS telemetry_keyspace
WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
""")

session.execute("DROP TABLE IF EXISTS telemetry_keyspace.f1_data;")
session.execute("DROP TABLE IF EXISTS telemetry_keyspace_1.f1_data_1;")


# Creating a table
session.execute("""
CREATE TABLE IF NOT EXISTS telemetry_keyspace.f1_data (
    uuid UUID PRIMARY KEY,
    id INT,
    timestamp TEXT,
    rpm INT,
    gear INT,
    steer INT,
    throttle_position INT,
    brake INT,
    front_left_temp INT,
    front_right_temp INT,
    rear_left_temp INT,
    rear_right_temp INT
);
""")

# Insert data into the f1_data table
# session.execute("""
# # INSERT INTO telemetry_keyspace_1.f1_data_1 (uniq, id, timestamp, rpm, gear, steer, throttle_position, brake, front_left_temp, front_right_temp, rear_left_temp, rear_right_temp)
# # VALUES (%s, 2, '2024-08-25T00:14:59.971164Z', 7159, 6, -105, 16, 26, 82, 3, 42, 59);
# # """, (uuid4(),))

# Query and print the data
rows = session.execute('SELECT * FROM telemetry_keyspace.f1_data')
for row in rows:
    print(row)

cluster.shutdown()
