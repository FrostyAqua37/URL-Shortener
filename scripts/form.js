$(document).ready(function() {
         $('form').submit(function(event) {
            event.preventDefault();
            $.ajax({
               type: 'POST',
               url: '/',
               data: $('form').serialize(),
               success: function() {
                    document.getElementById("long-url").innerHTML = "<h2>Hello World</h2>";
                    alert('Form submitted!');
               }
            });
         });
      });
    