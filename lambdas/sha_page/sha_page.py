from common.common import *
import os
import re

template = 'common/templates/sha_page.template'

def handler(event, context):
  sha = event['sha']

  redirect = "https://gitshame.xyz/blob/%s" % sha
  username, state, cookie = github_oauth(event, redirect)

  try:
    blob = get_item_for_sha(sha)['html']['S']
  except Exception as e:
    print "[ERROR] Error retrieving html blob for sha %s. Exception %s." % (sha, e)
    blob = '<span>Invalid sha.</span>'

  comments = get_comments(sha)

  sha_page_html = render(template, {
    'username': username,
    'state': state,
    'redirect': redirect,
    'blob': blob,
    'comments': comments
  })

  return {"html": sha_page_html, 'cookie': cookie}

def get_comments(sha):
  try:
    items = dynamo_client.query(
      TableName='gitshame-posts',
      IndexName='sha-timestamp-index',
      Limit=20,
      ScanIndexForward=False,
      ProjectionExpression='post',
      KeyConditionExpression='sha = :sha',
      ExpressionAttributeValues={':sha':{'S':sha}})['Items']
    comments = [item['post']['S'] for item in items]
  except Exception as e:
    print "[ERROR] Unable to retrieve comments for sha %s. Exception %s." % (sha, e)
    return []

  return comments
