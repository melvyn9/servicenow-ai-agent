# ServiceNow AI Agent
AI Agent that integrates with ServiceNow to categorize incident reports using OpenAI’s API.
This project demonstrates how to integrate an AI Agent with ServiceNow using the Table REST API.  
The agent automatically classifies new IT incidents based on their short description and updates ServiceNow with the category and a comment.

## Features
- Fetch uncategorized incidents from ServiceNow via REST API
- Classify incidents (AI-powered classification coming soon, placeholder random for now)
- Update incidents with the chosen category and add AI comments
- Built with Python and easily extendable

## Tech Stack
- Python 3
- ServiceNow Developer Instance
- REST API (GET/PATCH)
- [OpenAI API](https://platform.openai.com/) (planned integration)

## Example Flow
1. User creates a new incident in ServiceNow.
2. The AI Agent retrieves the uncategorized incident.
3. The description is classified into categories: `network`, `hardware`, `software`, `inquiry`.
4. ServiceNow is updated with the category and a comment:
   > "AI Agent classified this as Networking"

## Getting Started
1. Clone this repo.
2. Set up a ServiceNow developer instance.
3. Update `INSTANCE_URL`, `USERNAME`, `PASSWORD` in `classify_tickets.py`.
4. Install dependencies: `pip install -r requirements.txt`
5. Run the script: `python classify_tickets.py`

## Next Steps
- Replace placeholder classification with GPT-based NLP.
- Deploy as a GitHub Action to run automatically every 15 minutes.
