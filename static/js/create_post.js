
function uploadImage() {
    let extensionError = document.getElementById('extension-error');
    let pictureInput = document.getElementById('image');

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
            let picture = document.getElementById('post-image');
            picture.src = event.target.result;
            picture.style.maxWidth = '100%';
        }
    } else {
        extensionError.innerText = 'Ekstenzija nije dozvolljena...'
    }
}