import os, requests, time

def main(event):
  token = os.getenv("ChatGPT")
  cnotes = event.get('inputFields').get('cNotes')
  tnotes = event.get('inputFields').get('tNotes')
  mnotes = event.get('inputFields').get('mNotes')
  prePerText = "I want you to generate summary like this. (This is an example) -> churn reason in the first line based on these options: Company Shut Down, Lack of Funding Pricing Issues, Service Issues, ICP Misfit, Hired In-House Team, Moved to NetSuite, Moved to Competitor, Zeni's Decision, Company Sold, Controller Issue, 11:43, So it should look more like: Pricing Issues Customer XYZ, a SaaS company in the healthcare sector, churned due to pricing concerns. Despite initial satisfaction with our product's features, their needs shifted towards a lower-cost solution as they scaled operations. The primary decision driver was budget constraints, compounded by competition offering similar functionality at a reduced price. Previous attempts to address their concerns with custom pricing were unsuccessful, as they were seeking a more cost-efficient long-term option. No technical or support-related issues were reported. Potential future win-back if their financial situation improves."
  preText = prePerText + "Based on above example, please generate a 250 maximum character summary for this information. Be careful to understand the entire context, as a previous churn ticket was incorrectly tagged as Company Shut Down even though it was Company Sold." + "I have extracted following ticket information i.e. company notes,ticket notes and meetings notes. I want you to summarise why this is churn?"
  postText = " Just write the summary and do not enter anything like here's the summary. go straight into summary. First line should be the suggested churn reason based on the given data."
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
    'max_tokens': 200
  }
  time.sleep(5)
  response = requests.post(openai_endpoint, headers=headers, json=data)
  print(response.status_code)
  conclusion = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
  recommendedreason = conclusion.split('\n')[0]
  conclusion = "\n".join(conclusion.split('\n')[1:])
  return {
    "outputFields": {
      "conclusion": conclusion,
    }
  }