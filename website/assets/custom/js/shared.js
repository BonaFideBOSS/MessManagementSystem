// Clear previous requests
if (window.history.replaceState) {
  window.history.replaceState(null, null, window.location.href);
}

const csrf_token = document.querySelector('meta[name="csrf_token"]').getAttribute('content')
$.ajaxSetup({ headers: { 'X-CSRFToken': csrf_token } });

// Tooltips
function enable_tooltips() {
  const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
  const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
}
enable_tooltips()

// Notification Toast
function notify(message, delay = 10) {
  delay = delay * 1000
  toast_container = document.getElementById("notification-toast");
  const wrapper = document.createElement("div");
  wrapper.classList.add("toast", 'fade-in-right', 'bg-custom-gradient', "border-0", "shadow-lg");
  wrapper.setAttribute("data-bs-delay", delay);
  const website_name = document.querySelector('meta[property="og:title"]').getAttribute('content')
  const website_logo = document.querySelector('meta[property="og:image"]').getAttribute('content')
  wrapper.innerHTML =
    `<div class="toast-header border-0">
      <img src="${website_logo}" width="20" class="me-2">
      <strong class="me-auto">${website_name}</strong>
      <small>Just Now</small>
      <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
    </div>
    <div class="toast-body fs-6 text-dark">${message}</div>`;
  toast_container.append(wrapper);
  const toast = new bootstrap.Toast(wrapper);
  toast.show();
}

// Disable submit button on form submission
$('form').on('submit', function () {
  const loader = `<span class="spinner-grow spinner-grow-sm opacity-50"></span><span role="status">Loading...</span>`
  const btn = $(this).find('button[type="submit"]')
  if (this.checkValidity()) {
    $(btn).attr('disabled', true)
    $(btn).addClass('d-flex justify-content-center align-items-center gap-2')
    $(btn).html(loader)
  }
})

$('.resend-otp').on('click', function (e) {
  e.preventDefault()
  $.post($(this).data('url'))
  notify('Email sent!')
})