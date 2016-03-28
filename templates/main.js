function openModal() {
  el = document.getElementById("modal");
  el.style.visibility = "visible";
}

function closeModalEvent(event) {
  if (event.target.id == "modal") {
    closeModal()
  }
}

function closeModal() {
  el = document.getElementById("modal");
  el.style.visibility = "hidden";
}
