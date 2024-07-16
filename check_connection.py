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


async def main():
    # get current running event loop to be used with Connector
    loop = asyncio.get_running_loop()
    # initialize Connector object as async context manager
    async with Connector(loop=loop) as connector:
        # create connection to Cloud SQL database
        conn: asyncpg.Connection = await connector.connect_async(
            f"{project_id}:{region}:{instance_name}",  # Cloud SQL instance connection name
            "asyncpg",
            user=f"{database_user}",
            password=f"{database_password}",
            db=f"{database_name}"
            # ... additional database driver args
        )

        # query Cloud SQL database
        results = await conn.fetch("SELECT version()")
        print(results[0]["version"])

        # close asyncpg connection
        await conn.close()


if __name__ == "__main__":
    asyncio.run(main())