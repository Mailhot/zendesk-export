import requests
import csv
import config
from time import sleep
import json

# First test with curl:
# curl.exe https://domain.zendesk.com/api/v2/views.json -v -u username/token:password

# Settings
auth = config.username, config.token
view_tickets = []
view_id = config.view_id
your_domain = config.your_domain

# ticket_id = 80




def get_tickets_comment(ticket_id):
   url2 = f'https://{your_domain}.zendesk.com/api/v2/tickets/{ticket_id}/comments'
   while url2:
      response = requests.get(url2, auth=auth)
      print(response)
      if response:
         page_data = response.json()
         print(page_data)
         return page_data
      else: 
         return None
   

def get_tickets():
   url = f'https://{your_domain}.zendesk.com/api/v2/tickets.json'
   output_tickets = {}
   output_tickets['tickets'] = []
   # while url:
   response = requests.get(url, auth=auth)
   page_data = response.json()
   print(page_data)
   print('')
   for ticket in page_data['tickets']:
      
      print(f"comments on ticket {ticket['id']}")
      sleep(7)
      comments = get_tickets_comment(ticket['id'])
      ticket['comments'] = comments
      output_tickets['tickets'].append(ticket)
      print(comments)
      print('')

   with open('tickets.json', mode='w', newline='\n') as the_file:
      json.dump(output_tickets, the_file)
      # report_writer = csv.writer(csv_file, dialect='excel')

def list_view_ticket(view_id):
   # List tickets from a View
   print(f'Getting tickets from view ID {view_id}')
   # url = f'https://{your_domain}.zendesk.com/api/v2/views/{view_id}/tickets.json'
   url = f'https://{your_domain}.zendesk.com/api/v2/tickets/{ticket_id}.json'

   while url:
      response = requests.get(url, auth=auth)
      print(response)
      page_data = response.json()
      print(page_data)
      tickets = page_data['tickets']     # extract the "tickets" list from the page
      view_tickets.extend(tickets)
      url = page_data['next_page']

def save_as_csv(data):
   # Initialize rows with an initial header row
   rows = [('Ticket ID', 'Subject', 'Requester ID',
           'Assignee ID', 'Created', 'Status', 'URL')]

   # Define a row per ticket and append
   for ticket in view_tickets:
      print('')
      print(ticket)

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

if __name__ == '__main__':
   get_tickets()
   # get_tickets_comment(375)