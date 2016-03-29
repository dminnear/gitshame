import boto3
import re

client = boto3.client('dynamodb')
chunks_pattern = re.compile("^chunks/.+$")

base_html = """
<!DOCTYPE html>
<html lang="en-us">
<title>Gitshame</title>
<meta charset=UTF-8" />
<style>
html,
body {
  margin: 0;
  padding: 0;
  height: 100%;
}

.groove {
  border: 1px #000;
  border-style: solid;
  border-radius: 10px;
  background-color: rgb(255, 255, 255);
}

#modal {
  visibility: hidden;
  position: fixed;
  left: 0px;
  top: 0px;
  width: 100%;
  height: 100%;
  text-align: center;
  z-index: 1000;
  background-color: rgba(0, 0, 0, .5);
}

#modal div {
  width: 60%;
  margin: 100px auto;
  background-color: #fff;
  padding: 10px;
}

#modal div h3 {
  margin: 10px;
}

div.nav {
  text-align: center;
  position: relative;
  margin: 10px;
}

h1.title {
  display: inline;
}

button.shame {
  position: absolute;
  right: 0;
  padding: 10px;
}

div.wrapper {
  width: 80%;
  margin: 20px 10% 20px 10%;
}

td.linenos {
  background-color: #f0f0f0;
  padding-right: 10px;
}

span.lineno {
  background-color: #f0f0f0;
  padding: 0 5px 0 5px;
}

pre {
  line-height: 125%;
}

body .hll {
  background-color: #ffffcc
}

body {
  background: #f8f8f8;
}

body .c {
  color: #408080;
  font-style: italic
}

body .err {
  border: 1px solid #FF0000
}

body .k {
  color: #008000;
  font-weight: bold
}

body .o {
  color: #666666
}

body .ch {
  color: #408080;
  font-style: italic
}

body .cm {
  color: #408080;
  font-style: italic
}

body .cp {
  color: #BC7A00
}

body .cpf {
  color: #408080;
  font-style: italic
}

body .c1 {
  color: #408080;
  font-style: italic
}

body .cs {
  color: #408080;
  font-style: italic
}

body .gd {
  color: #A00000
}

body .ge {
  font-style: italic
}

body .gr {
  color: #FF0000
}

body .gh {
  color: #000080;
  font-weight: bold
}

body .gi {
  color: #00A000
}

body .go {
  color: #888888
}

body .gp {
  color: #000080;
  font-weight: bold
}

body .gs {
  font-weight: bold
}

body .gu {
  color: #800080;
  font-weight: bold
}

body .gt {
  color: #0044DD
}

body .kc {
  color: #008000;
  font-weight: bold
}

body .kd {
  color: #008000;
  font-weight: bold
}

body .kn {
  color: #008000;
  font-weight: bold
}

body .kp {
  color: #008000
}

body .kr {
  color: #008000;
  font-weight: bold
}

body .kt {
  color: #B00040
}

body .m {
  color: #666666
}

body .s {
  color: #BA2121
}

body .na {
  color: #7D9029
}

body .nb {
  color: #008000
}

body .nc {
  color: #0000FF;
  font-weight: bold
}

body .no {
  color: #880000
}

body .nd {
  color: #AA22FF
}

body .ni {
  color: #999999;
  font-weight: bold
}

body .ne {
  color: #D2413A;
  font-weight: bold
}

body .nf {
  color: #0000FF
}

body .nl {
  color: #A0A000
}

body .nn {
  color: #0000FF;
  font-weight: bold
}

body .nt {
  color: #008000;
  font-weight: bold
}

body .nv {
  color: #19177C
}

body .ow {
  color: #AA22FF;
  font-weight: bold
}

body .w {
  color: #bbbbbb
}

body .mb {
  color: #666666
}

body .mf {
  color: #666666
}

body .mh {
  color: #666666
}

body .mi {
  color: #666666
}

body .mo {
  color: #666666
}

body .sb {
  color: #BA2121
}

body .sc {
  color: #BA2121
}

body .sd {
  color: #BA2121;
  font-style: italic
}

body .s2 {
  color: #BA2121
}

body .se {
  color: #BB6622;
  font-weight: bold
}

body .sh {
  color: #BA2121
}

body .si {
  color: #BB6688;
  font-weight: bold
}

body .sx {
  color: #008000
}

body .sr {
  color: #BB6688
}

body .s1 {
  color: #BA2121
}

body .ss {
  color: #19177C
}

body .bp {
  color: #008000
}

body .vc {
  color: #19177C
}

body .vg {
  color: #19177C
}

body .vi {
  color: #19177C
}

body .il {
  color: #666666
}
</style>
<script>
function openModal() {
  el = document.getElementById("modal");
  el.style.visibility = "visible";
}

function closeModal() {
  el = document.getElementById("modal");
  el.style.visibility = "hidden";
}

function closeModalEvent(event) {
  if (event.target.id == "modal") {
    closeModal();
  }
}

function shame() {
  link = document.getElementById("link").value;
  httpRequest = new XMLHttpRequest();
  httpRequest.open('POST', 'https://5w7zwh5alf.execute-api.us-east-1.amazonaws.com/prod/pygmentize');
  httpRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  httpRequest.send(JSON.stringify({github_link: link}));
  closeModal();
}
</script>

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

"""

def get_item_for_sha(sha):
  return client.get_item(
    TableName='gitshame-chunks',
    Key={
      'sha': {
        'S': sha
      }
    }
  )

def handler(event, context):
  item_shas = get_item_for_sha('index_page')['Item']['item_shas']['M']
  html_chunks = [get_item_for_sha(item_shas[key]['S'])['Item']['html']['S'] for key in sorted(item_shas)]
  html_chunks = ['<div class="wrapper groove">' + html + '</div>' for html in html_chunks]
  index_html = base_html + '\n'.join(html_chunks) + '</body></html>'

  return index_html
