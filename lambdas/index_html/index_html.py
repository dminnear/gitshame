import boto3
import json
import os
import random
import re
import requests
import string

local = os.getenv('IS_LOCAL', "false")
dynamo_client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1') if local == "true" else boto3.client('dynamodb')
s3_client = boto3.client('s3')

def state_generator(size=32, chars=string.ascii_lowercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def get_item_for_sha(sha):
  return dynamo_client.get_item(
    TableName='gitshame-chunks',
    Key={
      'sha': {
        'S': sha
      }
    }
  )['Item']

def html_blob(item):
  html = item['html']['S']
  content = json.loads(item['json']['S'])
  filename = content['name']
  sha = content['sha']

  return "<div class='wrapper groove'><div class='file-header'><a href='/blob/%s'>%s</a></div><div class='scroll'>" % (sha, filename) + html + '</div></div>'

def extract_cookie(cookie):
  cookie_pattern = re.compile('^(access_token=[a-z0-9]*);.*(state=[a-z0-9]*);.*$')
  access_token = ''
  state = ''
  cookie_match = cookie_pattern.match(cookie)
  if cookie_match:
    access_token = cookie_match.group(1)[13:]
    state = cookie_match.group(2)[6:]
  return (access_token, state)

def get_access_token(code, state):
  s3_response = s3_client.get_object(
    Bucket='gitshame-secrets',
    Key='github_client_secret'
  )
  client_secret = s3_response['Body'].read().decode(s3_response['ContentEncoding'])

  data = {
    'client_id': '6de9e53b515a73893674',
    'client_secret': client_secret,
    'code': code,
    'state': state,
    'redirect': 'https://gitshame.xyz'
  }

  response = requests.post('https://github.com/login/oauth/access_token', data=data, headers={'Accept': 'application/json'}).json()

  return response['access_token']

def get_username(access_token):
  if local:
    return 'USER'
  response = requests.get('https://api.github.com/user?access_token=' + access_token).json()
  return response['login']

def create_index_html(access_token, state, html_blobs):
  html = """<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset=UTF-8" />
<link href="//s3.amazonaws.com/gitshame-html/main.css" rel="stylesheet" type="text/css">
<link href="//s3.amazonaws.com/gitshame-html/icon.png" rel="icon" type="image/png">
<script src="//s3.amazonaws.com/gitshame-html/main.js"></script>
<body>
  <div class="nav">
    <h1 class="title"> Gitshame </h1>
    <div class="buttons">
"""

  if access_token:
    html += '      <span>' + get_username(access_token) + '</span>'
  else:
    html += '      <button type="button" class="groove" onclick="githubLogin(\'' + state + '\')">Login</button>'

  html += """      <button type="button" class="groove" onclick="openModal()">
        Shame
      </button>
    </div>
  </div>
  <div id="modal" onclick="closeModalEvent(event)">
    <div class="groove">
      <h3> Enter a shameful github link </h3>
      <input id="link" type="text" name="link">
      <input type="button" value="Shame!" onclick="shame()">
    </div>
  </div>
"""
  html += '\n'.join(html_blobs)

  html += '</body></html>'

  return html

def handler(event, context):
  access_token, state = extract_cookie(event['cookie'])
  code = ''

  try:
    access_token = event['param_access_token']
    if not state == event['param_state']:
      raise Exception('Bad State!')
  except KeyError:
    pass

  try:
    code = event['param_code']
    if not state == event['param_state']:
      raise Exception('Bad State!')
    access_token = get_access_token(code, state)
  except KeyError:
    pass

  if access_token == '':
    state = state_generator()

  item_shas = get_item_for_sha('index_page')['item_shas']['M']
  dynamo_items = [get_item_for_sha(item_shas[key]['S']) for key in sorted(item_shas)]
  html_blobs = [html_blob(item) for item in dynamo_items]
  index_html = create_index_html(access_token, state, html_blobs)

  cookie = 'access_token=' + access_token + '; state=' + state + '; Domain=gitshame.xyz; Secure; HttpOnly;'

  return {'html': index_html, 'cookie': cookie}
