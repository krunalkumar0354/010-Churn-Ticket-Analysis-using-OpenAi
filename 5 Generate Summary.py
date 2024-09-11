import os, requests, time

def main(event):
    token = os.getenv("ChatGPT")
    cnotes = event.get('inputFields').get('cNotes')
    tnotes = event.get('inputFields').get('tNotes')
    mnotes = event.get('inputFields').get('mNotes')
    name = event.get('inputFields').get('name')
    prePerText = f"I want you to generate a summary like this. (This is an example) -> churn reason in the first line based on these options: Company Shut Down, Lack of Funding, Pricing Issues, Service Issues, ICP Misfit, Hired In-House Team, Moved to NetSuite, Moved to Competitor, Zeni's Decision, Company Sold, Controller Issue, 11:43, and next line separated by new line character \n should be the summary. So it should look more like: Pricing Issues. {name}, a SaaS company in the healthcare sector, churned due to pricing concerns. Despite initial satisfaction with our product's features, their needs shifted towards a lower-cost solution as they scaled operations. The primary decision driver was budget constraints, compounded by competition offering similar functionality at a reduced price. Previous attempts to address their concerns with custom pricing were unsuccessful, as they were seeking a more cost-efficient long-term option. No technical or support-related issues were reported. Potential future win-back if their financial situation improves."
    preText = prePerText + f" Based on the above example, please generate a 250 maximum character summary for this information. Be careful to understand the entire context. {name} has the following ticket information: company notes, ticket notes, and meeting notes. Summarize why this company churned."
    postText = " Just write the summary and do not enter anything like here's the summary. Go straight into the summary. The first line should be the suggested churn reason based on the given data."
    if cnotes == None:
        finalText = preText + " Company Notes ->" + "No Company Notes."
    else:
        finalText = preText + " Company Notes ->" + cnotes
    if tnotes == None:
        finalText = finalText + " Ticket Notes ->" + "No Ticket Notes."
    else:
        finalText = finalText + " Ticket Notes ->" + tnotes
    if mnotes == None:
        finalText = finalText + " Meeting Notes ->" + "No Meeting Notes." + postText
    else:
        finalText = finalText + " Meeting Notes ->" + mnotes + postText
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
    time.sleep(3)
    response = requests.post(openai_endpoint, headers=headers, json=data)
    conclusion = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
    recommendedreason = conclusion.split('.')[0]
    conclusion = " ".join(conclusion.split('.')[1:])
    return {
        "outputFields": {
            "conclusion": conclusion,
        }
    }