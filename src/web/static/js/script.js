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
        if (value.length < 4 || value.length > 5) {
            return "__'__''";
        } else {
            const minutes = value.slice(0, -2);
            const seconds = value.slice(-2);
            return minutes + "'" + seconds + "''";
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
    // Deselect all options in the group
    const options = document.querySelectorAll(`input[name="${inputName}"]`);
    options.forEach(option => {
        if (option.value === value) {
            option.checked = true; // Check the radio input that matches the value
        }
    });

    // Update visual selection
    if (selectedOption !== null) {
        document.getElementById(`option${selectedOption}`).classList.remove('selected');
    }
    selectedOption = id;
    document.getElementById(`option${id}`).classList.add('selected');
}

function selectAlternativeOverwrite(id, questionGroup, answer) {
    // Query all alternatives within the same question group
    const alternatives = document.querySelectorAll(`.alternative[data-question-group="${questionGroup}"]`);
    
    // Remove `.selected` class from all alternatives to ensure only one is selected at a time
    alternatives.forEach(alternative => {
        alternative.classList.remove('selected');
    });
    
    // Add `.selected` class to the clicked alternative
    const selectedAlternative = document.getElementById(id);
    if (selectedAlternative) {
        selectedAlternative.classList.add('selected');
    }
    
    // Optional: Handle the answer, e.g., send it to a server or log
    console.log(`Answer for ${questionGroup}: ${answer}`);
}


let rowIndex = 1;  // Keep track of the number of rows

// Function to toggle the button status
function toggleButton(suffixId) {
    const toggleId = `toggle_${suffixId}`;
    const inputId = `input_${suffixId}`;

    const toggleElement = document.getElementById(toggleId);
    const inputElement = document.getElementById(inputId);

    toggleElement.classList.toggle('toggle-true');

    inputElement.value = (inputElement.value === 'True') ? 'False' : 'True';
}


function addRow() {
    const formContainer = document.getElementById('form-container');
    const newRow = document.createElement('div');
    newRow.setAttribute('input-index', rowIndex);

    newRow.innerHTML = `
        <div class="anima-row">
            <div class="anima-cell cell-100 text-input">
                <input type="text" name="text_wisdom_navigator_book_${rowIndex}" placeholder="Nome do Livro">
            </div>
        </div>
        <div class="anima-row">
            <div class="anima-cell cell-33">
                <div id="id_read_${rowIndex}" class="check" onclick="checkButton('id_read_${rowIndex}', 'input_wisdom_navigator_read_${rowIndex}', 'False', 'True')">
                    <span><i class="fas fa-glasses"></i></span>
                </div>
                <input type="hidden" id="input_wisdom_navigator_read_${rowIndex}" name="bool_wisdom_navigator_read_${rowIndex}" value="False">
            </div>
            <div class="anima-cell cell-33">
                <div id="id_listen_${rowIndex}" class="check" onclick="checkButton('id_listen_${rowIndex}', 'input_wisdom_navigator_listen_${rowIndex}', 'False', 'True')">
                    <span><i class="fas fa-headphones-alt"></i></span>
                </div>
                <input type="hidden" id="input_wisdom_navigator_listen_${rowIndex}" name="bool_wisdom_navigator_listen_${rowIndex}" value="False">
            </div>
            <div class="anima-cell cell-33">
                <div id="id_notes_${rowIndex}" class="check" onclick="checkButton('id_notes_${rowIndex}', 'input_wisdom_navigator_notes_${rowIndex}', 'False', 'True')">
                    <span><i class="fas fa-quote-right"></i></span>
                </div>
                <input type="hidden" id="input_wisdom_navigator_notes_${rowIndex}" name="bool_wisdom_navigator_notes_${rowIndex}" value="False">
            </div>
        </div>
    `;

    formContainer.appendChild(newRow);
    rowIndex++;
}


function removeRow() {
    const formContainer = document.getElementById('form-container');
    if (formContainer.childElementCount > 1) {
        formContainer.removeChild(formContainer.lastChild);
        rowIndex--;
    }
}