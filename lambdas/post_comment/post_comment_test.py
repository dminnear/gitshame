import post_comment
import unittest

class TestIndexHtml(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    post_comment.client.create_table(
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

  @classmethod
  def tearDownClass(cls):
    post_comment.client.delete_table(TableName='gitshame-posts')

  def test_post_comment(self):
    event = {'sha': '123456789', 'post': 'test post'}
    post_id, sha, timestamp, post = post_comment.handler(event,'')
    item = post_comment.client.get_item(
      TableName='gitshame-posts',
      Key={
        'post_id': {
          'S': post_id
        }
      }
    )['Item']
    self.assertEqual('123456789', item['sha']['S'])
    self.assertEqual(timestamp, item['timestamp']['S'])
    self.assertEqual('test post', item['post']['S'])

if __name__ == '__main__':
  unittest.main()
