$(document).ready(function() {

    // Moramo dohvatiti sve podatke za postove
    $.ajax({
        type: 'GET',
        url: '/get_posts'
    })
    .done(function(data){
        // uzimamo sve sto nam je potrebno
        // Uglavnom trebaju nam podaci samo za lajkovanje a to su:
        // 1.Kakvo ce biti dugme..
        // Increment lajka i decrement
        console.log('Stigli podaci');

        // Postavljanje isLiked kolone:
        for (let i = 0; i < data.length; i++) {
            if (data[i].whoLiked.includes(data[i].currentUser)) {
                data[i].isLiked = true;
            } else {
                data[i].isLiked = false;
            }
        }

        let likes = $('.like-number');
        let addLikeButtos = $('.like-btn');


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
        }
    });
});