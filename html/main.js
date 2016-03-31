function submitComment() {
  text = escapeHtml(document.getElementById("comment-text").value);
  comments = document.getElementById("comments").innerHTML;
  comment = '<div class="comment">' + text + '</div>';
  document.getElementById("comments").innerHTML = comment + comments;
  document.getElementById("comment-text").value = "";
}

function escapeHtml(str) {
  var div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
};

function unescapeHtml(escapedStr) {
  var div = document.createElement('div');
  div.innerHTML = escapedStr;
  var child = div.childNodes[0];
  return child ? child.nodeValue : '';
};

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
