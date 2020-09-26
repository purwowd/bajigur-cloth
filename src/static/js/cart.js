const updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;
        console.log('productId:', productId, 'Action', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            location.href='/accounts/auth/'
            console.log('User is not authenticated')
        }else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data...')

    const url = '/orders/update-item/';

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(({'productId': productId, 'action': action}))
    }).then((response) => {
        return response.json();
    }).then((data) => {
        console.log('data:', data)
        location.reload()
    });
}
