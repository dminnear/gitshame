import boto3
import os
import re

local = os.getenv('IS_LOCAL', "false")
client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1') if local == "true" else boto3.client('dynamodb')

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
</body></html>
"""

comment_submit_html = """
<div class="comment-submit">
  <textarea id="comment-text"></textarea>
  <div class="buttons">
    <button type="button" onclick="submitComment()">
      Submit!
    </button>
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

  comments = ['<div class="comment">' + comment['post']['S'] + '</div>' for comment in dynamo_comments ]

  return '<div id="comments">' + "\n".join(comments) + '</div>'

def handler(event, context):
  item_sha = event['sha']
  html = get_item_for_sha(item_sha)['html']['S']
  html_chunk = '<div class="wrapper groove"><div class="scroll">' + html + '</div></div>'
  page_html = opening_html + html_chunk + comment_submit_html + comments_html(item_sha) + closing_html

  return page_html
