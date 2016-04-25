import index_html
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
    <div class="buttons">
      <span>USER</span>      <button type="button" class="groove" onclick="openModal()">
        Shame
      </button>
    </div>
  </div>
  <div id="modal" onclick="closeModalEvent(event)">
    <div class="groove">
      <h3> Enter a shameful github link </h3>
      <input id="link" type="text" name="link">
      <input type="button" value="Shame!" onclick="shame()">
    </div>
  </div>
<div class='wrapper groove'><div class='file-header'><a href='/blob/4401a492327917623a31d480a9eae21a31a089ec'>404.jade</a></div><div class='scroll'><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2</pre></div></td><td class="code"><div class="highlight"><pre><span></span><span class="nt">h1</span> 404
<span class="nt">p</span> Page not found. Bummer.
</pre></div>
</td></tr></table></div></div>
<div class='wrapper groove'><div class='file-header'><a href='/blob/807f5437a9fe221a6b79d96619b41c67be14c4f4'>activate.sh</a></div><div class='scroll'><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre> 1
 2
 3
 4
 5
 6
 7
 8
 9
10
11
12
13
14
15
16
17
18
19
20
21
22
23</pre></div></td><td class="code"><div class="highlight"><pre><span></span><span class="ch">#!/usr/bin/env bash</span>

<span class="c1"># This is the activation script for the "code hosting" driver family.</span>
<span class="c1">#</span>
<span class="c1"># It is called when this family is activated.</span>
<span class="c1"># It automatically determines the right driver for the current environment</span>
<span class="c1"># and loads it.</span>


<span class="c1"># Loads the code-hosting driver that works with the given hostname</span>
<span class="k">function</span> activate_driver_for_code_hosting <span class="o">{</span>
  <span class="nb">local</span> <span class="nv">origin_hostname</span><span class="o">=</span><span class="s2">"</span><span class="k">$(</span>remote_domain<span class="k">)</span><span class="s2">"</span>
  <span class="k">if</span> <span class="o">[</span> <span class="s2">"</span><span class="nv">$origin_hostname</span><span class="s2">"</span> <span class="o">==</span> <span class="s1">'github.com'</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span>
    activate_driver <span class="s1">'code_hosting'</span> <span class="s1">'github'</span>
  <span class="k">elif</span> <span class="o">[</span> <span class="s2">"</span><span class="nv">$origin_hostname</span><span class="s2">"</span> <span class="o">==</span> <span class="s1">'bitbucket.org'</span> <span class="o">]</span><span class="p">;</span> <span class="k">then</span>
    activate_driver <span class="s1">'code_hosting'</span> <span class="s1">'bitbucket'</span>
  <span class="k">else</span>
    echo_error_header
    echo_usage <span class="s2">"Unsupported hosting service."</span>
    echo_usage <span class="s1">'This command requires hosting on GitHub or Bitbucket.'</span>
    exit_with_error newline
  <span class="k">fi</span>
<span class="o">}</span>
</pre></div>
</td></tr></table></div></div></body></html>
"""

class TestIndexHtml(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    index_html.dynamo_client.create_table(
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

    index_html.dynamo_client.put_item(
      TableName='gitshame-chunks',
      Item={
        'sha': {
          'S': 'index_page'
        },
        'item_shas': {
          'M': {
            '1': {
              'S': '4401a492327917623a31d480a9eae21a31a089ec'
            },
            '2': {
              'S': '807f5437a9fe221a6b79d96619b41c67be14c4f4'
            }
          }
        }
      }
    )

    index_html.dynamo_client.put_item(
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

    index_html.dynamo_client.put_item(
      TableName='gitshame-chunks',
      Item={
        'sha': {
          'S': '807f5437a9fe221a6b79d96619b41c67be14c4f4'
        },
        'html': {
          'S': """<table class=\"highlighttable\"><tr><td class=\"linenos\"><div class=\"linenodiv\"><pre> 1\n 2\n 3\n 4\n 5\n 6\n 7\n 8\n 9\n10\n11\n12\n13\n14\n15\n16\n17\n18\n19\n20\n21\n22\n23</pre></div></td><td class=\"code\"><div class=\"highlight\"><pre><span></span><span class=\"ch\">#!/usr/bin/env bash</span>\n\n<span class=\"c1\"># This is the activation script for the \"code hosting\" driver family.</span>\n<span class=\"c1\">#</span>\n<span class=\"c1\"># It is called when this family is activated.</span>\n<span class=\"c1\"># It automatically determines the right driver for the current environment</span>\n<span class=\"c1\"># and loads it.</span>\n\n\n<span class=\"c1\"># Loads the code-hosting driver that works with the given hostname</span>\n<span class=\"k\">function</span> activate_driver_for_code_hosting <span class=\"o\">{</span>\n  <span class=\"nb\">local</span> <span class=\"nv\">origin_hostname</span><span class=\"o\">=</span><span class=\"s2\">\"</span><span class=\"k\">$(</span>remote_domain<span class=\"k\">)</span><span class=\"s2\">\"</span>\n  <span class=\"k\">if</span> <span class=\"o\">[</span> <span class=\"s2\">\"</span><span class=\"nv\">$origin_hostname</span><span class=\"s2\">\"</span> <span class=\"o\">==</span> <span class=\"s1\">'github.com'</span> <span class=\"o\">]</span><span class=\"p\">;</span> <span class=\"k\">then</span>\n    activate_driver <span class=\"s1\">'code_hosting'</span> <span class=\"s1\">'github'</span>\n  <span class=\"k\">elif</span> <span class=\"o\">[</span> <span class=\"s2\">\"</span><span class=\"nv\">$origin_hostname</span><span class=\"s2\">\"</span> <span class=\"o\">==</span> <span class=\"s1\">'bitbucket.org'</span> <span class=\"o\">]</span><span class=\"p\">;</span> <span class=\"k\">then</span>\n    activate_driver <span class=\"s1\">'code_hosting'</span> <span class=\"s1\">'bitbucket'</span>\n  <span class=\"k\">else</span>\n    echo_error_header\n    echo_usage <span class=\"s2\">\"Unsupported hosting service.\"</span>\n    echo_usage <span class=\"s1\">'This command requires hosting on GitHub or Bitbucket.'</span>\n    exit_with_error newline\n  <span class=\"k\">fi</span>\n<span class=\"o\">}</span>\n</pre></div>\n</td></tr></table>"""
        },
        'json': {
          'S': """{\"name\": \"activate.sh\", \"encoding\": \"base64\", \"url\": \"https://api.github.com/repos/Originate/git-town/contents/src/drivers/code_hosting/activate.sh?ref=master\", \"html_url\": \"https://github.com/Originate/git-town/blob/master/src/drivers/code_hosting/activate.sh\", \"download_url\": \"https://raw.githubusercontent.com/Originate/git-town/master/src/drivers/code_hosting/activate.sh\", \"content\": \"IyEvdXNyL2Jpbi9lbnYgYmFzaAoKIyBUaGlzIGlzIHRoZSBhY3RpdmF0aW9u\\nIHNjcmlwdCBmb3IgdGhlICJjb2RlIGhvc3RpbmciIGRyaXZlciBmYW1pbHku\\nCiMKIyBJdCBpcyBjYWxsZWQgd2hlbiB0aGlzIGZhbWlseSBpcyBhY3RpdmF0\\nZWQuCiMgSXQgYXV0b21hdGljYWxseSBkZXRlcm1pbmVzIHRoZSByaWdodCBk\\ncml2ZXIgZm9yIHRoZSBjdXJyZW50IGVudmlyb25tZW50CiMgYW5kIGxvYWRz\\nIGl0LgoKCiMgTG9hZHMgdGhlIGNvZGUtaG9zdGluZyBkcml2ZXIgdGhhdCB3\\nb3JrcyB3aXRoIHRoZSBnaXZlbiBob3N0bmFtZQpmdW5jdGlvbiBhY3RpdmF0\\nZV9kcml2ZXJfZm9yX2NvZGVfaG9zdGluZyB7CiAgbG9jYWwgb3JpZ2luX2hv\\nc3RuYW1lPSIkKHJlbW90ZV9kb21haW4pIgogIGlmIFsgIiRvcmlnaW5faG9z\\ndG5hbWUiID09ICdnaXRodWIuY29tJyBdOyB0aGVuCiAgICBhY3RpdmF0ZV9k\\ncml2ZXIgJ2NvZGVfaG9zdGluZycgJ2dpdGh1YicKICBlbGlmIFsgIiRvcmln\\naW5faG9zdG5hbWUiID09ICdiaXRidWNrZXQub3JnJyBdOyB0aGVuCiAgICBh\\nY3RpdmF0ZV9kcml2ZXIgJ2NvZGVfaG9zdGluZycgJ2JpdGJ1Y2tldCcKICBl\\nbHNlCiAgICBlY2hvX2Vycm9yX2hlYWRlcgogICAgZWNob191c2FnZSAiVW5z\\ndXBwb3J0ZWQgaG9zdGluZyBzZXJ2aWNlLiIKICAgIGVjaG9fdXNhZ2UgJ1Ro\\naXMgY29tbWFuZCByZXF1aXJlcyBob3N0aW5nIG9uIEdpdEh1YiBvciBCaXRi\\ndWNrZXQuJwogICAgZXhpdF93aXRoX2Vycm9yIG5ld2xpbmUKICBmaQp9Cg==\\n\", \"sha\": \"807f5437a9fe221a6b79d96619b41c67be14c4f4\", \"_links\": {\"self\": \"https://api.github.com/repos/Originate/git-town/contents/src/drivers/code_hosting/activate.sh?ref=master\", \"git\": \"https://api.github.com/repos/Originate/git-town/git/blobs/807f5437a9fe221a6b79d96619b41c67be14c4f4\", \"html\": \"https://github.com/Originate/git-town/blob/master/src/drivers/code_hosting/activate.sh\"}, \"git_url\": \"https://api.github.com/repos/Originate/git-town/git/blobs/807f5437a9fe221a6b79d96619b41c67be14c4f4\", \"path\": \"src/drivers/code_hosting/activate.sh\", \"type\": \"file\", \"size\": 763}"""
        }
      }
    )

  @classmethod
  def tearDownClass(cls):
    index_html.dynamo_client.delete_table(TableName='gitshame-chunks')

  def test_index_html(self):
    self.assertEqual(index_html.handler({'cookie': 'encoded=eyJhY2Nlc3NfdG9rZW4iOiAiYWJjZGVmZyIsICJzdGF0ZSI6ICIifQ==\n'},'')['html'].strip(), expected.strip())

if __name__ == '__main__':
  unittest.main()
