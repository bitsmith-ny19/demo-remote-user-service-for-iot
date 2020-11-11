async function getToken(houseId) {
    const data = {
        "house_id": houseId
    }

    const res = await fetch(
		`http://${domain}:${port}/rucs/demo/set_token`,
		{
	        method: 'POST',
	        body: JSON.stringify(data),
	        headers: {
	            'Content-Type': 'application/json',
        	}
		}
    )

    return res.status === 200
}

async function getHome() {
    const res = await fetch(`http://${domain}:${port}/rucs/`, {
        method: 'GET',
        credentials: 'include'
    })

    return res.json()
}

async function update(record){
    const res = await fetch(`http://${domain}:${port}/rucs/`, {
        method: 'PUT',
        body: JSON.stringify(record),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include'
    })
	.then( () => location.reload() );
}

const deleteLight = e => {
	e.preventDefault();
    const record = {
		id: parseInt(e.currentTarget.parentNode.getAttribute('data-id'))
	};
    fetch(`http://${domain}:${port}/rucs/`, {
        method: 'DELETE',
        body: JSON.stringify(record),
        headers: {
			'Content-Type': 'application/json',
        },
        credentials: 'include'
    }).then( () => location.reload() )
}

const addLight = e => {
	e.preventDefault();
    const record = { label: e.target.children[0].value, is_on: false }
    fetch( `http://${domain}:${port}/rucs/`, {
        method: 'POST',
        body: JSON.stringify(record),
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
    })
	.then( () => location.reload() );
};
