# from cassandra.cluster import Cluster
# from cassandra.auth import PlainTextAuthProvider

# # Connect to the Cassandra cluster running in Docker
# cluster = Cluster(['localhost'], port=9042)
# session = cluster.connect()

# # Example query: Create a keyspace (if not already created)
# session.execute("""
# CREATE KEYSPACE IF NOT EXISTS test_keyspace
# WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};
# """)

# # Example query: Create a table
# session.execute("""
# CREATE TABLE IF NOT EXISTS test_keyspace.users (
#     user_id UUID PRIMARY KEY,
#     name text,
#     age int
# );
# """)

# # Example query: Insert data
# session.execute("""
# INSERT INTO test_keyspace.users (user_id, name, age)
# VALUES (uuid(), 'Alice', 30);
# """)

# # Example query: Retrieve data
# rows = session.execute('SELECT * FROM test_keyspace.users')
# for row in rows:
#     print(row)

# # Close the connection
# cluster.shutdown()
