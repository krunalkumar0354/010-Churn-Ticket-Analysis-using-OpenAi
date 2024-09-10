import os, requests

def main(event):
  token = os.getenv("ChatGPT")
  cnotes = event.get('inputFields').get('cNotes')
  tnotes = event.get('inputFields').get('tNotes')
  mnotes = event.get('inputFields').get('mNotes')
  preText = "I have extracted following ticket information i.e. company notes,ticket notes and meetings notes. I want you to summarise why this is churn?"
  postText = " Just write the summary and do not enter anything like here's the summary. go straight into summary."
  if cnotes == None:
    finalText = preText + "Company Notes ->" + "No Company Notes."
  else:
    finalText = preText + "Company Notes ->" + cnotes
  if tnotes == None:
    finalText = finalText + "Ticket Notes ->" + "No Ticket Notes."
  else:
    finalText = finalText + "Ticket Notes ->" + tnotes
  if mnotes == None:
    finalText = finalText + "Meeting Notes ->" + "No Meeting Notes." + postText
  else:
    finalText = finalText + "Meeting Notes ->" + mnotes + postText
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