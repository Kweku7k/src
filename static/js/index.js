var paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener('submit', payWithPaystack, false);
function payWithPaystack() {
    console.log('Paid')
  var handler = PaystackPop.setup({
    key: 'pk_live_648228b4d09ff7a593456bae534339f0b58cd37f',
    email: 'mr.adumatta@gmail.com',
    amount: 3 * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit
    currency: 'GHS', // Use GHS for Ghana Cedis or USD for US Dollars

    callback: function(response) {
        console.log("Payment Successful")
      //this happens after the payment is completed successfully
      var reference = response.reference;
      alert('Payment complete! Reference: ' + reference);
      // Make an AJAX call to your server with the reference to verify the transaction
    },
    onClose: function() {
      alert('Transaction was not completed, window closed.');
    },
  });
  handler.openIframe();
}
