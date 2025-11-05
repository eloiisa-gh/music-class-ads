import os
import uuid
from dotenv import load_dotenv

# ADK imports
from google.adk import Agent
from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext

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
    description="Creates branded illustrations (prompts and pictures).",
    instruction="""
    You are an illustrator for a company that publicizes music classes by music teachers and academies.

    You will receive keywords or a short summary of the classes provided, it is your job to write
    a prompt that will express the ideas of this text.

    You always emphasize that there should be no text in the image.
    Use precise outlines, flat color fields, and minimal detail. Base the comic in simplicity emphasizing flatness and contrast. 
    Your brand style is inspired in the classic comic strips aesthetic from the modern art movement Pop Art, simulating mechanical printing, using bold outlines, dramatic compositions, sometimes exaggerated expressions, and Ben-Day Dots, resulting in a bright, artificial look. 
    Without text or speech bubbles. Produce only one main panel.
    Ensure the illustration depicts both male and female characters.
    Your palette is mainly bold primary colors mirroring the limited color palette of comic printing. Use this colors in a bright, saturated, vivid, and vibrant way.
    Consider a clever or charming approach with specific details.
    Incorporate music teaching imagery like music notation, teachers and young students.
    Incorporate musical imagery relevant to the prompt, like musical instruments (e.g.: piano, guitar, violin, flute, microphone).
    Incorporate general music playing imagery if relevant, like a singer, a musical group, a chorus, or speakers.

    Once you have written the prompt, use your 'generate_image' tool to generate an image.
    Always return both of the following:
        - the text of the prompt you used
        - the generated image URL returned by your tool
    """,
    tools=[generate_image]
)
