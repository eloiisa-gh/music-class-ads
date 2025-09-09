import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext

from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from google import genai
from google.genai import types

load_dotenv()

project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
client = genai.Client(vertexai=True,
    project=project_id,
    location=os.getenv("GOOGLE_CLOUD_LOCATION")
)


# Tools

def generate_image(
    prompt: str) -> dict[str, str]:
    """Generate an illustration or diagram to support text.

    Args:
        prompt (str): the prompt to provide to an image generation model

    Returns:
        dict[str, str]: {"generation_response": "RESPONSE"}
    """

    bucket_name = f"gs://{project_id}-bucket"

    generation_response = client.models.generate_images(
        model=os.getenv("IMAGE_MODEL"),
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            negative_prompt="text",
            safety_filter_level="BLOCK_MEDIUM_AND_ABOVE",
            person_generation="ALLOW_ADULT",
            output_gcs_uri=bucket_name
        ),
    )
    blob_name = "/".join(generation_response.generated_images[0].image.gcs_uri.split("/")[-2:])
    url = "https://storage.cloud.google.com/" + bucket_name.split("/")[-1] + "/" + blob_name + "?authuser=1"
    return {"image_url": url}


# Agents

root_agent = Agent(
    name="illustration_agent",
    model=os.getenv("MODEL"),
    description="Creates branded illustrations.",
    instruction="""
    You are an illustrator for a stadium maintenance company.

    You will receive a block of text, it is your job to write
    a prompt that will express the ideas of this text.

    You always emphasize that there should be no text in the image.
    You prefer a flat, geometric, corporate memphis diagrammatic style of art.
    Your brand palette is purple (#BF40BF), green (#DAF7A6), and sunset colors.
    Consider a clever or charming approach with specific details.
    Incorporate stadium imagery like lights, yardage indicators, green fields, popcorn.
    Incorporate maintenance imagery like wrenches, toolboxes, overalls.
    Incorporate general sports imagery like balls, caps, gloves.

    Once you have written the prompt, use your 'generate_image' tool to generate an image.
    Always return both of the following:
        - the text of the prompt you used
        - the generated image URL returned by your tool
    """,
    tools=[generate_image]
)
