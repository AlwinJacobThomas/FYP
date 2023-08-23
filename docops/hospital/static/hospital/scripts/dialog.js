var currentTab = 0
showTab(currentTab)

function showTab(n) {
  var x = document.getElementsByClassName('tab')
  x[n].style.display = 'block'
  if (n == 0) {
    document.getElementById('prevBtn').style.display = 'none'
  } else {
    document.getElementById('prevBtn').style.display = 'inline'
  }
  if (n == x.length - 1) {
    document.getElementById('nextBtn').innerHTML = 'Mark Response'
    document.getElementById('nextBtn').addEventListener('click', submitForm)
  } else {
    document.getElementById('nextBtn').innerHTML = 'Next'
    document.getElementById('nextBtn').removeEventListener('click', submitForm)
  }
  fixStepIndicator(n)
  enableDisableNextButton()
}

function nextPrev(n) {
  var x = document.getElementsByClassName('tab')
  x[currentTab].style.display = 'none'
  currentTab = currentTab + n
  showTab(currentTab)
}

function fixStepIndicator(n) {
  var i,
    x = document.getElementsByClassName('step')
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(' active', '')
  }
  x[n].className += ' active'
}

function enableDisableNextButton() {
  var x = document.getElementsByClassName('tab')
  var inputs = x[currentTab].querySelectorAll(
    "input[required]:not([type='hidden']), select[required], textarea[required]",
  )
  var nextBtn = document.getElementById('nextBtn')

  var allFieldsFilled = true

  for (var i = 0; i < inputs.length; i++) {
    if (inputs[i].value === '' || inputs[i].value === null) {
      allFieldsFilled = false
      break
    }
  }

  nextBtn.disabled = !allFieldsFilled
}

function submitForm() {
  var form = document.getElementById('regForm')
  form.submit()
}

// Image Preview
function readURL(input) {
  if (input.files && input.files[0]) {
    var reader = new FileReader()
    reader.onload = function (e) {
      var imagePreview = document.getElementById('imagePreview')
      imagePreview.style.backgroundImage = 'url(' + e.target.result + ')'
      imagePreview.style.display = 'none'
      fadeIn(imagePreview, 650)
    }
    reader.readAsDataURL(input.files[0])
  }
}

function fadeIn(element, duration) {
  var op = 0 // initial opacity
  var timer = setInterval(function () {
    if (op >= 1) {
      clearInterval(timer)
    }
    element.style.display = 'block'
    element.style.opacity = op
    element.style.filter = 'alpha(opacity=' + op * 100 + ')'
    op += op * 0.1 || 0.1
  }, duration / 10)
}

var imageUpload = document.getElementById('imageUpload')
if (imageUpload) {
  imageUpload.addEventListener('change', function () {
    readURL(this)
  })
}
// End Image Preview

// Add event listeners to track changes in form fields
var inputs = document.getElementsByTagName('input')
for (var i = 0; i < inputs.length; i++) {
  inputs[i].addEventListener('input', enableDisableNextButton)
}

var selects = document.getElementsByTagName('select')
for (var i = 0; i < selects.length; i++) {
  selects[i].addEventListener('change', enableDisableNextButton)
}

var textareas = document.getElementsByTagName('textarea')
for (var i = 0; i < textareas.length; i++) {
  textareas[i].addEventListener('input', enableDisableNextButton)
}
