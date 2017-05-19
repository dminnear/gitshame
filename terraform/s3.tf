resource "aws_s3_bucket" "lambdas" {
  bucket = "gitshame-v2-lambdas"
  acl    = "private"

  tags {
    Name = "Gitshame V2 Lambdas"
  }
}

resource "aws_s3_bucket_object" "index-lambda" {
  bucket = "${aws_s3_bucket}.lambdas.bucket"
  key    = "index.zip"
  source = "../lambdas/index/index.zip"
  etag   = "${md5(file("../lambdas/index/index.zip"))}"
}

resource "aws_s3_bucket_object" "submit-lambda" {
  bucket = "${aws_s3_bucket}.lambdas.bucket"
  key    = "submit.zip"
  source = "../lambdas/submit/submit.zip"
  etag   = "${md5(file("../lambdas/submit/submit.zip"))}"
}
