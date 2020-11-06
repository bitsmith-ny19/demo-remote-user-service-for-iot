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
