import requests
import csv
import config
from time import sleep
import json
import os

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

   response = requests.get(url2, auth=auth)
   print(response)
   if response:
      page_data = response.json()
      print(page_data)
      return page_data
   else: 
      return None
   

def get_comments_attachments(ticket_id):
   url = f'https://{your_domain}.zendesk.com/api/v2/tickets/{ticket_id}/comments'

   response = requests.get(url, auth=auth)
   sleep(7)
   page_data = response.json()
   if page_data.get('error'):
      print('Error encontered: ', page_data['error'])
      return None
   print('page_data')
   print(page_data)
   for comment in page_data['comments']:
      comment_id = comment['id']
      for attachment in comment['attachments']:
         # filename_out = f"{attachment['id']}_{attachment['file_name']}"
         filename_out = f"{attachment['file_name']}"

         content_url = attachment['content_url']

         response2 = requests.get(content_url)
         sleep(7)

         # create a ticket number path if it does not exist.
         path = f"./{ticket_id}"
         if not os.path.exists(path):
            os.makedirs(path)

         with open(f"./{ticket_id}/{filename_out}", "wb+") as the_file:
            the_file.write(response2.content)
            print(f'file written {filename_out}')
   return None

def append_ticket_to_file(number, filename):
   ticket_id = number

   url = f'https://{your_domain}.zendesk.com/api/v2/tickets/{ticket_id}.json'

   response = requests.get(url, auth=auth)

   page_data = response.json()
   print(page_data)
   print('')
   if page_data.get('error') == 'RecordNotFound':
      print('error this record does not exist', number)
      return None


   ticket = page_data['ticket']
   print(f"comments on ticket {ticket['id']}")
   sleep(7)
   comments = get_tickets_comment(ticket['id'])
   ticket['comments'] = comments
   # output_tickets['tickets'].append(ticket)
   print(comments)
   print('')

   with open(filename, mode='a+', newline='\n') as the_file:
      the_file.write(json.dumps(ticket))
      the_file.write('\n')
      # report_writer = csv.writer(csv_file, dialect='excel')


def get_tickets(number=None):
   if number == None: 
      # get all currently open ticket
      url = f'https://{your_domain}.zendesk.com/api/v2/tickets.json'
   else:
      # assume it is a number
      url = f'https://{your_domain}.zendesk.com/api/v2/tickets/{ticket_id}.json'

   response = requests.get(url, auth=auth)
   page_data = response.json()
   # print(page_data)
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
   for i in range(1, 259):
      # append_ticket_to_file(number=i, filename='tickets.json')

      get_comments_attachments(ticket_id=i)
      print('processed ticket ', i)
   

   # append_ticket_to_file(number=13, filename='tickets.json')
   # get_tickets()
   # get_tickets_comment(375)