const createIndex = data => {
    const div = document.createElement('div')

    const {thermostat, lighting} = data
    const thermostatWidget = createThermostatWidget(thermostat)
    div.appendChild(thermostatWidget)

    let lightingWidget = createLightingWidget(lighting)
    div.appendChild(lightingWidget)

    root.appendChild(div)
}
