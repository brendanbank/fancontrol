// Auto-dismiss the floating alert after 5 seconds
setTimeout(() => {
    const alertElement = document.querySelector('.floating-alert');
    if (alertElement) {
        alertElement.classList.remove('show');
        alertElement.classList.add('fade');
        setTimeout(() => alertElement.remove(), 150); // Remove the element after fading out
    }
}, 5000); // Adjust the timeout duration (5000 ms = 5 seconds)

// Example starter JavaScript for disabling form submissions if there are invalid fields
(() => {
  'use strict'

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  const forms = document.querySelectorAll('.needs-validation')

  // Loop over them and prevent submission
  Array.from(forms).forEach(form => {
    form.addEventListener('submit', event => {
      if (!form.checkValidity()) {
        event.preventDefault()
        event.stopPropagation()
      };

      form.classList.add('was-validated')
    }, false)
  })
})()


