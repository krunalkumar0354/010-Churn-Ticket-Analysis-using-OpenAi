import os, requests, re

def get_ticket_notes(token, ticket_id, base_url, headers):
    url = base_url
    header = headers
    params = {
        'limit': 100
    }
    notes = []
    has_more = True
    offset = None
    while has_more:
        if offset:
            params['offset'] = offset
        response = requests.get(url, headers = header, params = params)
        if response.status_code != 200:
            print(f"Error: {response.status_code} - {response.text}")
            break
        data = response.json()
        for engagement in data.get('results', []):
            if engagement['engagement']['type'] == 'NOTE':
                note_body = engagement['metadata'].get('body', '')
                notes.append(note_body)
        has_more = data.get('hasMore', False)
        offset = data.get('offset')
    return notes

def main(event):
  token = os.getenv("RevOps")
  ticket_id = event.get('inputFields').get('hs_ticket_id')
  description = event.get('inputFields').get('content')
  reason = event.get('inputFields').get('churn_reason')
  category = event.get('inputFields').get('churn_category')
  base_url = f'https://api.hubapi.com/engagements/v1/engagements/associated/ticket/{ticket_id}/paged'
  headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
  }
  html_notes = ' '.join(get_ticket_notes(token, ticket_id, base_url, headers))
  notes = re.sub(r'<[^>]+>', '', html_notes)
  final_note = "Ticket Description = " + str(description) + ". Ticket Churn Reason = " + str(reason) + ". Ticket Churn Category = " + str(category) + ". Additional Notes added to the ticket = " + notes
  return {
    "outputFields": {
      "TicketNotes": final_note
    }
  }