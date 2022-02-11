    # Uzimamo sve postove
    """
        cursor = mydb.cursor(prepared = True)
        sql = 'SELECT * FROM post'
        cursor.execute(sql)
        posts_res = cursor.fetchall()

        if posts_res == None:
            return 'Nema nijednog posta na ovoj aplikaciji...'

        n = len(posts_res)
        posts_res = list(posts_res)
        posts = []

        for i in range(n):
            posts_res[i] = dekodiraj(posts_res[i])
            post_id = posts_res[i][0]
            title = posts_res[i][1]
            content = posts_res[i][2]
            image = posts_res[i][3]
            userID = posts_res[i][4]

            post = Post(post_id, title, content, image, userID)
            posts.append(post)
    """



    # Uzimamo sve usere iz baze
    """
        cursor = mydb.cursor(prepared = True)
    sql = 'SELECT * FROM user'
    cursor.execute(sql)
    users_res = cursor.fetchall()

    if users_res == None:
        return 'Nema nijednog korisnika na ovoj aplikaciji...'

    n = len(users_res)
    users_res = list(users_res)
    users = []

    for i in range(n):
        users_res[i] = dekodiraj(users_res[i])
        user_id = users_res[i][0]
        firstname = users_res[i][1]
        lastname = users_res[i][2]
        email = users_res[i][3]
        username = users_res[i][4]
        password = users_res[i][5]
        profile_image = users_res[i][6]

        user = User(user_id, firstname, lastname, email, username, password, profile_image)
        users.append(user)
    """
