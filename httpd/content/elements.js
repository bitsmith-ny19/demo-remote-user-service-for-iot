const createTitle = str => {
    const el = document.createElement('h1')
    el.innerText = str
    root.appendChild(el)
    return el
}

const createTextInput = placeholder => {
    const textInput = document.createElement('input')
    textInput.setAttribute('type', 'text')
    textInput.placeholder = placeholder
    return textInput
}

const createSubmitButton = callback => {
    const submitButton = document.createElement('input')
    submitButton.setAttribute('type', 'submit')
    submitButton.className = 'submit-button'
    submitButton.onclick = callback

    return submitButton
}
