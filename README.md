# Music class ad generation agent 🎼

A company needs an agent for a project to publicize music classes. There is an image generation agent that can create illustrations according to the company's brand guidelines: 
- a specific illustration style: Pop Art comic strip panel
- a color palette: bold, saturated, mainly primary colors
- include musical and teaching imagery

This illustrator agent can then be incorporated by the ad content creator agent.


<details>
  <summary>Instructions</summary>

<details open>
  <summary>1. Install ADK and set up your environment</summary>

### 1. Install ADK and set up your environment
Enable the Vertex AI API and Cloud Run API:
```
gcloud services enable \
  aiplatform.googleapis.com \
  run.googleapis.com
```

Download and install the ADK:
```
# Install ADK and the A2A Python SDK
cd ~
export PATH=$PATH:"/home/${USER}/.local/bin"
python3 -m pip install google-adk==1.8.0 a2a-sdk==0.2.16
pip install --upgrade google-genai
# Correcting a typo in this version
sed -i 's/{a2a_option}"/{a2a_option} "/' ~/.local/lib/python3.12/site-packages/google/adk/cli/cli_deploy.py
```

Set up the `.env` files. 

Create a Cloud Storage bucket: 'PROJECT_ID-bucket'.

</details>


<details open>
  <summary>2. Explore the illustrations agent</summary>

### 2. Explore the illustrations agent

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
	| For local testing, access at http://localhost:8000.                         |
	+-----------------------------------------------------------------------------+
	INFO:     Application startup complete.
	INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

Clicking the [http://127.0.0.1:8000](https://8000-cs-70724c49-cfc8-4e60-b3d7-15a89c90e20e.cs-us-east1-pkhd.cloudshell.dev/dev-ui/) link, open the ADK Dev UI. 
From the 'Select an agent' dropdown on the left, select `illustration_agent`.

Query the agent with text related to music classes: `piano and violin`
<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/illustration_agent_pianoandviolin.png?raw" alt="illustration agent" width=75% height=75% />

Resulting image:
<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/illustration_agent_generated-images_pianoandviolin.png?raw" alt="illustration agent result" width=30% height=30% />

</details>


<details open>
  <summary>3. Deploy the illustration agent as an A2A Server</summary>

### 3. Deploy the illustration agent as an A2A Server
Use `adk deploy cloud_run` with the `--a2a` flag to deploy the agent to Cloud Run as an A2A server.
- `--project` and `--region` : where the Cloud Run service will be deployed
- the `--service_name` defines the name for the Cloud Run service
- the `--a2a` flag indicates it should be hosted as an A2A agent.

Deploy the illustration agent to Cloud Run as an A2A server:
```
adk deploy cloud_run \
    --project YOUR_GCP_PROJECT_ID \
    --region GCP_LOCATION \
    --service_name illustration-agent \
    --a2a \
    illustration_agent
```
Output: 
```
Service [illustration-agent] revision [illustration-agent-00001-xpp] has been deployed and is serving 100 percent of traffic.
Service URL: https://illustration-agent-ProjectNumber.GCP_LOCATION.run.app
```
We use this URL for the agent's url in the card (JSON) files.

</details>


<details open>
  <summary>4. Enable another agent to call the illustration agent remotely</summary>

### 4. Enable another agent to call the illustration agent remotely

This second agent creates content for ads. It writes a headline and a couple of sentences of body text, then transfer to the illustration agent to generate an image to illustrate that text.

Launch the UI from the Cloud Shell Terminal:
```
cd ~/adk_and_a2a
adk web
```

From the 'Select an agent' dropdown on the left, select `ad_content_agent`. Query the agent with an idea for an ad:
```
Create content for an ad about singing classes for beginners
```
Output: 
- a headline and body text written by the ad_content_agent
- a call to transfer_to_agent, indicating a transfer to the illustration_agent
- the response from the illustration_agent with a link to the new image.

Verify that `ad_content_agent` is using `illustration_agent` as a sub-agent: 
<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/ad_content_agent_singingbeginners.png?raw" alt="ad agent" width=75% height=75% />

Resulting image:
<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/ad_content_agent_generated-images_singingbeginners.png?raw" alt="ad agent result" width=30% height=30% />

</details>

</details>
