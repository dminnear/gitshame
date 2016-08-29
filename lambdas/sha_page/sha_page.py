import boto3
import os
import re

local = os.getenv('IS_LOCAL', "false")
client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1') if local == "true" else boto3.client('dynamodb')

opening_html = """<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset="UTF-8" />
<link href="//s3.amazonaws.com/gitshame-html/main.css" rel="stylesheet" type="text/css">
<link href="//s3.amazonaws.com/gitshame-html/icon.png" rel="icon" type="image/png">
<script src="//s3.amazonaws.com/gitshame-html/main.js"></script>
<body>
  <header>
    <h1><a href="../">Gitshame</a></h1>
    <div class="header-buttons">
      <a id="shame" onclick="openModal()">Shame!</a>
    </div>
  <div id="modal" onclick="closeModalEvent(event)">
    <div class="modal-inner">
      <h3> Enter a shameful github link </h3>
      <input id="link" type="text" name="link">
      <input type="button" value="Shame!" onclick="shame()">
    </div>
  </div>
"""

closing_html = """
</body>
</html>
"""

comment_submit_html = """
  <section>
    <div id="comment">
      <textarea id="comment-text"></textarea>
      <a id="comment-submit">Submit</a>
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
  )['Item']

def comments_html(sha):
  dynamo_comments = client.query(
    TableName='gitshame-posts',
    IndexName='sha-timestamp-index',
    Limit=20,
    ScanIndexForward=False,
    ProjectionExpression='post',
    KeyConditionExpression='sha = :sha',
    ExpressionAttributeValues={':sha':{'S':sha}})['Items']

  comments = ['    <div class="comment">\n      <textarea readonly>\n' + comment['post']['S'] + '\n      </textarea>\n    </div>' for comment in dynamo_comments ]

  return "\n".join(comments) + '\n  </section>'

def handler(event, context):
  item_sha = event['sha']
  html = get_item_for_sha(item_sha)['html']['S']
  html_chunk = '  <section>\n    <div class="blob">\n' + html + '\n    </div>\n  </section>'
  page_html = opening_html + html_chunk + comment_submit_html + comments_html(item_sha) + closing_html

  return page_html
