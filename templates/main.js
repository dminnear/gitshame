function openModal() {
  el = document.getElementById("modal");
  el.style.visibility = "visible";
}

function closeModalEvent(event) {
  if (event.target.id == "modal") {
    closeModal();
  }
}

function closeModal() {
  el = document.getElementById("modal");
  el.style.visibility = "hidden";
}

function shame() {
  link = document.getElementById("link").value;
  httpRequest = new XMLHttpRequest();
  httpRequest.onreadystatechange = function(){
    location.reload()
  };
  httpRequest.open('GET', 'https://5w7zwh5alf.execute-api.us-east-1.amazonaws.com/prod/pygmentize?link=' + link, true);
  httpRequest.send(null);
  closeModal();
}
