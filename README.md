# ServiceNow AI Agent  
AI Agent that integrates with ServiceNow to categorize incident reports using OpenAI’s API.  
This project demonstrates how to integrate an AI Agent with ServiceNow using the Table REST API.  
The agent automatically classifies new IT incidents based on their short description and updates ServiceNow with the correct category and a comment.  

---

## Features
- Fetch **active incidents** from ServiceNow where the category is **blank** or defaulted to **Inquiry / Help** (`inquiry` in DB).
- Sorts by **newest incidents first** so recent issues get priority.
- Skips incidents that already contain an `[AI_AGENT]` classification comment (idempotent).
- Classify incidents into correct categories using **OpenAI GPT-4o-mini**.
- Update ServiceNow with the chosen category.

---

## Tech Stack
- Python 3  
- ServiceNow Developer Instance  
- ServiceNow Table API  
- OpenAI API  

---

## Example Flow
1. User creates a new incident in ServiceNow (default category: **Inquiry / Help**).  
2. The AI Agent retrieves incidents with `category=` (empty) or `category=inquiry`.  
3. The description is classified into categories:  
   - **Inquiry / Help**  
   - **Hardware**  
   - **Software**  
   - **Network**  
   - **Database**  
   - **Password Reset**  
4. ServiceNow is updated with:  
   - Correct category.  
   - Comment noting the AI’s decision. 

## Getting Started

### 1. Clone the Repo
```bash
git clone https://github.com/yourname/servicenow-ai-agent.git
cd servicenow-ai-agent
```

### 2. Set Up a ServiceNow Developer Instance

Sign up at developer.servicenow.com

Get your instance URL, admin username, and password.

### 3. Environment Variables

Set your secrets as environment variables:

Windows PowerShell (temporary session):
```bash
$env:OPENAI_API_KEY="sk-your-key"
$env:SNOW_INSTANCE="https://dev12345.service-now.com"
$env:SNOW_USERNAME="admin"
$env:SNOW_PASSWORD="yourpassword"
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Script
```bash
python classify_tickets.py
```

## Verifying Incident Updates
### 1. View incidents in your ServiceNow instance:
```bash
https://dev12345.service-now.com/now/nav/ui/classic/params/target/incident_list.do
```

### 2. Search by incident number (e.g., INC0010004).

### 3. Open the record and check the Category field.
Set it manually to Inquiry / Help (or leave blank) for testing.

### 4. Run the Python script.

### 5. Check incident page and the category should be updated with a comment.

## REST API Explorer
```bash
https://dev12345.service-now.com/now/nav/ui/classic/params/target/$restapi.do
```