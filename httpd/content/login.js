const createLogin = () => {
    const div = document.createElement('div')
    div.className = 'login-box'
    const h3 = document.createElement('h3')
    h3.innerText = 'Enter device id: '
    const textInput = createTextInput('enter house id')
    const submitButton = createSubmitButton()
    const form = document.createElement('form')

    form.appendChild(h3)
    form.appendChild(textInput)
    form.appendChild(submitButton)
    form.onsubmit = createAuthCallback(textInput)
    div.appendChild(form)
    
    root.appendChild(div)
}
const createAuthCallback = textInput => {
    return async function(e) {
        e.preventDefault()
        const homeId = textInput.value

        const res = await getToken(homeId)
        if (res) {
            getHome()
                .then(data => {
                    e.target.parentNode.remove()
                    createIndex(data)
                })
                .catch(err => {
                    console.log('error: ', err, ' - reverting to sample data')
                    e.target.parentNode.remove()
                    createIndex(sampleData)
                })
        }
    }
}
