from pymilvus import connections, utility

def test_milvus_connection():
    try:
        # Connect to the Milvus server
        connections.connect("default", host="localhost", port=19530)
        print("✅ Connection to Milvus successful!")

        # Check if the connection is active
        if utility.get_server_version():
            print(f"Milvus server version: {utility.get_server_version()}")
        else:
            print("⚠️ Connection established but could not retrieve the server version.")

    except Exception as e:
        print(f"❌ Failed to connect to Milvus: {e}")

    finally:
        # Disconnect from the Milvus server
        connections.disconnect("default")
        print("Disconnected from Milvus.")

if __name__ == "__main__":
    test_milvus_connection()
