function main() {

    // Edit buttons
    let firstnameEditBtn = document.getElementById('for-firstname');
    let lastnameEditBtn = document.getElementById('for-lastname');
    let usernameEditBtn = document.getElementById('for-username');
    let firstnameOkBtn = document.getElementById('firstname-ok');
    let lastnameOkBtn = document.getElementById('lastname-ok');
    let usernameOkBtn = document.getElementById('username-ok');

    // Input fields
    let firstnameInput = document.getElementById('firstname');
    let lastnameInput = document.getElementById('lastname');
    let usernameInput = document.getElementById('username');

    // Personal Info
    let firstnameInfo = document.getElementById('firstname-info');
    let lastnameInfo = document.getElementById('lastname-info');
    let usernameInfo = document.getElementById('username-info');



    firstnameEditBtn.addEventListener('click', (e) => {
        e.preventDefault();

        firstnameInput.parentElement.classList.toggle('d_none');
    });

    lastnameEditBtn.addEventListener('click', (e) => {
        e.preventDefault();

        lastnameInput.parentElement.classList.toggle('d_none');
    });

    usernameEditBtn.addEventListener('click', (e) => {
        e.preventDefault();

        usernameInput.parentElement.classList.toggle('d_none');
    });



    firstnameOkBtn.addEventListener('click', (e) => {
        e.preventDefault();
        firstnameInfo.innerText = firstnameInput.value;
        firstnameInput.parentElement.classList.add('d_none');
    });

    lastnameOkBtn.addEventListener('click', (e) => {
        e.preventDefault();
        lastnameInfo.innerText = lastnameInput.value;
        lastnameInput.parentElement.classList.add('d_none');
    });

    usernameOkBtn.addEventListener('click', (e) => {
        e.preventDefault();
        usernameInfo.innerText = '@' + usernameInput.value;
        usernameInput.parentElement.classList.add('d_none');
    });
}

// Pocinje deo za profilnu sliku
// Funkcija je pokrenuta pomocu onchange dogadjaja

function setProfilePicture() {
    let extensionError = document.getElementById('extension-error');
    let pictureInput = document.getElementById('profile-picture');

    let picturePath = pictureInput.value;
    let pictureExtension = picturePath.split('.').slice(-1)[0];
    let allowed = false;
    
    let allowd_extensions = ['png', 'jpg', 'jpeg'];

    for (let i = 0; i < allowd_extensions.length; i++) {
        if (pictureExtension === allowd_extensions[i]) {
            allowed = true;
        }
    }

    if (allowed === true) {
        extensionError.innerText = '';
        let fReader = new FileReader();
        fReader.readAsDataURL(pictureInput.files[0]);
        fReader.onloadend = function(event) {
            let picture = document.querySelector('.edit-picture img');
            picture.src = event.target.result;
        }
    } else {
        extensionError.innerText = 'Ekstenzija nije dozvolljena...'
    }

}


window.addEventListener('load', main);