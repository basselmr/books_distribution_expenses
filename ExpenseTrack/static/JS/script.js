function deleteAction(form,delValue) {
    if (confirm('Are you sure you want to delete "' + delValue + '"?')) {
        return true; // Submit the form
    }
    return false; // Cancel form submission
}

function updateAction(form){
    try {
        var rowInput = form.parentElement.querySelector('#rowInput');
        console.log(rowInput.value)
        const regex = /^(?:[a-zA-Z0-9\s',./]+|[^\W_]+)$/u;
        if (!regex.test(rowInput.value)) {
            alert("Invalid text.");
            return false;
        } else {
            var newInput = document.createElement('input');
            newInput.type = 'hidden';
            newInput.name = 'updateValue'; // Set the name attribute
            newInput.value = rowInput.value; // Set a default value if needed
            // Append the new input element to the form
            form.appendChild(newInput);
            console.log(form)
            return true;
        }               
    } catch (error) {
        console.error(error); // Log any errors that occur
    }
    return false;
}

function search(searchURL,searchQueryParam) {
    var searchValue = document.getElementById("searchedText").value
    //console.log(searchValue)
    if (searchValue){
        console.log(searchValue)
    }
    if (searchValue){
        //window.location.href = "/categories" + "?" + "category=" + encodeURIComponent(searchValue);   
        window.location.href = searchURL + "?" + searchQueryParam + encodeURIComponent(searchValue);   
    } else {
        //window.location.href = "/categories"
        window.location.href = searchURL
    }           
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function addNew (URL,bodyParam) {
    const inputText = document.getElementById("newRecord").value;
    console.log(inputText);
    if (!inputText.trim()) {
        console.log("New " + bodyParam +" is required.");
        document.getElementById("newErr").innerHTML="New " + bodyParam +" title is required."
        return
    } else {
        const regex = /^(?:[a-zA-Z0-9\s',./]+|[^\W_]+)$/u;
        if (!regex.test(inputText)) {
            document.getElementById("newErr").innerHTML="Only numeric, alphabetic characters accepted."
            console.log("Only numeric, alphabetic characters accepted.");
            return
        } else {
            const csrftoken = getCookie('csrftoken');
            console.log(csrftoken)
            const options = {
                method: 'POST',
                headers: {
                    cookie: 'csrftoken='+csrftoken,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: `{"${bodyParam}":"${inputText}"}`
            };
            fetch(URL, options)
            .then(response => {
                if (response.status === 201) {
                    // Handle success with status 201
                    return response.text(); // Read response as text
                } else {
                    // Handle other status codes
                    return response.json(); // Parse JSON response
                }
            })
            .then(data => {
                // Handle response data for other status codes
                if (typeof data === 'string') {
                    // If response is HTML page, replace current page content with it
                    document.documentElement.innerHTML = data;
                } else {
                    // Handle JSON response
                    console.log(data);
                    document.getElementById("newErr").innerHTML = data.error;
                }
            })
            .catch(err => console.error(err)); // Handle fetch error
        }
    }
}