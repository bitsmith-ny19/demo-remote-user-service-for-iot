const sampleData = {
    "_id": {
        "$oid": "5f9f31194d209a9655856f6b"
    },
    "thermostat": 27.0,
    "lighting": [
        {
            "id": 1,
            "label": "main-entrance-left",
            "is_on": false,
            "description": ""
        },
                    {
            "id": 2,
            "label": "backyard",
            "is_on": true,
            "description": ""
        }
    ]
}

async function getToken(houseId) {
    const data = {
        "house_id": houseId
    }

    const res = await fetch('http://localhost:8080/rucs/demo/set_token', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'Content-Type': 'application/json',
        }
    })

    return res.status === 200
}

async function getHome() {
    const res = await fetch('http://localhost:8080/rucs/', {
        method: 'GET',
        credentials: 'include'
    })

    return res
}

async function update(record){
    const res = await fetch('http://localhost:8080/rucs/', {
        method: 'PUT',
        body: JSON.stringify(record),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
}

const deleteLight = e => {
    const record = { id: e.currentTarget.parentNode.getAttribute('data-id') }

    fetch('http://localhost:8080/rucs/', {
        method: 'DELETE',
        body: JSON.stringify(record),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
}

const addLight = e => {
    const record = { label: e.target.children[0].value, is_on: false }
    
    fetch('http://localhost:8080/rucs/', {
        method: 'DELETE',
        body: JSON.stringify(record),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
}

const updateLabel = e => {
    e.preventDefault()
    const newRecord = {
        lighting: [{
            id: e.target.getAttribute("data-id"),
            label: e.target.children[2].value
        }]
    }
    debugger
    update(newRecord)
        .then(res => {
            e.target.children[0].value = e.target.children[2].value
        })
        .catch(err => {
            console.log(err)
        })
}

const toggleLight = e => {
    e.preventDefault()
    const newVal = (e.target.value === "turn on" ? false : true)
    const newRecord = {
        lighting: [{
            id: e.target.parentNode.getAttribute("data-id"),
            is_on: e.target.value === "turn on" ? false : true
        }]
    }

    update(newRecord)
        .then(res => {
            e.target.value = newVal ? "turn off" : "turn on"
        })
        .catch(err => {
            console.log(err)
        })
}

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

const createWidget = ({title, columns}) => {
    const div = document.createElement('div')
    div.className = 'widget'

    const h2 = document.createElement('h2')
    h2.innerText = title
    h2.className = 'widget-title'
    div.appendChild(h2)

    const outerCol = document.createElement('div')
    outerCol.className = 'outer-column'
    
    const headers = document.createElement('div')
    headers.className = 'row'

    cols = columns.map((colTitle, idx) => {
        let col = document.createElement('div')
        col.className = `col1-${idx+1}`
        let header = document.createElement('h3')
        header.innerText = colTitle
        col.appendChild(header)
        let subdiv = document.createElement('div')
        subdiv.className = colTitle.toLowerCase().split(" ").join("-")
        col.appendChild(subdiv)
        headers.append(col)

        return col
    })
    
    outerCol.appendChild(headers)
    div.appendChild(outerCol)

    return {
        body: div,
        columns: outerCol,
        title: h2
    }
}

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
    row.appendChild(form)
    widget.columns.appendChild(row)

    return widget.body
}

const createLightingWidget = data => {
    const {columns, title} = createWidget({
        title: 'Lights',
        columns: ['Label', 'New Label']
    })

    columns.className = "row"

    const widget = document.createElement('div')
    widget.className = 'widget'
    widget.appendChild(title)

    const outerCol = document.createElement('div')
    outerCol.className = 'outer-column'
    outerCol.appendChild(columns)

    const lights = data.map((light, idx) => {
        const div = document.createElement('div')
        div.className = 'inline-widget'
        let form = document.createElement('form')
        form.setAttribute('data-id', light.id)

        let label = document.createElement('p')
        label.className = 'light-label'
        label.innerText = light.label
        form.appendChild(label)
        
        let onOffButton = createSubmitButton(toggleLight)
        onOffButton.value = light.is_on ? 'turn on' : 'turn off'
        form.appendChild(onOffButton)

        let newLabelInput = createTextInput('enter new label...')
        form.appendChild(newLabelInput)

        let newLabelSubmit = createSubmitButton()
        newLabelSubmit.value = 'Update'
        form.onsubmit = updateLabel
        form.appendChild(newLabelSubmit)

        let removeLight = createSubmitButton(deleteLight)
        removeLight.value = 'Delete'
        form.appendChild(removeLight)

        div.appendChild(form)
        outerCol.appendChild(div)
        return div
    })

    const addLightRow = document.createElement('div')
    addLightRow.className = 'row'

    const addLightForm = document.createElement('form')
    addLightForm.className = 'add-light-form'
    const addLightTextInput = createTextInput('Add new light here...')
    addLightForm.appendChild(addLightTextInput)
    const addLightSubmit = createSubmitButton()
    addLightSubmit.value = "Create"
    addLightForm.appendChild(addLightSubmit)
    addLightForm.onsubmit = addLight
    outerCol.appendChild(addLightForm)

    widget.appendChild(outerCol)
    return widget
}

const createIndex = data => {
    const div = document.createElement('div')

    const {thermostat, lighting} = data
    const thermostatWidget = createThermostatWidget(thermostat)
    div.appendChild(thermostatWidget)

    let lightingWidget = createLightingWidget(lighting)
    div.appendChild(lightingWidget)

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

document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('root')
    createTitle('IoT Demo App')
    getHome()
        .then(res => createIndex(res))
        .catch(() => createLogin())
})