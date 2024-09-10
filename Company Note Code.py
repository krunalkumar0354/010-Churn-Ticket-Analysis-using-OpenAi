import requests, os, json, re

def get_notes_for_company(url, headers, company_id):
  after = 0
  notes = []
  while True:
    payload = {
      "filterGroups": [
        {
          "filters": [
            {
              "propertyName": "associations.company",
              "operator": "EQ",
              "value": company_id
            }
          ]
        }
      ],
      "properties": ["hs_note_body"],
      "limit": 200,
      "after": after
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
      data = response.json()
      notes.extend(data.get("results", []))
      if "paging" in data and "next" in data["paging"]:
        after = data["paging"]["next"]["after"]
      else:
        break
    else:
      print(f"Error: {response.status_code} - {response.text}")
      break
  return notes

def main(event):
  token = os.getenv("RevOps")
  cId = event.get("inputFields").get("cId")
  url = "https://api.hubapi.com/crm/v3/objects/notes/search"
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {token}"
  }
  notes = []
  noteswithextradata = get_notes_for_company(url, headers, cId)
  for note in noteswithextradata:
    note_body = note["properties"].get("hs_note_body", "No content")
    if type(note_body) != type(None):
      note_body = re.sub(r'<[^>]+>', '', note_body)
      note_body = re.sub(r'http\S+|www\.\S+', '', note_body)
      notes.append(note_body)
  return {
    "outputFields": {
      "CompanyNotes": notes
    }
  }