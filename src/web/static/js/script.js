// Function to calculate the time difference between bed and wakeup time
function calculateDatetimeDifference() {
    const bedDateTime = bedDateTimeInput.value;
    const wakeupDateTime = wakeupDateTimeInput.value;

    if (bedDateTime && wakeupDateTime) {
        const bedDateTimeObj = new Date(bedDateTime);
        const wakeupDateTimeObj = new Date(wakeupDateTime);

        const datetimeDifference = wakeupDateTimeObj - bedDateTimeObj;
        const hours = Math.floor(datetimeDifference / (1000 * 60 * 60));
        const minutes = Math.floor((datetimeDifference % (1000 * 60 * 60)) / (1000 * 60));

        datetimeDifferenceOutput.textContent = `Duração do Sono: ${hours}h e ${minutes}min`;
    } else {
        datetimeDifferenceOutput.textContent = "Aguardando inserção de ambos os dados.";
    }
}

// Function to calculate the total percentage of sleep
function calculateTotalPercentage() {
    const awakePercentage = parseInt(awakePercentageInput.value);
    const remPercentage = parseInt(remPercentageInput.value);
    const lightPercentage = parseInt(lightPercentageInput.value);
    const deepPercentage = parseInt(deepPercentageInput.value);

    const totalPercentage = awakePercentage + remPercentage + lightPercentage + deepPercentage;
    totalPercentageOutput.textContent = `Porcentagem Total: ${totalPercentage}%`;

    return totalPercentage;
}

// Function to validate the total percentage of sleep
function validatePercentage() {
    totalPercentage = calculateTotalPercentage();
    if (totalPercentage !== 100) {
        alert("A soma das porcentagens deve ser igual a 100%");
        return false;
    }

    return true;
}

// Function to format the input value
function formatValue(value, type) {
    if (type === 'time') {
        if (value.length < 3 || value.length > 4) {
            return "__h __min";
        } else {
            return value.toString().slice(0, -2) + "h " + value.toString().slice(-2) + "min";
        }
    } else if (type === 'calories') {
        if (value.length < 1) {
            return "_ cal";
        } else {
            return value + " cal";
        }
    } else if (type === 'money') {
        if (value.length < 3) {
            return "R$ __.__";
        } else {
            const formatedValue = value.slice(0, -2) + "." + value.slice(-2);
            return "R$ " + formatedValue;
        }
    } else if (type === 'weight') {
        if (value.length !== 4) {
            return "__.__ kg";
        } else {
            const formatedValue = value.slice(0, -2) + "." + value.slice(-2);
            return formatedValue + " kg";
        }
    } else if (type === 'percentage') {
        if (value.length < 3 || value.length > 4) {
            return "__.__ %";
        } else {
            const formatedValue = value.slice(0, -2) + "." + value.slice(-2);
            return formatedValue + " %";
        }
    }
}

//  Function to check the button status
function checkButton(checkId, inputId, normalValue, checkedValue) {
    var element = document.getElementById(checkId);
    var inputElement = document.getElementById(inputId);
    if (element.classList.contains('check-true')) {
        element.classList.remove('check-true');
        inputElement.value = normalValue;
    } else {
        element.classList.add('check-true');
        inputElement.value = checkedValue;
    }
}

// Function to toggle the button status
function toggleButton(toggleId, textId, inputId) {
    var element = document.getElementById(toggleId);
    element.classList.toggle('toggle-true');

    var textElement = document.getElementById(textId);
    var spanElement = textElement.querySelector('span');
    var inputElement = document.getElementById(inputId);
    if (spanElement.innerText === 'Não') {
        spanElement.innerText = 'Sim';
        inputElement.value = 'True';
    } else {
        spanElement.innerText = 'Não';
        inputElement.value = 'False';
    }
}
// Function to update the output value
function updateOutput(inputElement, outputElement) {
    var value = inputElement.value;
    var classification = "";
    
    if (value == 0) {
        classification = "Falha";
    } else if (value >= 1 && value <= 13) {
        classification = "Derrota";
    } else if (value == 14 || value == 15) {
        classification = "Vitória";
    } else if (value == 16) {
        classification = "Sucesso";
    }
    
    outputElement.innerText = classification;
}

let selectedOption = null;

// Function to select an alternative option
function selectAlternative(id, inputId, value) {
    // let selectedOption = null;

    if (selectedOption !== null) {
        document.getElementById(`option${selectedOption}`).classList.remove('selected');
    }

    selectedOption = id;
    document.getElementById(`option${id}`).classList.add('selected');

    document.getElementById(inputId).value = value;
}
