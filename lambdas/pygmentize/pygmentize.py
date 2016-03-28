import re
import requests
from pygments import highlight
from pygments.lexers import guess_lexer, guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
import boto3

s3 = boto3.resource('s3')

def validate_link(link):
  pattern = re.compile("^https:\/\/github\.com\/([a-zA-Z0-9.\-_]*)\/([a-zA-Z0-9.\-_]*)\/blob\/([a-zA-Z0-9.\-_]*)([a-zA-Z0-9.\/\-_]*)\/([a-zA-Z0-9.\-_]*)#L(\d*)-L(\d*)$")
  match = pattern.match(link)
  if match:
    return (match.group(1), match.group(2), match.group(3), match.group(4), match.group(5), int(match.group(6)), int(match.group(7)))
  else:
    raise Exception("Link provided was not a valid github link. Link : %s" % link)

def handler(event, context):
  github_link = event['github_link']

  owner, repo, branch, path, filename, start_line, end_line = validate_link(github_link)
  request = requests.get("https://api.github.com/repos/%s/%s/contents%s/%s?ref=%s" % (owner, repo, path, filename, branch)).json()
  print "https://api.github.com/repos/%s/%s/contents%s/%s?ref=%s" % (owner, repo, path, filename, branch)
  file = request['content'].decode(request['encoding'])
  chunk = '\n'.join(file.splitlines()[start_line-1:end_line])

  lexer = guess_lexer_for_filename(filename, chunk)
  formatter = HtmlFormatter(linenos=True)
  html = highlight(chunk, lexer, formatter)

  s3.Object('gitshame', "chunks/%s.html" % request['sha']).put(Body=html)
