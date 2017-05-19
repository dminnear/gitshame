import submit
import time
import unittest

expected_blob = '<table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre>16\n17\n18\n19\n20\n21\n22\n23</pre></div></td><td class="code"><div class="highlight"><pre><span></span>  <span class="n">link_pattern</span> <span class="o">=</span> <span class="n">re</span><span class="o">.</span><span class="n">compile</span><span class="p">(</span><span class="s1">&#39;^https:\\/\\/github\\.com\\/([a-zA-Z0-9.\\-_]*)\\/([a-zA-Z0-9.\\-_]*)\\/blob\\/([a-zA-Z0-9.\\-_]*)([a-zA-Z0-9.\\/\\-_]*)\\/([a-zA-Z0-9.\\-_]*)(#L\\d+-L\\d+|#L\\d+)?$&#39;</span><span class="p">)</span>\n  <span class="n">link_match</span> <span class="o">=</span> <span class="n">link_pattern</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="n">link</span><span class="p">)</span>\n  <span class="k">if</span> <span class="n">link_match</span><span class="p">:</span>\n    <span class="n">owner</span> <span class="o">=</span> <span class="n">link_match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">1</span><span class="p">)</span>\n    <span class="n">repo</span> <span class="o">=</span> <span class="n">link_match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">2</span><span class="p">)</span>\n    <span class="n">ref</span> <span class="o">=</span> <span class="n">link_match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">3</span><span class="p">)</span>\n    <span class="n">path</span> <span class="o">=</span> <span class="n">link_match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">4</span><span class="p">)</span>\n    <span class="n">filename</span> <span class="o">=</span> <span class="n">link_match</span><span class="o">.</span><span class="n">group</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span>\n</pre></div>\n</td></tr></table>'

class TestSubmit(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    submit.client.create_table(
      AttributeDefinitions = [
        {
          'AttributeName': 'Language',
          'AttributeType': 'S'
        },
        {
          'AttributeName': 'Timestamp-Sha',
          'AttributeType': 'S'
        }
      ],
      TableName = 'Gitshame-Blobs',
      KeySchema = [
        {
          'AttributeName': 'Language',
          'KeyType': 'HASH'
        },
        {
          'AttributeName': 'Timestamp-Sha',
          'KeyType': 'RANGE'
        }
      ],
      ProvisionedThroughput = {
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
      }
    )

  @classmethod
  def tearDownClass(cls):
    submit.client.delete_table(TableName = 'Gitshame-Blobs')

  def test_good_url(self):
    submit.handler({'github_link':'https://github.com/dminnear/gitshame/blob/4b11593c56e22ebb5db968ac78aa82fdb246fae1/lambdas/pygmentize/pygmentize.py#L16-L23'},'')
    items = submit.client.query(
      TableName = 'Gitshame-Blobs',
      KeyConditionExpression = '#L = :python',
      ExpressionAttributeNames = {
        '#L':'Language'
      },
      ExpressionAttributeValues = {
        ':python': { 'S': 'Python'}
      }
    )

    self.assertEqual(items['Count'], 1)
    item = items['Items'][0]

    self.assertEqual(item['Url']['S'], 'https://github.com/dminnear/gitshame/blob/4b11593c56e22ebb5db968ac78aa82fdb246fae1/lambdas/pygmentize/pygmentize.py')
    self.assertEqual(item['Language']['S'], 'Python')
    self.assertEqual(item['Blob']['S'], expected_blob)

    [actual_time, actual_sha] = item['Timestamp-Sha']['S'].split('-')
    expected_time = int(time.time() * 1000)
    self.assertTrue((expected_time - int(actual_time)) < 1000)
    self.assertEqual(actual_sha, '5224601bbfbe44541ae1ba923b5d52ea758c0134')

  def test_bad_urls(self):
    with self.assertRaises(submit.InvalidUrl):
      submit.handler({'github_link':'github.com/dminnear/gitshame/blob/4b11593c56e22ebb5db968ac78aa82fdb246fae1/lambdas/pygmentize/pygmentize.py#L16-L23'},'')
    with self.assertRaises(submit.InvalidUrl):
      submit.handler({'github_link':'https://github.org/dminnear/gitshame/blob/4b11593c56e22ebb5db968ac78aa82fdb246fae1/lambdas/pygmentize/pygmentize.py#L16-L23'},'')
    with self.assertRaises(submit.InvalidUrl):
      submit.handler({'github_link':'https://github.org/dminnear/gitshame/blob/4b11593c56e22ebb5db968ac78aa82fdb246fae1'},'')
    with self.assertRaises(submit.GithubApiError):
      submit.handler({'github_link':'https://github.com/dminnear/gitshame/blob/badref/lambdas/pygmentize/pygmentize.py#L16-L23'},'')

if __name__ == '__main__':
  unittest.main()
