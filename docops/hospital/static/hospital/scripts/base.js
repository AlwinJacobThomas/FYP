document.addEventListener("DOMContentLoaded", function () {
    var currentUrl = window.location.href;
    var links = document.querySelectorAll(".menu a");

    links.forEach(function (link) {
        if (link.href === currentUrl) {
            link.classList.add("active");
        }
    });
});

function openDialog(formId, msg) {
    let form = document.getElementById(formId);
    let text = msg;
    if (confirm(msg) == true) {
      form.submit()
    }
  }
