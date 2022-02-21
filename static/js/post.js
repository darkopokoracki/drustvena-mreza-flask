$(document).ready(function() {
    switchModals();
    showModals();
    likePost();
    commentPost();
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

    $.ajax({
        data: {
            postID: id
        },
        
        type: 'POST',
        url: '/get_post'
    })
    .done(function(likes_comments_data) {
        let likeModal = document.querySelector('.like-modal');

        // postavljamo broj lajkova
        let likeNumber = document.querySelector('.like-number');
        likeNumber.innerText = likes_comments_data[0].length;

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

function likePost() {
    let postID = document.querySelector('.postID');
    let id = parseInt(postID.id);


    $.ajax({
        data: {
            postID: id
        },
        
        type: 'POST',
        url: '/currentUser'
    })
    .done(function(data) {
        let likeIcon = document.querySelector('.fa-thumbs-up');
        let likeNumber = document.querySelector('.like-number');
        let likeModal = document.querySelector('.like-modal');
        let counter = 0; 

        if (likeIcon.classList[0] == 'fas') {
            counter = 1;
        } else if (likeIcon.classList[1] == 'far') {
            counter = 0;
        }
    
        likeIcon.addEventListener('click', () => {
            counter++;
    
            // Pravimo primerak lajka
            let userProfile = document.createElement('div');
            userProfile.classList.add('user-profile');
    
            let userImg = document.createElement('img');
            userImg.setAttribute('src', `/static/images/profile/${data.picture}`);
    
            let fullName = document.createElement('p');
            fullName.innerText = `${data.firstname} ${data.lastname}`;
    
            userProfile.append(userImg);
            userProfile.append(fullName);

    
            if (counter % 2 != 0) {
                likeIcon.classList.remove('far');
                likeIcon.classList.add('fas');
                let likesNow = parseInt(likeNumber.innerText);
                likeNumber.innerText = likesNow += 1;
                likeModal.append(userProfile);

            } else {
                likeIcon.classList.remove('fas');
                likeIcon.classList.add('far');
    
                let likesNow = parseInt(likeNumber.innerText);
                likeNumber.innerText = likesNow -= 1;
                likeModal.lastChild.remove();

            }

            // Saljemo podatke i na backend da bismo upisali u bazu podatka.
            let postID = document.querySelector('.postID');
            let id = parseInt(postID.id);

            let userID = document.querySelector('.userID');
            let whomLiked = parseInt(userID.id);

            $.ajax({
                data: {
                    'whomLiked': whomLiked,
                    'postID': id
                },

                type: 'POST',
                url: '/add_like'
            })
            .done(function(data){

            });

        });
    });
}


function commentPost() {
    // Sta nam treba:
    // Kome i koji post komentarisemo -> OK
    // Treba nam nas profil, firstname, username, profilepicture

    let postID = document.querySelector('.postID');
    let id = parseInt(postID.id);


    $.ajax({
        data: {
            postID: id
        },
        
        type: 'POST',
        url: '/currentUser'
    })
    .done(function(data) {
        // Trebaju nam sva polja:
        let sendButton = document.querySelector('.add-comment-btn');
        let commentInput = document.querySelector('#comment-input');

        let postID = document.querySelector('.postID');
        let id = parseInt(postID.id);

        sendButton.addEventListener('click', () => {
            // Prvo frontend - pravimo primerak komentara:
            let oneComment = document.createElement('div');
            oneComment.classList.add('one-comment');

            let a = document.createElement('a');
            let userImg = document.createElement('img');
            userImg.setAttribute('src', `/static/images/profile/${data.picture}`);

            a.appendChild(userImg)

            let contentContainer = document.createElement('div');
            contentContainer.classList.add('content-container');

            let fullName = document.createElement('h3');
            fullName.innerText = `${data.firstname} ${data.lastname}`;

            let commentContent = document.createElement('p');
            commentContent.classList.add('comment-content');
            commentContent.innerText = `${commentInput.value}`;

            contentContainer.appendChild(fullName);
            contentContainer.appendChild(commentContent);

            oneComment.appendChild(a);
            oneComment.appendChild(contentContainer);
            console.log(oneComment)

            document.querySelector('.read-comment-container').appendChild(oneComment);
            
            // Sada mozemo da poslajemo i na backend.
            $.ajax({
                data: {
                    content: commentInput.value,
                    postID: id
                },

                type: 'POST',
                url: '/add_comment'
            })
            .done(function(data) {

            });

        });
    });
}