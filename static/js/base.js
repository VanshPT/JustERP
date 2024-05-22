document.addEventListener("DOMContentLoaded", function() {
    const toggleButton = document.getElementById("toggle-sidebar");
    const sidebar = document.querySelector("aside");
    const mainArea = document.querySelector("main");
    const mainAreaWhite = document.querySelector(".main-area")
    const header = document.querySelector("header");
    const custtOuter = document.querySelector(".custt-outer");
    const logoContainerOff= document.getElementById("toggle-off-logo");

    toggleButton.addEventListener("click", function() {
      document.body.classList.add("transitioning");
      if (sidebar.parentNode === document.body) {
        // If aside element is in the body, remove it
        document.body.removeChild(sidebar);
        // Adjust main area width to fill the space
        mainArea.classList.remove("ml-60");
        // Adjust header left position
        header.style.left = "0";
        // Align the button to the left
        custtOuter.style.width = "100%";
        //push main area right
        mainAreaWhite.style.marginLeft= "15rem";
        //add justerp symbol when aside toggled off in header
        logoContainerOff.innerHTML="<h1><span class='main-logo-design'>JustERP</span></h1>";

      } else {
        // If aside element is not in the body, add it back
        document.body.appendChild(sidebar);
        // Restore main area width
        mainArea.classList.add("ml-60");
        // Restore header left position
        header.style.left = "10rem";
        // Restore button alignment
        custtOuter.style.width = "auto";
        //remove justerp symbol when aside toggled off in header
        logoContainerOff.innerHTML="";
      }
      // Set toggle icon margin left to 1rem regardless of the aside state
      toggleButton.style.marginLeft = "1rem";
      
      setTimeout(function() {
      document.body.classList.remove("transitioning");
    }, 300);

    });
  });
  // popover initialization 
  const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
  const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))