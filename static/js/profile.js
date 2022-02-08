function main() {
    let postsContent = document.querySelectorAll('.post-content p');
    let counter = 0; // Za toggle button

    // Ako je opis dugacak, ogranicimo ga na 67 karaktera plus 3 tacke
    // Kada korisnik klikne na Read more, moci ce da procita ceo tekst.
    for (let i = 0; i < postsContent.length; i++) {
        let fullText = postsContent[i].innerText;

        if (postsContent[i].innerText.length > 67) {
            let first70 = postsContent[i].innerText.substring(0, 67);
            postsContent[i].innerText = first70 + '...';

            let readMoreBtn = document.createElement('button');
            readMoreBtn.innerText = 'Read more';
            readMoreBtn.className = 'read-more-btn';

            // Dodajemo read more button samo tamo gde je tekst dugacak
            postsContent[i].parentElement.appendChild(readMoreBtn);

            // Kada kliknemo na read more, ucitavamo ceo tekst
            readMoreBtn.addEventListener('click', (e) => {
                if (counter % 2 === 0) {
                    readMoreBtn.parentElement.children[0].innerHTML = fullText;
                    readMoreBtn.innerText = 'Read less';
                } else {
                    readMoreBtn.parentElement.children[0].innerHTML = first70 + '...';
                    readMoreBtn.innerHTML = 'Read more';
                }

                counter++;
            });
        }
    }
}

window.addEventListener('load', main);
