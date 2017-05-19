from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.lexers.special import TextLexer
from pygments.util import ClassNotFound
from urlparse import urlsplit
import boto3
import os
import requests
import time

if os.getenv('USE_DYNAMO_LOCAL'):
  client = boto3.client('dynamodb', endpoint_url='http://localhost:8001', region_name='us-east-1')
else:
  client = boto3.client('dynamodb')

class InvalidUrl(Exception):
  pass

class GithubApiError(Exception):
  pass

class DynamoWriteError(Exception):
  pass

def parse_github_link(url):
  split_url = urlsplit(url)

  try:
    scheme = split_url.scheme
    if scheme != 'https':
      raise InvalidUrl("URL %s has invalid scheme %s. Expected scheme https" % (url, scheme))

    netloc = split_url.netloc
    if netloc != 'github.com':
      raise InvalidUrl("URL %s has invalid domain %s. Expected domain github.com" % (url, netloc))

    path = str.split(split_url.path, '/')[1:]
    if (len(path) < 5) or (path[2] != 'blob'):
      raise InvalidUrl("URL %s has invalid path %s. Expected path of form /owner/repo/blob/ref/filepath/filename" % (url, split_url.path))

  except Exception as e:
    print "[ERROR] Invalid github link. Exception %s" % e
    raise e

  owner = path[0]
  repo = path[1]
  filepath = '/'.join(path[4:-1])
  filename = path[-1]
  ref = path[3]

  fragment = split_url.fragment
  start_line = None
  end_line = None
  if fragment:
    lines = str.split(fragment, '-')
    if len(lines) == 2:
      start_line = int(lines[0][1:])
      end_line = int(lines[1][1:])

  return owner, repo, filepath, filename, ref, start_line, end_line

def fetch_blob(owner, repo, filepath, filename, ref):
  try:
    response = requests.get("https://api.github.com/repos/%s/%s/contents%s/%s?ref=%s" % (owner, repo, filepath, filename, ref)).json()
    file = response['content'].decode(response['encoding'])
    lines = file.splitlines()
    sha = response['sha']
    html_url = response['html_url']

  except Exception as e:
    print "[ERROR] Could not fetch blob with owner %s, repo %s, filepath %s, filename %s, and ref %s" % (owner, repo, filepath, filename, ref)
    raise GithubApiError(e)

  return lines, sha, html_url

def format_blob(filename, blob, start_line):
  lexer = TextLexer()

  try:
    lexer = guess_lexer_for_filename(filename, blob)

  except ClassNotFound:
    try:
      lexer = guess_lexer(blob)

    except:
      pass

  formatter = HtmlFormatter(linenos=True,linenostart=start_line)
  formatted_blob = highlight(blob, lexer, formatter)

  return formatted_blob, lexer.name

def write_to_db(blob, lexer, sha, url, filename):
  timestamp = "%d-%s" % (int(time.time() * 1000), sha)

  try:
    client.put_item(
      TableName = 'Gitshame-Blobs',
      Item = {
        'Language': {
          'S': lexer
        },
        'Timestamp-Sha': {
          'S': timestamp
        },
        'Blob': {
          'S': blob
        },
        'Url': {
          'S': url
        },
        'Filename': {
          'S': filename
        }
      }
    )

    client.put_item(
      TableName = 'Gitshame-Blobs',
      Item = {
        'Language': {
          'S': 'Index'
        },
        'Timestamp-Sha': {
          'S': timestamp
        },
        'Blob': {
          'S': blob
        },
        'Url': {
          'S': url
        },
        'Filename': {
          'S': filename
        }
      }
    )

  except Exception as e:
    print "[ERROR] Could not write to DynamoDB. Exception %s" % e
    raise DynamoWriteError(e)


def handler(event, context):
  github_link = event['github_link']

  owner, repo, filepath, filename, ref, start_line, end_line = parse_github_link(github_link)

  lines, sha, html_url = fetch_blob(owner, repo, filepath, filename, ref)

  if not start_line:
    start_line = 1

  if end_line:
    lines = lines[start_line-1:end_line]

  blob = '\n'.join(lines)

  formatted_blob, lexer_name = format_blob(filename, blob, start_line)

  write_to_db(formatted_blob, lexer_name, sha, html_url, filename)

  return
