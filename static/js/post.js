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
    let postID = document.querySelector('.postID');
    let id = parseInt(postID.id);
    console.log(id);

    $.ajax({
        data: {
            postID: id
        },
        
        type: 'POST',
        url: '/get_post'
    })
    .done(function(like_data) {
        console.log(like_data);
        let likeModal = document.querySelector('.like-modal');

        for (let i = 0; i < like_data.length; i++) {
            // Sada treba napraviti jedan primerak
            let userProfile = document.createElement('div');
            userProfile.classList.add('user-profile');

            let userImg = document.createElement('img');
            userImg.setAttribute('src', `/static/images/profile/${like_data[i].profile_image}`);

            let fullName = document.createElement('p');
            fullName.innerText = `${like_data[i].firstname} ${like_data[i].lastname}`;

            userProfile.append(userImg);
            userProfile.append(fullName);

            likeModal.append(userProfile);
        }   
    });
}

function showCommentModal() {   

}