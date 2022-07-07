var stripe = Stripe("pk_test_51JxWFsEMDYePyYSgY8abIK9kH8sQpy6XAOPsmuNDXzlqoH4QajY4ImmCi6VwzqULBqOdofL3DlgFYLk7915RTWR700ll6TxnDh");

const button = document.querySelector('#buy_now_btn');

button.addEventListener('click', event => {
    stripe.redirectToCheckout({
        // Make the id field from the Checkout Session creation API response
        // available to this file, so you can provide it as parameter here
        // instead of the {{CHECKOUT_SESSION_ID}} placeholder.
        sessionId: "cs_test_a1QgYnhbINnbXouvWuOKGegUrs6kNxnRHTSQ3FPShDg6vq6B7JHCN4Cktg"
    }).then(function (result) {
        // If `redirectToCheckout` fails due to a browser or network
        // error, display the localized error message to your customer
        // using `result.error.message`.
    });
})