import boto3
import os
import time
import uuid

local = os.getenv('IS_LOCAL', "false")
client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1') if local == "true" else boto3.client('dynamodb')

def handler(event, context):
  post_id = str(uuid.uuid4())
  sha = event['sha']
  timestamp = str(time.time() * 1000)
  post = event['post']

  client.put_item(
    TableName='gitshame-posts',
    Item={
      'post_id': {
        'S': post_id
      },
      'sha': {
        'S': sha
      },
      'timestamp': {
        'S': timestamp
      },
      'post': {
        'S': post
      }
    })

  return (post_id, sha, timestamp, post)
