import boto3
import re

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

closing_html = """
<div class="comment-submit">
  <textarea id="comment-text"></textarea>
  <div class="buttons">
    <button type="button" onclick="submitComment()">
      Submit!
    </button>
  </div>
</div>

<div id="comments">
  <div class="comment">
    This is a comment.
  </div>
</div>

</body></html>
"""

def get_item_for_sha(sha):
  return client.get_item(
    TableName='gitshame-chunks',
    Key={
      'sha': {
        'S': sha
      }
    }
  )['Item']

def handler(event, context):
  item_sha = event['sha']
  html = get_item_for_sha(item_sha)['html']['S']
  html_chunk = '<div class="wrapper groove">' + html + '</div>'
  page_html = opening_html + html_chunk + closing_html

  return page_html
