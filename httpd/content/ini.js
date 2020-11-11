const domain = "localhost"
const port = "8080"
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
document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('root')
    createTitle('IoT Demo App')
    getHome()
        .then(res => createIndex(res))
        .catch(() => createLogin())
})
