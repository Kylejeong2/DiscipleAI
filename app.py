import os
import asyncio
from dotenv import load_dotenv
from google.cloud import aiplatform
from google.cloud.sql.connector import Connector
from langchain.embeddings import VertexAIEmbeddings
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.llms import VertexAI
from langchain import PromptTemplate
import asyncpg
from pgvector.asyncpg import register_vector

def app(user_query):
    print(f"received query: {user_query}")
    load_dotenv()

    project_id = os.getenv("project_id")
    database_password = os.getenv("database_password")
    region = os.getenv("region")
    instance_name = os.getenv("instance_name")
    database_name = os.getenv("database_name")
    database_user = os.getenv("database_user")

    # Initialize the AI Platform
    aiplatform.init(project=project_id, location=region)

    # user_query = "Where does it say that Jesus is God?" # example question

    embeddings_service = VertexAIEmbeddings()
    qe = embeddings_service.embed_query([user_query])

    matches = []

    # RAG with Postgres 
    async def main():
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

            await register_vector(conn)
            similarity_threshold = 0.1
            num_matches = 10

            # Find similar products to the query using cosine similarity search
            # over all vector embeddings. This new feature is provided by `pgvector`.
            results = await conn.fetch(
                """
                    WITH vector_matches AS (
                        SELECT row_id, 1 - (embedding <=> $1) AS similarity
                        FROM bible_embeddings
                        WHERE 1 - (embedding <=> $1) > $2
                        ORDER BY similarity DESC
                        LIMIT $3
                    )
                    SELECT row_id, content FROM bible_embeddings
                    WHERE row_id IN (SELECT row_id FROM vector_matches)
                """,
                qe,
                similarity_threshold,
                num_matches
            )

            if len(results) == 0:
                raise Exception("Did not find any results. Adjust the query parameters.")

            for r in results:
                # Collect the description for all the matched similar toy products.
                matches.append(
                    f"""The scripture passage is taken from {r["row_id"]}. While the text itself says: {r["content"]}."""
                )

            await conn.close()

    # Run the SQL commands now.
    asyncio.run(main())  # type: ignore
    print(matches)

    # Using LangChain for summarization and efficient context building.

    # could use OpenAI llm ? 
    llm = VertexAI(
        model_name='text-bison',
        max_output_tokens=2048
    )
    # Alternative models:
    # llm = VertexAI(model_name='text-bison-32k')

    map_prompt_template = """
                You will be given a bible verse and some text.
                The text is enclosed in triple backticks (```)
                ```{text}```
                SUMMARY:
                """

    map_prompt = PromptTemplate(template=map_prompt_template, input_variables=["text"])

    combine_prompt_template = """
                    You will be given a bible verse, some text
                    and a question enclosed in double backticks(``).
                    Based on the given text, answer the following
                    question in as much detail as possible.
                    You may include the bible verse in your description, but it is not compulsory.
                    Do not repeat the bible verse as the answer.
                    Your description should be done in such a way that it answers the question.

                    Description:
                    ```{text}```


                    Question:
                    ``{user_query}``


                    Answer:
                    """

    combine_prompt = PromptTemplate(
        template=combine_prompt_template, input_variables=["text", "user_query"]
    )

    docs = [Document(page_content=t) for t in matches]

    chain = load_summarize_chain(
        llm, chain_type="map_reduce", map_prompt=map_prompt, combine_prompt=combine_prompt
    )
    print(f"Retrieved {len(docs)} documents for query: {user_query}")
    if docs:
        answer = chain.run(
            input_documents=docs,
            question=user_query,
            user_query=user_query
        )
    else:
        answer = "I'm sorry, but I couldn't find any relevant information to answer your question."

    print(answer)
    return(answer)

# display(Markdown(answer))

# app("Who are the 12 disciples?") #testing