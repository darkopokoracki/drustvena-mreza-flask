function main() {
    likeNumber = document.getElementsByClassName('like-number');

    for (let i = 0; i < likeNumber.length; i++) {
        likeNumber[i].addEventListener('click', openLikesModal)
    }
}

function openLikesModal() {
    console.log('open')
    whoLikedForm = document.querySelector('.who-liked-form input');
    console.log(whoLikedForm)
    whoLikedForm.submit()
    console.log('Submitovali smo formu...');
}


window.addEventListener('load', main);
