$(document).ready(function() {


    let loggedUser = document.querySelector('.logged-user').id;
    let addLikeButtos = $('.like-btn');
    let icons = $('.fas');
    let likes = $('.like-number'); // Svi lajkovi od svakog posta.



    for (let i = 0; i < addLikeButtos.length; i++) {
        addLikeButtos[i].addEventListener('click', (e) => {
            e.preventDefault();

            let whomLiked = e.target.parentElement.children[1].id // Ko je lajkovao
            let postID = e.target.parentElement.children[2].id  // Koji post je lajkovan
            
            console.log(whomLiked);
            console.log(postID);
            console.log(likes[postID]);


            $.ajax({
                data: {
                    whomLiked: whomLiked,
                    postID: postID
                },
                
                type: 'POST',
                url: '/add_like'
            })
            .done(function(data) {
                console.log(data)
            });
        });
    }
});