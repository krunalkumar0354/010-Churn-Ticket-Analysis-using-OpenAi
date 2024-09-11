import os, requests, time

def main(event):
  token = os.getenv("ChatGPT")
  summary = event.get('inputFields').get('conclusion')
  correctness = event.get('inputFields').get('Correctnss')
  preText = "Select one recommended churn reason from these options: Company Shut Down, Lack of Funding, Pricing Issues, Service Issues, ICP Misfit, Hired In-House Team, Moved to NetSuite, Moved to Competitor, Zeni's Decision, Company Sold, Controller Issue."
  postText = "Here's the summary, by using which you can select the recommended churn reason as mentioned earlier. Summary = " + summary
  finalText = preText + postText + "Please take this correctness into account while generating recommended churn reason." + (correctness if correctness else "correctness is not provided.") + "do not prefix anything like Recommended Churn Reason, instead just mention the reason. If you cannot derive a reason, then do not provide any text."
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
    'max_tokens': 50
  }
  time.sleep(3)
  response = requests.post(openai_endpoint, headers=headers, json=data)
  reason = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
  return {
    "outputFields": {
      "RecommendedChurnReason": reason
    }
  }