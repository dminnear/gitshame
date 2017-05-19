resource "aws_dynamodb_table" "gitshame-blobs" {
  name           = "Gitshame-Blobs"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "Language"
  range_key      = "Timestamp-Sha"

  attribute {
    name = "Language"
    type = "S"
  }

  attribute {
    name = "Timestamp-Sha"
    type = "S"
  }

  tags {
    Name = "Gitshame V2 Gitshame-Blobs"
  }
}
