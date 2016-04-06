import sha_page
import unittest

expected = """
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

<div class="wrapper groove"><div class="scroll"><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2</pre></div></td><td class="code"><div class="highlight"><pre><span></span><span class="nt">h1</span> 404
<span class="nt">p</span> Page not found. Bummer.
</pre></div>
</td></tr></table></div></div>
<div class="comment-submit">
  <textarea id="comment-text"></textarea>
  <div class="buttons">
    <button type="button" onclick="submitComment()">
      Submit!
    </button>
  </div>
</div>
<div id="comments"><div class="comment">test post</div></div>
</body></html>
"""

class TestShaPage(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    sha_page.client.create_table(
      AttributeDefinitions=[
        {
          'AttributeName': 'sha',
          'AttributeType': 'S'
        }
      ],
      TableName='gitshame-chunks',
      KeySchema=[
        {
          'AttributeName': 'sha',
          'KeyType': 'HASH'
        }
      ],
      ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
      }
    )

    sha_page.client.create_table(
      AttributeDefinitions=[
        {
          'AttributeName': 'post_id',
          'AttributeType': 'S'
        },
        {
          'AttributeName': 'sha',
          'AttributeType': 'S'
        },
        {
          'AttributeName': 'timestamp',
          'AttributeType': 'S'
        }
      ],
      TableName='gitshame-posts',
      KeySchema=[
        {
          'AttributeName': 'post_id',
          'KeyType': 'HASH'
        }
      ],
      GlobalSecondaryIndexes=[
        {
          'IndexName': 'sha-timestamp-index',
          'KeySchema': [
            {
              'AttributeName': 'sha',
              'KeyType': 'HASH'
            },
            {
              'AttributeName': 'timestamp',
              'KeyType': 'RANGE'
            }
          ],
          'Projection': {
            'ProjectionType': 'ALL'
          },
          'ProvisionedThroughput': {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
          }
        }
      ],
      ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
      }
    )

    sha_page.client.put_item(
      TableName='gitshame-posts',
      Item={
        'post_id': {
          'S': '12345'
        },
        'sha': {
          'S': '4401a492327917623a31d480a9eae21a31a089ec'
        },
        'timestamp': {
          'S': '1'
        },
        'post': {
          'S': 'test post'
        }
      }
    )

    sha_page.client.put_item(
      TableName='gitshame-chunks',
      Item={
        'sha': {
          'S': '4401a492327917623a31d480a9eae21a31a089ec'
        },
        'html': {
          'S': """<table class=\"highlighttable\"><tr><td class=\"linenos\"><div class=\"linenodiv\"><pre>1\n2</pre></div></td><td class=\"code\"><div class=\"highlight\"><pre><span></span><span class=\"nt\">h1</span> 404\n<span class=\"nt\">p</span> Page not found. Bummer.\n</pre></div>\n</td></tr></table>"""
        },
        'json': {
          'S': """{\"name\": \"404.jade\", \"encoding\": \"base64\", \"url\": \"https://api.github.com/repos/Originate/git-town/contents/website/404.jade?ref=master\", \"html_url\": \"https://github.com/Originate/git-town/blob/master/website/404.jade\", \"download_url\": \"https://raw.githubusercontent.com/Originate/git-town/master/website/404.jade\", \"content\": \"aDEgNDA0CnAgUGFnZSBub3QgZm91bmQuIEJ1bW1lci4K\\n\", \"sha\": \"4401a492327917623a31d480a9eae21a31a089ec\", \"_links\": {\"self\": \"https://api.github.com/repos/Originate/git-town/contents/website/404.jade?ref=master\", \"git\": \"https://api.github.com/repos/Originate/git-town/git/blobs/4401a492327917623a31d480a9eae21a31a089ec\", \"html\": \"https://github.com/Originate/git-town/blob/master/website/404.jade\"}, \"git_url\": \"https://api.github.com/repos/Originate/git-town/git/blobs/4401a492327917623a31d480a9eae21a31a089ec\", \"path\": \"website/404.jade\", \"type\": \"file\", \"size\": 33}"""
        }
      }
    )

  @classmethod
  def tearDownClass(cls):
    sha_page.client.delete_table(TableName='gitshame-chunks')
    sha_page.client.delete_table(TableName='gitshame-posts')

  def test_sha_page(self):
    self.assertEqual(sha_page.handler({'sha':'4401a492327917623a31d480a9eae21a31a089ec'},'').strip(), expected.strip())

if __name__ == '__main__':
  unittest.main()