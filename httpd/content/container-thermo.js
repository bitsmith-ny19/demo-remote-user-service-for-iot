const createThermostatWidget = data => {
    const widget = createWidget({
        title: 'Thermostat',
        columns: ['Temperature', 'Set Temperature']
    })

    const row = document.createElement('div')
    row.className = 'row'

    const h1 = document.createElement('h1')
    h1.innerText = `${data}°`
    h1.className = 'temperature-reading'
    row.appendChild(h1)

    const form = document.createElement('form')
    form.className = 'inline-form'

    const textInput = createTextInput('temp')
    const submitButton = createSubmitButton()
    submitButton.value = 'Update'
    form.appendChild(textInput)
    form.appendChild(submitButton)
	form.onsubmit = (event) => {
		event.preventDefault();
		update( {
			thermostat: parseInt(
				event.target.querySelector('input[type="text"]').value
			)
		} );
	}
    row.appendChild(form)
    widget.columns.appendChild(row)
	

    return widget.body
}
