# ADK and A2A
Connect to remote agents with ADK and the Agent2Agent (A2A) SDK

Imagine you work for a stadium maintenance company: 'Cymbal Stadiums'. There is an image generation-agent that can create illustrations according to brand guidelines: 
- a specific illustration style: (Corporate Memphis / [Alegria](https://buck.co/work/facebook-alegria) art)
- a color palette (purples and greens on sunset gradients)
- examples of stadium/sports and maintenance imagery because it is a stadium maintenance company

Now, several different teams in the organization want to use it too.
you can deploy the agent once as an agent wrapped with an A2A server, and the other teams' agents can incorporate it by querying it remotely.


### Objective
- Deploy an ADK agent as an A2A Server
- Prepare a JSON Agent Card to describe an A2A agent's capabilities
- Enable another ADK agent to read the Agent Card of your deployed A2A agent and use it as a sub-agent


<details>
  <summary>Instructions</summary>

### 1. Install ADK and set up your environment
Enable the Vertex AI API and Cloud Run API:
```
gcloud services enable aiplatform.googleapis.com
```
```
gcloud services enable run.googleapis.com
```

Download and install the ADK and code samples:
```
# Install ADK and the A2A Python SDK
cd ~
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk==1.8.0 a2a-sdk==0.2.16
# Correcting a typo in this version
sed -i 's/{a2a_option}"/{a2a_option} "/' ~/.local/lib/python3.12/site-packages/google/adk/cli/cli_deploy.py
```

Copy the lab code from the Cloud Storage bucket and unzip it:
```
gcloud storage cp gs://YOUR_GCP_PROJECT_ID-bucket/adk_and_a2a.zip ./adk_and_a2a.zip
gcloud storage cp gs://adk-and-a2a-bucket/adk_and_a2a.zip ./adk_and_a2a.zip
unzip adk_and_a2a.zip
```

### 2. Explore the ADK agent you will make available remotely
Write and .env file to set environment variables needed by ADK agents in `illustration_agent` and in `slide_content_agent`: 
```
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=YOUR_GCP_PROJECT_ID
GOOGLE_CLOUD_LOCATION=GCP_LOCATION
MODEL="gemini-2.0-flash-001"
IMAGE_MODEL="imagen-3.0-generate-002"
```

From the Cloud Shell Terminal, launch the ADK dev UI with:
```
adk web
```
Output:
```
	INFO:     Started server process [3274]
	INFO:     Waiting for application startup.
	+-----------------------------------------------------------------------------+
	| ADK Web Server started                                                      |
	|                                                                             |
	| For local testing, access at http://localhost:8000.                         |
	+-----------------------------------------------------------------------------+
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Clicking the http://127.0.0.1:8000 link, open the ADK Dev UI. 
From the 'Select an agent' dropdown on the left, select 'illustration_agent' from the dropdown.


Query the agent with some text that could be used in a recruitment slide deck:
```
By supporting each other, we get big things done!
```

Resulting image:






</details>

