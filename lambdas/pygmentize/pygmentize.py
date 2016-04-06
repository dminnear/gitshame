from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, guess_lexer_for_filename
import boto3
import json
import re
import requests

client = boto3.client('dynamodb')

def validate_link(link):
  link_pattern = re.compile('^https:\/\/github\.com\/([a-zA-Z0-9.\-_]*)\/([a-zA-Z0-9.\-_]*)\/blob\/([a-zA-Z0-9.\-_]*)([a-zA-Z0-9.\/\-_]*)\/([a-zA-Z0-9.\-_]*)(#L\d+-L\d+|#L\d+)?$')
  link_match = link_pattern.match(link)
  if link_match:
    owner = link_match.group(1)
    repo = link_match.group(2)
    ref = link_match.group(3)
    path = link_match.group(4)
    filename = link_match.group(5)

    start_line = -1
    end_line = -1

    line_pattern = re.compile('^#L(\d+)-?L?(\d+)?$')
    lines = link_match.group(6) if link_match.group(6) else ''
    line_match = line_pattern.match(lines)

    if line_match:
      start_line = int(line_match.group(1))
      end_line = start_line if not line_match.group(2) else int(line_match.group(2))

    return (owner, repo, ref, path, filename, start_line, end_line)
  else:
    raise Exception("Link provided was not a valid github link. Link : %s" % link)

def handler(event, context):
  github_link = event['github_link']

  owner, repo, ref, path, filename, start_line, end_line = validate_link(github_link)
  response = requests.get("https://api.github.com/repos/%s/%s/contents%s/%s?ref=%s" % (owner, repo, path, filename, ref)).json()
  file = response['content'].decode(response['encoding'])
  chunk = '\n'.join(file.splitlines()[start_line-1:end_line]) if start_line > 0 else '\n'.join(file.splitlines()

  lexer = guess_lexer_for_filename(filename, chunk)
  formatter = HtmlFormatter(linenos=True,linenostart=start_line)
  html = highlight(chunk, lexer, formatter)

  sha = response['sha']

  client.put_item(
    TableName='gitshame-chunks',
    Item={
      'sha': {
        'S': sha
      },
      'html': {
        'S': html
      },
      'json': {
        'S': json.dumps(response)
      }
    })

  item_shas = client.get_item(
    TableName='gitshame-chunks',
    Key={
      'sha': {
        'S': 'index_page'
      }
    }
  )['Item']['item_shas']['M']

  client.put_item(
    TableName='gitshame-chunks',
    Item={
      'sha': {
        'S': 'index_page'
      },
      'item_shas': {
        'M': {
          '4': {
            'S': item_shas['3']['S']
          },
          '3': {
            'S': item_shas['2']['S']
          },
          '2': {
            'S': item_shas['1']['S']
          },
          '1': {
            'S': sha
          },
        }
      }
    }
  )

  return (sha, html, json)
