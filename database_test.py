import asyncio
import asyncpg
from google.cloud.sql.connector import Connector
from dotenv import load_dotenv
import os

load_dotenv()

project_id = os.getenv("project_id")
database_password = os.getenv("database_password")
region = os.getenv("region")
instance_name = os.getenv("instance_name")
database_name = os.getenv("database_name")
database_user = os.getenv("database_user")


async def query_first_5_rows():
    loop = asyncio.get_running_loop()
    async with Connector(loop=loop) as connector:
        # Create connection to Cloud SQL database.
        conn: asyncpg.Connection = await connector.connect_async(
            f"{project_id}:{region}:{instance_name}",  # Cloud SQL instance connection name
            "asyncpg",
            user=f"{database_user}",
            password=f"{database_password}",
            db=f"{database_name}",
        )

        # Query the first 5 rows from the table
        result = await conn.fetch("SELECT * FROM bible_embeddings LIMIT 5")

        # Display the result
        for row in result:
            print(row)

        await conn.close()

# Run the query
if __name__ == "__main__":
    asyncio.run(query_first_5_rows())  # type: ignore