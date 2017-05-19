import boto3
import jinja2
import os
import time

if os.getenv('USE_DYNAMO_LOCAL'):
  client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1')
else:
  client = boto3.client('dynamodb')

def get_blobs():
  timestamp = str(int(time.time() * 1000))

  items = client.query(
    TableName = 'Gitshame-Blobs',
    KeyConditionExpression = '#L = :index AND #T <= :sort',
    ExpressionAttributeValues = {
      ':index': { 'S': 'Index'},
      ':sort': { 'S': timestamp}
    },
    ScanIndexForward = False,
    Limit = 5,
    ExpressionAttributeNames = {
      '#L': 'Language',
      '#T': 'Timestamp-Sha'
    }
  )['Items']

  get_blob = lambda item: item['Blob']['S']
  get_url = lambda item: item['Url']['S']
  get_name = lambda item: item['Filename']['S']

  return [{'html': get_blob(item), 'url': get_url(item), 'name': get_name(item)} for item in items]

# from http://matthiaseisen.com/pp/patterns/p0198/
def render(tpl_path, args):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(args)

def handler(event, context):
  blobs = get_blobs()

  html = render('index.template', {
    'blobs': blobs
  })

  return html
