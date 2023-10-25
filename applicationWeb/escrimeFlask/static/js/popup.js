window.addEventListener("load", function () {
    // Le code à exécuter une fois que la page et toutes les ressources ont été chargées
    let btnPopup = document.getElementsByClassName("btn-close")[0];

    console.log(btnPopup);
    if(btnPopup !== undefined){
        btnPopup.addEventListener("click", function(e){
          let popup = document.getElementsByClassName("wrap_popup")[0];
          console.log(popup)
          popup.style.visibility = "hidden";
        });

    }
  });