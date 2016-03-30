import boto3
import re

client = boto3.client('dynamodb')
chunks_pattern = re.compile("^chunks/.+$")

base_html = """
<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset=UTF-8" />
<link href='http://s3.amazonaws.com/gitshame-html/main.css' rel='stylesheet' type='text/css'>
<script src='http://s3.amazonaws.com/gitshame-html/main.js'></script>

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

def get_item_for_sha(sha):
  return client.get_item(
    TableName='gitshame-chunks',
    Key={
      'sha': {
        'S': sha
      }
    }
  )

def handler(event, context):
  item_shas = get_item_for_sha('index_page')['Item']['item_shas']['M']
  html_chunks = [get_item_for_sha(item_shas[key]['S'])['Item']['html']['S'] for key in sorted(item_shas)]
  html_chunks = ['<div class="wrapper groove">' + html + '</div>' for html in html_chunks]
  index_html = base_html + '\n'.join(html_chunks) + '</body></html>'

  return index_html
