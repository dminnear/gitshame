import index
import unittest

expected_html = '<!DOCTYPEhtml><htmllang="en-us"><title>Gitshame</title><metacharset="UTF-8"/><linkhref="//s3.amazonaws.com/gitshame-html/main.css"rel="stylesheet"type="text/css"><linkhref="//s3.amazonaws.com/gitshame-html/icon.png"rel="icon"type="image/png"><scriptsrc="//s3.amazonaws.com/gitshame-html/main.js"></script><scriptsrc="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script><body><header><h1><ahref="/">Gitshame</a></h1><divclass="header-buttons"><aid="shame"onclick="openModal()">Shame!</a><aid="search">Seach</a></div></header><divid="modal"onclick="closeModalEvent(event)"><divclass="modal-inner"><h3>Enterashamefulgithublink</h3><inputid="link"type="text"name="link"><inputtype="button"value="Shame!"onclick="shame()"></div></div><section><divclass="blob"><aclass="file-header"href="https://github.com/dminnear/gitshame/blob/master/common/blob2.py">blob2.py</a><div>Blob2</div></div><divclass="blob"><aclass="file-header"href="https://github.com/dminnear/gitshame/blob/master/common/blob1.py">blob1.py</a><div>Blob1</div></div></section></body></html>'

class TestSubmit(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    index.client.create_table(
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

    index.client.put_item(
      TableName = 'Gitshame-Blobs',
      Item = {
        'Language': {
          'S': 'Index'
        },
        'Timestamp-Sha': {
          'S': '01'
        },
        'Blob': {
          'S': '<div>Blob 1</div>'
        },
        'Url': {
          'S': 'https://github.com/dminnear/gitshame/blob/master/common/blob1.py'
        },
        'Filename': {
          'S': 'blob1.py'
        }
      }
    )

    index.client.put_item(
      TableName = 'Gitshame-Blobs',
      Item = {
        'Language': {
          'S': 'Index'
        },
        'Timestamp-Sha': {
          'S': '02'
        },
        'Blob': {
          'S': '<div>Blob 2</div>'
        },
        'Url': {
          'S': 'https://github.com/dminnear/gitshame/blob/master/common/blob2.py'
        },
        'Filename': {
          'S': 'blob2.py'
        }
      }
    )

  @classmethod
  def tearDownClass(cls):
    index.client.delete_table(TableName = 'Gitshame-Blobs')

  def test_index(self):
    html = index.handler('','')
    self.assertEqual(expected_html, "".join(html.split()))

if __name__ == '__main__':
  unittest.main()
