function submitComment() {
  var text = $('#comment-text').val();
  var comments = $('#comments').html();
  if ($.trim(text) == "") {
    return
  }
  var comment = '      <div class="comment">\n        <textarea readonly>\n' + text + '\n        </textarea>\n      </div>\n';
  $('#comments').html(comment + comments);
  $('#comment-text').val('');

  var href = window.location.href;
  var sha = href.substring(href.lastIndexOf('/') + 1);
  var httpRequest = new XMLHttpRequest();
  httpRequest.open('POST', 'https://gitshame.xyz/post');
  httpRequest.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
  httpRequest.send(JSON.stringify({
    sha: sha,
    post: text
  }));
}

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
  httpRequest.send(JSON.stringify({
    github_link: link
  }));
  closeModal();
}

function githubLogin(state, redirect) {
  var url = 'https://github.com/login/oauth/authorize'
  url += '?' + 'client_id=' + '6de9e53b515a73893674' + '&state=' + state + '&redirect=' + redirect

  window.location = url
}
