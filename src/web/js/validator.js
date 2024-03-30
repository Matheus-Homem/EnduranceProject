function validatePercentage() {
    var awakePercentage = parseInt(document.getElementById("awakePercentage").value);
    var remPercentage   = parseInt(document.getElementById("remPercentage").value);
    var lightPercentage = parseInt(document.getElementById("lightPercentage").value);
    var deepPercentage  = parseInt(document.getElementById("deepPercentage").value);

    var totalPercentage = awakePercentage + remPercentage + lightPercentage + deepPercentage;

    if (totalPercentage !== 100) {
        alert("A soma das porcentagens deve ser igual a 100%");
        return false;
    }

return true;
}



export { validatePercentage };