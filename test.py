from main import posts


posts_res = [[1, 'Moj Prvi auto', 'Ovo je moj prvi auto koji sam kupio od gradjevine...\r\n ', 'car3.jpg', 1], [2, 'Gluvak', 'Danas smo sredjivali ovu sobu i prodali llijentu za 1000eur\r\n ', 'enterior.jpg', 2], [3, 'Ovo je moj kuca', 'joooojo sto jeeee mioooo ', 'pexels-valeria-boltneva-1805164.jpg', 5]]
who_liked = [[1, 1], [2, 2], [1, 1], [2, 2], [1, 1], [2, 2], [1, 1], [3, 5], [3, 5]]

y = []
for i in range(len(posts_res)):
    i = []
    for j in range(len(who_liked)):
        if posts_res[i][0] == who_liked[j][0]:
            i.append(who_liked[j][1])
    y.append(i)

print(y)

print(len(posts_res))