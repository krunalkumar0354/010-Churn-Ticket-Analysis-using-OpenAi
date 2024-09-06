import os, requests

def main(event):
  token = os.getenv("ChatGPT")
  notes = event.get('inputFields').get('notes')
  meetings = event.get('inputFields').get('meeting_notes')
  preText = "I have extracted following ticket information i.e. ticket notes and meetings notes. I want you to summarise why this is churn?"
  postText = " Just write the summary and do not enter anything like here's the summary. go straight into summary."
  finalText = preText + "Ticket Notes ->" + notes + "Meeting Notes ->" + meetings + postText
  openai_endpoint = 'https://api.openai.com/v1/chat/completions'
  headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
  }
  data = {
    'model': 'gpt-4',
    'messages': [
      {
        'role': 'user',
        'content': finalText
      }
    ],
    'max_tokens': 500
  }
  response = requests.post(openai_endpoint, headers=headers, json=data)
  print(response.status_code)
  conclusion = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
  return {
    "outputFields": {
      "conclusion": conclusion
    }
  }