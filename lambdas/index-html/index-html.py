import boto3
import re
import json

client = boto3.client('dynamodb')

opening_html = """
<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset=UTF-8" />
<link href="//s3.amazonaws.com/gitshame-html/main.css" rel="stylesheet" type="text/css">
<link href="//s3.amazonaws.com/gitshame-html/icon.png" rel="icon" type="image/png">
<script src="//s3.amazonaws.com/gitshame-html/main.js"></script>

<body>
  <div class="nav">
    <h1 class="title"> Gitshame </h1>
    <button type="button" class="shame groove" onclick="openModal()"> Shame! </button>
  </div>
  <div id="modal" onclick="closeModalEvent(event)">
    <div class="groove">
      <h3> Enter a shameful github link </h3>
      <input id="link" type="text" name="link">
      <input type="button" value="Shame!" onclick="shame()">
    </div>
  </div>

"""

closing_html = '</body></html>'

def get_item_for_sha(sha):
  return client.get_item(
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

  return "<div class='wrapper groove'><div class='file-header'><a href='/blob/%s'>%s</a></div>" % (sha, filename) + html + '</div>'

def handler(event, context):
  item_shas = get_item_for_sha('index_page')['item_shas']['M']
  dynamo_items = [get_item_for_sha(item_shas[key]['S']) for key in sorted(item_shas)]
  html_blobs = [html_blob(item) for item in dynamo_items]
  index_html = opening_html + '\n'.join(html_blobs) + closing_html

  return index_html
