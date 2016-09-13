from common.common import *
import requests

template = 'common/templates/index.template'
redirect = 'https://gitshame.xyz'

def handler(event, context):
  username, state, cookie = github_oauth(event, redirect)

  index_shas = filter(None, get_index_shas())
  dynamo_items = filter(None, [get_item_for_sha(sha) for sha in index_shas])
  html_blobs = filter(None, [html_blob(item) for item in dynamo_items])

  index_html = render(template, {
    'username': username,
    'state': state,
    'redirect': redirect,
    'html_blobs': html_blobs
  })

  return {'html': index_html, 'cookie': cookie}

def get_index_shas():
  try:
    item_map = get_item_for_sha('index_page')['item_shas']['M']
    indices = sorted(item_map)
    shas = [item_map[index]['S'] for index in indices]
  except Exception as e:
    print "[ERROR] Unable to retrieve shas for index page. Exception %s." % e
    return []

  return shas

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
