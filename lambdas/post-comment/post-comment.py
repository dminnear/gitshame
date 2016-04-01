import boto3
import time
import uuid

client = boto3.client('dynamodb')

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
      }
      'post': {
        'S': post
      }
    })
