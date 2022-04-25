import requests
import csv


# First test with curl:
# curl.exe https://domain.zendesk.com/api/v2/views.json -v -u username/token:password

# Settings
auth = 'username', 'token'
view_tickets = []
view_id = 'view_id'
your_domain = 'domain'

# List tickets from a View
print(f'Getting tickets from view ID {view_id}')
url = f'https://{your_domain}.zendesk.com/api/v2/views/{view_id}/tickets.json'
while url:
   response = requests.get(url, auth=auth)
   print(response)
   page_data = response.json()
   print(page_data)
   tickets = page_data['tickets']     # extract the "tickets" list from the page
   view_tickets.extend(tickets)
   url = page_data['next_page']

# Initialize rows with an initial header row
rows = [('Ticket ID', 'Subject', 'Requester ID',
        'Assignee ID', 'Created', 'Status', 'URL')]

# Define a row per ticket and append
for ticket in view_tickets:
   row = (
       ticket['id'],
       ticket['subject'],
       ticket['requester_id'],
       ticket['assignee_id'],
       ticket['created_at'],
       ticket['status'],
       f'https://support.zendesk.com/agent/tickets/{ticket["id"]}'
   )
   rows.append(row)

with open('tickets.csv', mode='w', newline='') as csv_file:
   report_writer = csv.writer(csv_file, dialect='excel')
   for row in rows:
       report_writer.writerow(row)