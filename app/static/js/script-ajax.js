const button = document.querySelector('#buy_now_btn');

checkout_public_key = "pk_test_51JxWFsEMDYePyYSgY8abIK9kH8sQpy6XAOPsmuNDXzlqoH4QajY4ImmCi6VwzqULBqOdofL3DlgFYLk7915RTWR700ll6TxnDh"
checkout_session_id = "cs_test_a1QgYnhbINnbXouvWuOKGegUrs6kNxnRHTSQ3FPShDg6vq6B7JHCN4Cktg"
button.addEventListener('click', event => {
    fetch('/stripe_pay')
    .then((result) => { return result.json(); })
    .then((data) => {
        var stripe = Stripe(data.checkout_public_key);
        stripe.redirectToCheckout({
            // Make the id field from the Checkout Session creation API response
            // available to this file, so you can provide it as parameter here
            // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
            sessionId: data.checkout_session_id
        }).then(function (result) {
            // If `redirectToCheckout` fails due to a browser or network
            // error, display the localized error message to your customer
            // using `result.error.message`.
        });
    })
});