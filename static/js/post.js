$(document).ready(function() {
    showModal();
    showLikeModal();
    showCommentModal();
});

function showModal() {
    let checkbox = document.querySelector('.switch-button-checkbox');
    let likeModal = document.querySelector('.like-modal');
    let commentModal = document.querySelector('.comment-modal');
    let counter = 0;

    checkbox.addEventListener('click', () => {
        counter++;
        
        if (counter % 2 != 0) {
            likeModal.classList.add('d_none');
            commentModal.classList.remove('d_none');
        } else {
            likeModal.classList.remove('d_none');
            commentModal.classList.add('d_none');
        }
    });
}

function showLikeModal() {
    
}

function showCommentModal() {   

}