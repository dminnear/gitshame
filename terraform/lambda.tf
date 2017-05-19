resource "aws_iam_role" "lambda" {
  name = "Gitshame V2 Lambda IAM Role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [{
      "Sid": "",
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Sid": "GitshameBlobFullAccess",
      "Effect": "Allow",
      "Action": "dynamodb:*",
      "Resource": "${aws_dynamodb_table.gitshame-blobs.arn}/*"
    }
  ]
}
EOF
}

resource "aws_lambda_function" "index" {
  function_name    = "gitshame-v2-index"
  s3_bucket        = "${aws_s3_bucket}.lambdas.bucket"
  s3_key           = "index.zip"
  role             = "${aws_iam_role.lambda.arn}"
  handler          = "handler"
  source_code_hash = "${base64sha256(file("../lambdas/index/index.zip"))}"
  runtime          = "python2.7"
}

resource "aws_lambda_function" "submit" {
  function_name    = "gitshame-v2-submit"
  s3_bucket        = "${aws_s3_bucket}.lambdas.bucket"
  s3_key           = "submit.zip"
  role             = "${aws_iam_role.lambda.arn}"
  handler          = "handler"
  source_code_hash = "${base64sha256(file("../lambdas/submit/submit.zip"))}"
  runtime          = "python2.7"
}
