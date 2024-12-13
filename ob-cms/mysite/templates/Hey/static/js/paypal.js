// script.js

// Initialize the PayPal JavaScript SDK with your client ID
paypal.Buttons({
    createOrder: function(data, actions) {
        return actions.order.create({
            purchase_units: [{
                amount: {
                    value: '5' // Default donation amount ($5)
                }
            }]
        });
    },
    onApprove: function(data, actions) {
        // Capture the payment and redirect to chat.html
        return actions.order.capture().then(function(details) {
            // Redirect to chat.html after successful donation
            window.location.href = 'chat.html';
        });
    }
}).render('#paypal-button-container');

// Function to handle donations with different amounts
function donate(amount) {
    // Update the PayPal donation amount
    paypal.Buttons().update({
        createOrder: function(data, actions) {
            return actions.order.create({
                purchase_units: [{
                    amount: {
                        value: amount.toString()
                    }
                }]
            });
        }
    });
    
    // Trigger the PayPal button click
    document.getElementById('paypal-button-container').click();
}

// Function to load content into the "content" div
function loadPage(pageName) {
    const contentDiv = document.getElementById('content');
    
    // Use fetch or XMLHttpRequest to load content from the server
    fetch(`/${pageName}.html`)
        .then(response => response.text())
        .then(data => {
            contentDiv.innerHTML = data;
        })
        .catch(error => {
            console.error(`Error loading ${pageName}.html: ${error}`);
        });
}