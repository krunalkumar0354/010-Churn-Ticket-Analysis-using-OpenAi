import os, requests, time

def main(event):
  token = os.getenv("ChatGPT")
  reason = event.get('inputFields').get('churn_reason')
  category = event.get('inputFields').get('churn_category')
  summary = event.get('inputFields').get('conclusion')
  openai_endpoint = 'https://api.openai.com/v1/chat/completions'
  finalText = "I am sharing the summary. I want you to go through it and tell me whether the churn reason " + (reason if reason else "Reason Not Provided") + " is correct? The summary you need to go through to make a decision is " + (summary if summary else "Summary Not Provided") + ". Please answer in a short text, make sure you say yes and no for reason. Be careful to understand the entire context of the summary."
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
    'max_tokens': 100
  }
  time.sleep(3)
  response = requests.post(openai_endpoint, headers=headers, json=data)
  correctness = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
  return {
    "outputFields": {
      "Correctness": correctness
    }
  }