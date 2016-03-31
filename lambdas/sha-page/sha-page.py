import boto3
import re

client = boto3.client('dynamodb')

base_html = """
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
  item_sha = event['sha']
  html = get_item_for_sha(item_sha)['Item']['html']['S']
  html_chunk = '<div class="wrapper groove">' + html + '</div>'
  page_html = base_html + html_chunk + '</body></html>'

  return page_html
