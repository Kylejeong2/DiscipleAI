from google.cloud import aiplatform
from langchain.llms import VertexAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import os
import dotenv

dotenv.load_dotenv()

def generate_context(currContext, context): #string and list

    project_id = os.getenv("project_id")
    database_password = os.getenv("database_password")
    region = os.getenv("region")
    instance_name = os.getenv("instance_name")
    database_name = os.getenv("database_name")
    database_user = os.getenv("database_user")
    # Initialize VertexAI
    aiplatform.init(project=project_id, location=region)

    # Create VertexAI instance
    llm = VertexAI(
        model_name='text-bison',
        max_output_tokens=2048,
        temperature=0.6
    )

    # Combine the current context and new context
    if context:
        combined_context = currContext + " " + "previous question: " + context[0] + "; previous answer: " + context[1]
    else:
        combined_context = currContext

    # Create a prompt template for summarization
    prompt_template = """
    Summarize the following context in about 4 sentences:

    {text}

    Summary:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

    # Create a summarization chain
    chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)

    # Create a document from the combined context
    doc = Document(page_content=combined_context)

    # Generate the summary
    summary = chain.run([doc])
    print(summary)

    return summary