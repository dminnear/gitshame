function submitComment() {
  var text = escapeHtml(document.getElementById("comment-text").value);
  var comments = document.getElementById("comments").innerHTML;
  var comment = '<div class="comment">' + text + '</div>';
  document.getElementById("comments").innerHTML = comment + comments;
  document.getElementById("comment-text").value = "";

  var href = window.location.href;
  var sha = href.substring(href.lastIndexOf("/") + 1);
  var httpRequest = new XMLHttpRequest();
  httpRequest.open('POST', 'https://gitshame.xyz/post');
  httpRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  httpRequest.send(JSON.stringify({sha: sha, post: text}));
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
  var el = document.getElementById("modal");
  el.style.visibility = "visible";
}

function closeModal() {
  var el = document.getElementById("modal");
  el.style.visibility = "hidden";
}

function closeModalEvent(event) {
  if (event.target.id == "modal") {
    closeModal();
  }
}

function shame() {
  var link = document.getElementById("link").value;
  var httpRequest = new XMLHttpRequest();
  httpRequest.open('POST', 'https://gitshame.xyz/pygmentize');
  httpRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  httpRequest.send(JSON.stringify({github_link: link}));
  closeModal();
}

function githubLogin(state) {
  var url = 'https://github.com/login/oauth/authorize'
  url += '?' + 'client_id=' + '6de9e53b515a73893674' + '&state=' + state + '&redirect=' + 'https://gitshame.xyz/login'

  window.location = url
}
