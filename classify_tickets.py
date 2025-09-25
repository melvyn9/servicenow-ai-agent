import os
import requests
from openai import OpenAI

# ==============================
# CONFIGURATION
# ==============================
INSTANCE_URL = os.getenv("SNOW_INSTANCE")
USERNAME = os.getenv("SNOW_USERNAME")
PASSWORD = os.getenv("SNOW_PASSWORD")

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Allowed ServiceNow categories
CATEGORIES = ["Inquiry / Help", "Hardware", "Software", "Network", "Database", "Password Reset"]

# ==============================
# STEP 1. GET UNCATEGORIZED INCIDENTS
# ==============================
def get_uncategorized_incidents(limit=10):
    url = f"{INSTANCE_URL}/api/now/table/incident"
    # (category blank OR inquiry) AND active=true, ordered by newest
    query = {
        "sysparm_query": "(category=^ORcategory=inquiry)^active=true^ORDERBYDESCsys_created_on",
        "sysparm_fields": "sys_id,number,short_description,category",
        "sysparm_limit": limit
    }
    response = requests.get(url, auth=(USERNAME, PASSWORD), params=query)
    response.raise_for_status()
    return response.json().get("result", [])

# Skips already categorized incidents using comments
def has_ai_comment(sys_id: str) -> bool:
    url = f"{INSTANCE_URL}/api/now/table/sys_journal_field"
    query = {
        "sysparm_query": f"element_id={sys_id}^element=comments^valueLIKE[AI_AGENT]",
        "sysparm_fields": "sys_id",
        "sysparm_limit": 1
    }
    r = requests.get(url, auth=(USERNAME, PASSWORD), params=query)
    r.raise_for_status()
    return len(r.json().get("result", [])) > 0

# ==============================
# STEP 2. CLASSIFY INCIDENT (placeholder AI logic)
# ==============================
def classify_incident(description):
    prompt = f"""
    You are an AI agent classifying IT support incidents.
    Choose one category for this description: "{description}"
    Categories: Inquiry / Help, Hardware, Software, Network, Database, Password Reset
    Answer with only the category name.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=10
    )
    category_raw = response.choices[0].message.content.strip()

    # Normalize answer (lowercase, strip spaces)
    category_normalized = category_raw.lower().replace("-", "").strip()

    # Mapping dictionary
    CATEGORY_MAP = {
        "inquiry": "Inquiry / Help",
        "inquiry / help": "Inquiry / Help",
        "help": "Inquiry / Help",
        "hardware": "Hardware",
        "software": "Software",
        "network": "Network",
        "database": "Database",
        "password reset": "Password Reset",
        "password": "Password Reset",
    }

    # Use mapped value or fallback
    return CATEGORY_MAP.get(category_normalized, "Inquiry / Help")

# ==============================
# STEP 3. UPDATE INCIDENT
# ==============================
def update_incident(sys_id, category):
    url = f"{INSTANCE_URL}/api/now/table/incident/{sys_id}"
    payload = {
        "category": category,
        "comments": f"[AI_AGENT] Classified this as {category}"
    }
    r = requests.patch(url, auth=(USERNAME, PASSWORD), json=payload)
    r.raise_for_status()
    return r.json()

# ==============================
# MAIN FLOW
# ==============================
if __name__ == "__main__":
    incidents = get_uncategorized_incidents(limit=3)
    if not incidents:
        print("No uncategorized incidents found.")
    else:
        for inc in incidents:
            if has_ai_comment(inc["sys_id"]):
                print(f"Skipping {inc['number']} (already AI-classified)")
                continue

            print(f"\nClassifying Incident {inc['number']}: {inc['short_description']}")
            category = classify_incident(inc['short_description'])
            print(f" → Assigned Category: {category}")
            updated = update_incident(inc['sys_id'], category)
            print(f"Updated Incident {updated['result']['number']} with category {updated['result']['category']}")
