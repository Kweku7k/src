var paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener('submit', payWithPaystack, false);
function payWithPaystack() {
  var amount = localStorage.getItem('amount')
  console.log(amount) 
  var userId = localStorage.getItem('userId')
  console.log(userId) 
  var userName = localStorage.getItem('userName')
  // var slemail = userName.replace(/\s+/g, '');
  var email = "contestant"+userId+"@prestosl.com"
  console.log(userName)
  console.log(email)

  
  function intToFloat(num, decPlaces) { return num.toFixed(decPlaces); }
  // alert(intToFloat(12.5, 1)); // returns 12.0
  // alert(intToFloat(12, 2)); // returns 12.00

  var handler = PaystackPop.setup({
    key: 'pk_live_648228b4d09ff7a593456bae534339f0b58cd37f',
    email: email,
    amount: amount * 100, // the amount value is multiplied by 100 to convert to the lowest currency unit
    currency: 'GHS', // Use GHS for Ghana Cedis or USD for US Dollars	
    subaccount: "ACCT_jpwt9480ebqz0b8",
    ref: userId + 000 +''+Math.floor((Math.random() * 100000) + 1), // Use GHS for Ghana Cedis or USD for US Dollars

    callback: function(response) {
        console.log("Payment Successful")
        console.log(response)
        console.log(localStorage.getItem("userId"))
        var amount = localStorage.getItem("amount") * 100
        var reference = response.reference;
        console.log(reference)
        window.location.href = "/thanks/" + localStorage.getItem("userId") + "/" + amount + "/" + reference; 
        //this happens after the payment is completed successfully 
        // alert('Payment complete! Reference: ' + reference);
      // Make an AJAX call to your server with the reference to verify the transaction
    },
    onClose: function() {
      alert('Transaction was not completed,.');
      window.location.href = "/nothanks/" + localStorage.getItem("userId") + "/" + localStorage.getItem("amount")  ;
    },
  });
  handler.openIframe();
}

function test(){
  window.location.href = "/thanks/" + localStorage.getItem("userId") + "/" + localStorage.getItem("amount")
}
