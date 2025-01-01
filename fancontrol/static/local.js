// JavaScript addEventListener for password, submit and enable form
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

	const disableButtons = document.querySelectorAll('.disable-button');
	disableButtons.forEach(button => {

		disableButtons.forEach(button => {
			const isDisabled = !button.checked;
			const form = button.form
			Array.from(form.elements).forEach((field) => {

				if (field.id != button.id && field.type != 'submit') {
					field.disabled = isDisabled;
				}
			});
		});

		button.addEventListener('change', event => {
			const isDisabled = !event.target.checked;
			const form = button.form
			Array.from(form.elements).forEach((field) => {

				if (field.id != event.target.id && field.type != 'submit') {
					field.disabled = isDisabled;
				}
			});
		}, false)
	})
	
	const togglePasswordbutton = document.querySelectorAll('.toggle-password');
	
	togglePasswordbutton.forEach(button => {
			button.addEventListener('click', (event) => {
				// toggle the input field between password and text
				const inputGroup = event.target.closest(".input-group");
				const formInputArray = inputGroup.querySelectorAll('input');				
				Array.from(formInputArray).forEach((passwordField) => {
					const isPassword = passwordField.type === 'password';
					passwordField.type = isPassword ? 'text' : 'password';
				});
				// toggle the icon
				const elementIArray = inputGroup.querySelectorAll('i');
				Array.from(elementIArray).forEach((iElement) => {
					iElement.classList.toggle('bi-eye');
					iElement.classList.toggle('bi-eye-slash');
				});
				
			});

			
	})
	
	// check if there are any floating-alert to close with a timeout
	const alertList = document.querySelectorAll('.floating-alert');
	const alertsAll = [...alertList].map(element => new bootstrap.Alert(element))
	
	Array.from(alertsAll).forEach((alertItem) => {
		var timeOut = alertItem._element.getAttribute('timeout');
		if (!timeOut) {
			timeOut=2000; // default timeout
		}
		const timeOuts = timeOut;

		window.setTimeout(function () {
		    alertItem.close();
		  }, timeOuts);
	});
	
})()
