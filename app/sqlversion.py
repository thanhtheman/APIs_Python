#--------------------------------------------------------------------------------------------------------------------------
#Postgres routes - before user registration table, all routes are in the main.py file, we will delete and move all of these codes into the router folder

# import psycopg2
# from psycopg2.extras import RealDictCursor

#At 3:55, we remove the below model to create a real postgre database
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     rating: Optional[int] = None
#     id: Optional[int]

# this is for Postgres, we moved this into a separate file schema.py at 5:33
# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True

#realdictcursor is to make sure we have all the column names on our ouput. This is how we connect to our Postgres database
# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='OhYeah123', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('Database Connected!')
# except Exception as error:
#     print('Connecting to Database Failed!')
#     print(error)


# @app.get('/')
# async def get():
#     return {'message': 'Hello World'}

# @app.get('/posts', response_model=List[schema.Post])
# async def get():
#     cursor.execute("""select * from posts""")
#     posts = cursor.fetchall()
#     return posts

#I need to "commit" and save the new post - conn.commit(), just like git

# @app.post('/posts', response_model=schema.Post, status_code = status.HTTP_201_CREATED)
# async def create_pots(post: schema.PostCreate):
#     cursor.execute("""insert into posts(title, content, published) values(%s, %s, %s) returning *""",(post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return new_post

# if we just pass %s as id, it won't work
# because the command is a string, so the id must be a string
# it s kind of not making sense to take an input as a string by nature in the url
#then we specify it must be an int - input validation

# @app.get("/posts/{id}", response_model=schema.Post)
# async def get_post(id: int):
#     cursor.execute("""select * from posts where id = %s""",(str(id)))
#     search_post = cursor.fetchone()
#     if not search_post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post doesn't exist!")
#     return search_post

# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_posts(id: int):
#     cursor.execute("""delete from posts where id = %s returning*""",(str(id)))
#     delete_post = cursor.fetchone()
#     conn.commit()
#     if delete_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist")
#     else:
#         Response(status_code=status.HTTP_204_NO_CONTENT)
#         return {'result': f'Post {id} has been successfully deleted!'}
            

# @app.put("/posts/{id}", response_model=schema.Post)
# async def update_post(id: int, post: schema.PostUpdate):
#     cursor.execute("""update posts set title = %s, content = %s, published =%s where id = %s returning*""", (post.title, post.content, post.published, str(id)))
#     updated_post = cursor.fetchone()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist. Nothing is updated!")
#     conn.commit()
#     return post     
    