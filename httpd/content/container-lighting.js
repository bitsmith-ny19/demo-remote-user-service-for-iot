const updateLabel = e => {
    e.preventDefault()
    const newRecord = {
        lighting: [{
            id: parseInt(e.target.getAttribute("data-id")),
            label: e.target.children[2].value
        }]
    }
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
            id: parseInt(e.target.parentNode.getAttribute("data-id")),
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
