let faqs = document.getElementsByClassName("faq-quiz");
    let i=0;
    for (i = 0; i < faqs.length; i++) {
        faqs[i].addEventListener("click", function () {
         
            /* hiding and showing the message */
            let message = this.nextElementSibling;
            if (message.style.display === "block") {
                message.style.display = "none";
            } else {
                message.style.display = "block";
            }
        });
    }