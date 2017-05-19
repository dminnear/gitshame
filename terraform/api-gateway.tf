resource "aws_api_gateway_rest_api" "gitshame" {
  name        = "Gitshame V2 API"
  description = "Gitshame V2 resources"
}

resource "aws_api_gateway_resource" "index" {
  rest_api_id = "${aws_api_gateway_rest_api.gitshame.id}"
  parent_id   = "${aws_api_gateway_rest_api.gitshame.root_resource_id}"
  path_part   = "/"
}

resource "aws_api_gateway_method" "index" {
  rest_api_id    = "${aws_api_gateway_rest_api.gitshame.id}"
  resource_id    = "${aws_api_gateway_resource.index.id}"
  http_method    = "GET"
  authorization  = "NONE"
}

resource "aws_api_gateway_resource" "submit" {
  rest_api_id = "${aws_api_gateway_rest_api.gitshame.id}"
  parent_id   = "${aws_api_gateway_rest_api.gitshame.root_resource_id}"
  path_part   = "/submit"
}

resource "aws_api_gateway_method" "submit" {
  rest_api_id   = "${aws_api_gateway_rest_api.gitshame.id}"
  resource_id   = "${aws_api_gateway_resource.submit.id}"
  http_method   = "POST"
  authorization = "NONE"
}
