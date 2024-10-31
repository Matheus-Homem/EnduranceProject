document.addEventListener("DOMContentLoaded", function() {
    const accordionButtons = document.querySelectorAll(".accordion-button");

    accordionButtons.forEach(button => {
        button.addEventListener("click", function() {
            const content = this.nextElementSibling;

            if (content.style.maxHeight) {
                content.style.maxHeight = null;
            } else {
                document.querySelectorAll('.accordion-content').forEach(item => item.style.maxHeight = null);
                content.style.maxHeight = content.scrollHeight + "px";
            }
        });
    });
});

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

// Function to format the input value
function formatValue(value, type) {
    if (type === 'time') {
        if (value.length < 3 || value.length > 4) {
            return "__h __min";
        } else {
            const hours = value.slice(0, -2);
            const minutes = value.slice(-2);
            return hours + "h " + minutes + "min";
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
            const unit = value.slice(0, -2);
            const decimal = value.slice(-2);
            return "R$ " + unit + "." + decimal;
        }
    } else if (type === 'weight') {
        if (value.length !== 4) {
            return "__.__ kg";
        } else {
            const unit = value.slice(0, -2);
            const decimal = value.slice(-2);
            return unit + "." + decimal + " kg";
        }
    } else if (type === 'percentage') {
        if (value.length < 3 || value.length > 4) {
            return "__.__ %";
        } else {
            const unit = value.slice(0, -2);
            const decimal = value.slice(-2);
            return unit + "." + decimal + " %";
        }
    } else if (type === 'distance') {
        if (value.length < 3) {
            return "__.__ km";
        } else {
            const unit = value.slice(0, -2);
            const decimal = value.slice(-2);
            return unit + "." + decimal + " km";
        }
    } else if (type === 'exercise') {
        if (value.length !== 6) {
            return "__h__'__''";
        } else {
            const hour = value.slice(0, 2);
            const minutes = value.slice(2, 4);
            const seconds = value.slice(-2);
            return hour + "h " + minutes + "' " + seconds + "''";
        }
    } else if (type === 'bpm') {
        if (value.length < 2 || value.length > 3) {
            return "_ bpm";
        } else {
            return value + " bpm";
        }
    }
}


function updateOutput(outputId, value, type) {
    document.getElementById(outputId).value = formatValue(value, type);
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

let selectedOption = null;

// Function to select an alternative option
function selectAlternative(id, inputName, value) {
    const options = document.querySelectorAll(`input[name="${inputName}"]`);
    options.forEach(option => {
        if (option.value === value) {
            option.checked = true;
        }
    });

    if (selectedOption !== null) {
        document.getElementById(`option${selectedOption}`).classList.remove('selected');
    }
    selectedOption = id;
    document.getElementById(`option${id}`).classList.add('selected');
}

function selectAlternativeOverwrite(id, questionGroup, answer) {
    const alternatives = document.querySelectorAll(`.alternative[data-question-group="${questionGroup}"]`);
    alternatives.forEach(alternative => {
        alternative.classList.remove('selected');
    });
    
    const selectedAlternative = document.getElementById(id);
    if (selectedAlternative) {
        selectedAlternative.classList.add('selected');
    }
    
    console.log(`Answer for ${questionGroup}: ${answer}`);
}


// Function to toggle the button status
function toggleButton(suffixId) {
    const toggleId = `toggle_${suffixId}`;
    const inputId = `input_${suffixId}`;

    const toggleElement = document.getElementById(toggleId);
    const inputElement = document.getElementById(inputId);

    toggleElement.classList.toggle('toggle-true');

    inputElement.value = (inputElement.value === 'True') ? 'False' : 'True';
}


function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    const action = form.getAttribute('action');
    const maxAttempts = 3;

    function trySubmit(attempt) {
        fetch(action, {
            method: 'POST',
            body: new FormData(form),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (data.message === 'Form successfully submitted!') {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error(`Error submitting the form on attempt ${attempt}:`, error);
            if (attempt < maxAttempts) {
                setTimeout(() => trySubmit(attempt + 1), 1000);
            } else {
                alert('Error submitting the form after multiple attempts.');
            }
        });
    }

    trySubmit(1);
}