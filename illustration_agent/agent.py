import os
import uuid
from dotenv import load_dotenv

# ADK imports
from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from .agent_instructions import ILLUSTRATOR_DESCRIPTION, ILLUSTRATOR_INSTRUCTIONS

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from google import genai
from google.genai.types import GenerateContentConfig, ImageConfig
from google.cloud import storage 


load_dotenv()

# SDK Initialization
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
client = genai.Client(vertexai=True, project=project_id, location=location)


# Tool
def generate_image(prompt: str) -> dict[str, str]:
    """Generate an illustration and upload it to GCS using Gemini.

    Args:
        prompt (str): The prompt to provide to the image generation model.

    Returns:
        dict[str, str]: {"image_url": "The public URL of the generated image in GCS."}
    """
    # 1. Call the model
    response = client.models.generate_content(
        model=os.getenv("IMAGE_MODEL"),
        contents=prompt,
        config=GenerateContentConfig(
            response_modalities=["IMAGE"],
            image_config=ImageConfig(
                aspect_ratio="1:1",
            ),
            candidate_count=1,
        ),
    )

    # 2. Extract the raw image data from the response
    image_bytes = response.candidates[0].content.parts[0].inline_data.data

    # 3. Upload the image bytes to Google Cloud Storage
    storage_client = storage.Client(project=project_id)
    bucket_name = f"{project_id}-bucket"
    bucket = storage_client.bucket(bucket_name)
    
    # Generate a unique name for the image file
    blob_name = f"generated-images/{uuid.uuid4()}.png"
    blob = bucket.blob(blob_name)

    # Upload the data
    blob.upload_from_string(image_bytes, content_type="image/png")

    # 4. Construct and return the public URL
    url = f"https://storage.cloud.google.com/{bucket_name}/{blob_name}"

    return {"image_url": url}


# Agent
root_agent = Agent(
    name="illustration_agent",
    model=os.getenv("MODEL"),
    description=ILLUSTRATOR_DESCRIPTION,
    instruction=ILLUSTRATOR_INSTRUCTIONS,
    tools=[generate_image]
)
