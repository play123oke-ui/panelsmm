// Fungsi untuk melakukan request AJAX
<script src="script.js"></script>
function ajaxRequest(url, method, data, callback) {
    const xhr = new XMLHttpRequest();
    xhr.open(method, url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.onload = function() {
        if (xhr.status === 200) {
            callback(JSON.parse(xhr.responseText));
        } else {
            console.error(xhr.statusText);
        }
    };
    xhr.onerror = function() {
        console.error(xhr.statusText);
    };
    xhr.send(JSON.stringify(data));
}

// Fungsi untuk menghandle submit form
function handleSubmit(event) {
    event.preventDefault();
    const form = event.target;
    const data = {};
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(function(input) {
        data[input.name] = input.value;
    });
    ajaxRequest(form.action, form.method, data, function(response) {
        console.log(response);
    });
}

// Fungsi untuk menghandle klik tombol
function handleClick(event) {
    event.preventDefault();
    const button = event.target;
    const url = button.dataset.url;
    const method = button.dataset.method;
    const data = {};
    ajaxRequest(url, method, data, function(response) {
        console.log(response);
    });
}

// Tambahkan event listener untuk form
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', handleSubmit);
    });

    // Tambahkan event listener untuk tombol
    const buttons = document.querySelectorAll('button');
    buttons.forEach(function(button) {
        button.addEventListener('click', handleClick);
    });
});
