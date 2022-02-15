// Kada se ucita stranica, mozemo poceti sa radom...
$(document).ready(function() {
    

    // Moramo dohvatiti sve podatke za postove
    $.ajax({
        type: 'POST',
        url: '/get_posts'
    })
    .done(function(data){
        let loggedUser = $('#logged-user').attr('class');
        console.log(loggedUser);
        // uzimamo sve sto nam je potrebno
        // Uglavnom trebaju nam podaci samo za lajkovanje a to su:
        // 1. Kakvo ce biti dugme..
        // 2. Increment lajka i decrement
        console.log('Stigli podaci');
        console.log(data);
        // Postavljanje isLiked kolone:
        // Uglavnom cuvamo podatak u objektu kkoji nam pokazuje da li je trnutni korisnik lajkovao post
        for (let i = 0; i < data.length; i++) {
            if (data[i].whoLiked.includes(data[i].currentUser[0])) {
                data[i].isLiked = true;
            } else {
                data[i].isLiked = false;
            }
        }

        let likes = $('.like-number');
        let addLikeButtos = $('.like-btn');            
        let commentSections = $('.comment-section');
        let commentButtons = $('.comment-btn');
        let addCommentButtons = $('.add-comment-btn');
        let readCommentContainers = $('.read-comment-container');

        for (let i = 0; i < addLikeButtos.length; i++) {
            if (addLikeButtos[i])

            addLikeButtos[i].addEventListener('click', (e) => {
                e.preventDefault();
    
                let whomLiked = e.target.parentElement.children[1].id // Ko je lajkovao
                let postID = e.target.parentElement.children[2].id  // Koji post je lajkovan
                
                if (data[i].isLiked === true) {
                    data[i].likes -= 1;
                    likes[i].innerText = data[i].likes;
                    e.target.children[0].classList.remove('fas');
                    e.target.children[0].classList.add('far');
                    likes[i].parentElement.children[0].classList.remove('fas');
                    likes[i].parentElement.children[0].classList.add('far');

                    data[i].isLiked = false
                } else {
                    data[i].likes += 1;
                    likes[i].innerText = data[i].likes;
                    e.target.children[0].classList.remove('far');
                    e.target.children[0].classList.add('fas');
                    likes[i].parentElement.children[0].classList.remove('far');
                    likes[i].parentElement.children[0].classList.add('fas');

                    data[i].isLiked = true;
                }

                $.ajax({
                    data: {
                        whomLiked: whomLiked,
                        postID: postID
                    },
                    
                    type: 'POST',
                    url: '/add_like'
                })
                .done(function(data) {
                    
                });
            });


            // Za komentre
            commentButtons[i].addEventListener('click', (e) => {
                commentSections[i].classList.toggle('d_none');
            });
            
            addCommentButtons[i].addEventListener('click', (e) => {
                let content = e.target.parentElement.children[2].value;
                let postID = data[i].postID;
                let firstname = data[i].currentUser[1];
                let lastname = data[i].currentUser[2];
                let picture = data[i].currentUser[3];

                // Rucno pravljenje jednog komentara preko Javascripta
                // Cisti Javascript 
                let oneComment = document.createElement('div');
                oneComment.classList.add('one-comment');

                let a = document.createElement('a');
                a.setAttribute('href', `/profile/${data[i].currentUser[4]}`);
                
                let img = document.createElement('img');
                img.setAttribute('src', `/static/images/profile/${picture}`);

                a.appendChild(img);
                oneComment.appendChild(a);

                let icon = document.createElement('i');
                icon.classList.add('fas');
                icon.classList.add('fa-circle');
                icon.classList.add('active');

                oneComment.appendChild(icon);

                let contentContainer = document.createElement('div');
                contentContainer.classList.add('content-container');

                let heading = document.createElement('h3');
                heading.innerText = `${firstname} ${lastname}`;
                
                let commentContent = document.createElement('p');
                commentContent.classList.add('comment-content');
                commentContent.innerText = content;  //Promenljiva iz inputa...

                contentContainer.appendChild(heading);
                contentContainer.appendChild(commentContent);
                
                oneComment.appendChild(contentContainer);
        

                // Dodajemo napravljeni komentar u komentarsku sekciju posta...
                // Ali pre toga moramo proveriti..
                if (content == "" || content == null) {
                    e.target.parentElement.children[2].style.outline = '2px solid red';
                    const outlineTimeout = setTimeout(() => {
                        e.target.parentElement.children[2].style.removeProperty('outline');
                    }, 2000);
                } else {
                    readCommentContainers[i].appendChild(oneComment);
                    e.target.parentElement.children[2].value = '';

                    $.ajax({
                        data: {
                            content: content,
                            postID: postID
                        },
    
                        type: 'POST',
                        url: '/add_comment'
                    })
                    .done(function(data){
                        console.log('Podaci su uspesno posalti');
                        console.log(data)
                    });
                }
            });
        }
    });
});