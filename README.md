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
# Correcting a typo in this version
sed -i 's/{a2a_option}"/{a2a_option} "/' ~/.local/lib/python3.12/site-packages/google/adk/cli/cli_deploy.py
```

Set up the `.env` files. 

Create a Cloud Storage bucket: 'PROJECT_ID-bucket'.


### 2. Explore the ADK agent you will make available remotely

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

Clicking the [http://127.0.0.1:8000](https://8000-cs-331008850888-default.cs-us-east1-dogs.cloudshell.dev/dev-ui/) link, open the ADK Dev UI. 
From the 'Select an agent' dropdown on the left, select 'illustration_agent' from the dropdown.


<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/ADK_and_A2A_img01.png?raw" alt="illustration agent" width=75% height=75% />


Query the agent with some text that could be used in a recruitment slide deck:
```
By supporting each other, we get big things done!
```

Resulting image:

<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/ADK_and_A2A_sample_0.png?raw" alt="illustration agent result" width=40% height=40% />


### 3. Deploy the Agent as an A2A Server
Use `adk deploy cloud_run` with the `--a2a` flag to deploy your agent to Cloud Run as an A2A server.
- the `--project` and `--region` define the project and region in which the Cloud Run service will be deployed
- the `--service_name` defines the name for the Cloud Run service
- the `--a2a` flag indicates it should be hosted as an A2A agent. This means two things:
	- your agent will be wrapped by a class which bridges ADK and A2A agents: the A2aAgentExecutor. This class translates A2A Protocol's language of tasks and messages to an ADK Runner in its language of events.
	- the Agent Card will be hosted as well at CLOUD_RUN_URL/a2a/AGENT_NAME/.well-known/agent.json

Deploy the agent to Cloud Run as an A2A server:
```
adk deploy cloud_run \
    --project YOUR_GCP_PROJECT_ID \
    --region GCP_LOCATION \
    --service_name illustration-agent \
    --a2a \
    illustration_agent
```
Deployment should take about 5-10 minutes.
```
Service [illustration-agent] revision [illustration-agent-00001-xpp] has been deployed and is serving 100 percent of traffic.
Service URL: https://illustration-agent-ProjectNumber.GCP_LOCATION.run.app
```

### 4. Enable another ADK agent to call this agent remotely
Launch the UI from the Cloud Shell Terminal with:
```
cd ~/adk_and_a2a
adk web
```

Click the [http://127.0.0.1:8000](https://8000-cs-331008850888-default.cs-us-east1-dogs.cloudshell.dev/dev-ui/) link in the terminal output.
From the 'Select an agent' dropdown on the left, select 'slide_content_agent'. Query the agent with an idea for a slide:
```
Create content for a slide about our excellent on-the-job training.
```
Output: 
- a headline and body text written by the slide_content_agent itself 
- a call to transfer_to_agent, indicating a transfer to the illustration_agent
- the response from the illustration_agent with a link to the new image.

<img src="https://github.com/eloiisa-gh/adk_and_a2a/blob/main/ADK_and_A2A_img02.png?raw" alt="slide content agent result" width=75% height=75% />

</details>

