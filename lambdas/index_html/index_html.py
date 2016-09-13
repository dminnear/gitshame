import boto3
import jinja2
import json
import os
import random
import re
import requests
import string


local = os.getenv('IS_LOCAL', "false")
dynamo_client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1') if local == "true" else boto3.client('dynamodb')
s3_client = boto3.client('s3')


def handler(event, context):
  access_token, state = decode_cookie(event.get('cookie', ''))
  code = event.get('param_code', '')
  param_state = event.get('param_state', '')

  if code:
    if state != param_state:
      print "[ERROR] State mismatch! State from cookie: %s. State from query param: %s." % (state, param_state)
      state = ''
    else:
      access_token = get_access_token(code, state)

  if not access_token and not state:
    state = generate_state()

  index_shas = filter(None, get_index_shas())
  dynamo_items = filter(None, [get_item_for_sha(sha) for sha in index_shas])
  html_blobs = filter(None, [html_blob(item) for item in dynamo_items])

  username = get_username(access_token)

  index_html = render('index.template', {
    'username': username,
    'state': state,
    'html_blobs': html_blobs
  })

  cookie = encode_cookie(access_token, state)

  return {'html': index_html, 'cookie': cookie}


def decode_cookie(cookie):
  decoded = {}

  cookie_pattern = re.compile('^encoded=(.*)$')
  cookie_match = cookie_pattern.match(cookie)

  if cookie_match:
    encoded = cookie_match.group(1)
    decoded = json.loads(encoded)

  return (decoded.get('access_token', ''), decoded.get('state', ''))


def get_access_token(code, state):
  try:
    client_secret = s3_client.get_object(Bucket='gitshame-secrets', Key='github_client_secret')['Body'].read().strip()
  except Exception as e:
    print "[ERROR] Could not read github client secret from s3. Exception: %s." % e
    return ''

  data = {
    'client_id': '6de9e53b515a73893674',
    'client_secret': client_secret,
    'code': code,
    'state': state,
    'redirect': 'https://gitshame.xyz'
  }

  try:
    access_token = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept': 'application/json'}).json()['access_token']
  except Exception as e:
    print "[ERROR] Could not retrieve access token from github. Exception: %s." % e
    return ''

  return access_token


def generate_state(size=32, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))


def get_index_shas():
  try:
    item_map = get_item_for_sha('index_page')['item_shas']['M']
    indices = sorted(item_map)
    shas = [item_map[index]['S'] for index in indices]
  except Exception as e:
    print "[ERROR] Unable to retrieve shas for index page. Exception %s." % e
    return []

  return shas

def get_item_for_sha(sha):
  try:
    item = dynamo_client.get_item(
      TableName='gitshame-chunks',
      Key={
        'sha': {
          'S': sha
        }
      }
    )['Item']
  except Exception as e:
    print "[ERROR] Unable to retrieve item from database for sha %s. Exception: %s." % (sha, e)
    return {}

  return item


def html_blob(item):
  try:
    blob = {}
    content = json.loads(item['json']['S'])
    blob['filename'] = content['name']
    blob['sha'] = content['sha']
    blob['html'] = item['html']['S']
  except Exception as e:
    print "[ERROR] Unable to unmarshal json blob for item %s. Exception %s." % (item, e)
    return {}

  return blob


def get_username(access_token):
  if local == "true":
    return 'USER'

  try:
    username = requests.get('https://api.github.com/user?access_token=' + access_token).json()['login']
  except Exception as e:
    print "[ERROR] Unable to retrieve username from github for access token %s. Exception: %s." % (access_token, e)
    return ''

    return username


# from http://matthiaseisen.com/pp/patterns/p0198/
def render(tpl_path, args):
    path, filename = os.path.split(tpl_path)
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(path or './')
    ).get_template(filename).render(args)


def encode_cookie(access_token, state):
  encoded = json.dumps({'access_token': access_token, 'state': state})
  return 'encoded=' + encoded + '; Path=/; Domain=gitshame.xyz; Secure; HttpOnly'

