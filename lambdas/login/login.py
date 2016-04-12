import boto3
import re
import requests

client = boto3.client('s3')

# def extract_cookie(cookie):
#   cookie_pattern = re.compile('^(access_token=[a-z0-9]*)(state=[a-z0-9]*)?.*$')
#   access_token = ''
#   state = ''
#   cookie_match = cookie_pattern.match(cookie)
#   if cookie_match:
#     access_token = cookie_match.group(1)[13:]
#     state = cookie_match.group(2)[6:]
#   return (access_token, state)

def handler(event, context):
  # access_token, state = extract_cookie(event['cookie'])

  # try:
  #   if not state == event['param_state']:
  #     raise Exception('Bad State!')
  # except KeyError:
  #   raise Exception('Bad State!')

  # code = event['param_code']

  # sr_response = client.get_object(
  #   Bucket='gitshame-secrets',
  #   Key='github_client_secret'
  # )
  # client_secret = sr_response['Body'].read().decode(sr_response['ContentEncoding'])

  # data = {
  #   'client_id': '6de9e53b515a73893674',
  #   'client_secret': client_secret,
  #   'code': code,
  #   'state': state,
  #   'redirect': 'https://gitshame.xyz'
  # }

  # requests.post('https://github.com/login/oauth/access_token', data=data)

  return 'Success'
