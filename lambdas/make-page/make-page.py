import boto3
import re

s3 = boto3.resource('s3')
chunks_pattern = re.compile("^chunks/.+$")

base_html = """
<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset=UTF-8" />
<link rel="stylesheet" href="templates/main.css" type="text/css">
<script src="templates/main.js"></script>

"""

def handler(event, context):
  bucket = s3.Bucket('gitshame')
  chunks = [key.key for key in bucket.objects.all() if chunks_pattern.match(key.key)]
  html_chunks = [s3.Object('gitshame', key).get()['Body'].read() for key in chunks]
  html_chunks = ['<div class="wrapper groove">' + html + '</div>' for html in html_chunks]
  index_template = s3.Object('gitshame', 'templates/index.html').get()['Body'].read()
  index_html = base_html + '<body>\n' + index_template + '\n'.join(html_chunks) + '</body></html>'

  error_template = s3.Object('gitshame', 'templates/error.html').get()['Body'].read()
  error_html = base_html + '<body>\n' + error_template + '</body></html>'

  s3.Object('gitshame', 'index.html').put(Body=index_html, ContentType='text/html')
  s3.Object('gitshame', 'error.html').put(Body=error_html, ContentType='text/html')
