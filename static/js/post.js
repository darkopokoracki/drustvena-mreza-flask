$(document).ready(function() {
    switchModals();
    showModals();
});

function switchModals() {
    let checkbox = document.querySelector('.switch-button-checkbox');
    let likeModal = document.querySelector('.like-modal');
    let commentModal = document.querySelector('.comment-modal');
    let counter = 0;

    checkbox.addEventListener('click', () => {
        counter++;
        
        if (counter % 2 != 0) {
            likeModal.classList.add('d_none');
            commentModal.classList.remove('d_none');
            document.querySelector('.right-side').style.backgroundColor = 'rgb(200, 200, 200)';
        } else {
            likeModal.classList.remove('d_none');
            commentModal.classList.add('d_none');
            document.querySelector('.right-side').style.backgroundColor = 'rgb(240, 240, 240)';
        }
    });
}

function showModals() {
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
    .done(function(likes_comments_data) {
        console.log('Stigli smo do ovde gde hocemo');
        console.log(likes_comments_data);
        let likeModal = document.querySelector('.like-modal');

        for (let i = 0; i < likes_comments_data[0].length; i++) {
            // Sada treba napraviti jedan primerak
            let userProfile = document.createElement('div');
            userProfile.classList.add('user-profile');

            let userImg = document.createElement('img');
            userImg.setAttribute('src', `/static/images/profile/${likes_comments_data[0][i].profile_image}`);

            let fullName = document.createElement('p');
            fullName.innerText = `${likes_comments_data[0][i].firstname} ${likes_comments_data[0][i].lastname}`;

            userProfile.append(userImg);
            userProfile.append(fullName);

            likeModal.append(userProfile);
        }
        
        let commentModal = document.querySelector('.comment-modal');
        console.log(commentModal);

        for (let i = 0; i < likes_comments_data[1].length; i++) {
            // Pravimo jedan primerak komentara...
            let oneComment = document.createElement('div');
            oneComment.classList.add('one-comment');

            let a = document.createElement('a');
            let userImg = document.createElement('img');
            userImg.setAttribute('src', `/static/images/profile/${likes_comments_data[1][i].profile_image}`);

            a.appendChild(userImg)

            let contentContainer = document.createElement('div');
            contentContainer.classList.add('content-container');

            let fullName = document.createElement('h3');
            fullName.innerText = `${likes_comments_data[1][i].firstname} ${likes_comments_data[1][i].lastname}`;

            let commentContent = document.createElement('p');
            commentContent.classList.add('comment-content');
            commentContent.innerText = `${likes_comments_data[1][i].content}`;

            contentContainer.appendChild(fullName);
            contentContainer.appendChild(commentContent);

            oneComment.appendChild(a);
            oneComment.appendChild(contentContainer);

            // Konacno napravljeni primerak da apendujemo u sekciju komentara
            document.querySelector('.read-comment-container').appendChild(oneComment);
        }

    });
}
