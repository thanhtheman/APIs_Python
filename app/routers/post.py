


#sqlalchemy routes
@app.get('/sqlalchemy', response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.post('/sqlalchemy/post', response_model=schema.Post, status_code = status.HTTP_201_CREATED)
#the 'Post' below is the above class POST, not the Post from the models 
def create_post(post: schema.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.get('/sqlalchemy/posts/{id}', response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    search_post = db.query(models.Post).filter(models.Post.id == id).first()
    if not search_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail="This post doesn't exist!")
    return search_post

@app.delete("/sqlalchemy/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist")
    else:
        deleted_post.delete(synchronize_session = False)
        db.commit()
        Response(status_code=status.HTTP_204_NO_CONTENT)
        return {'result': f'Post {id} has been successfully deleted!'}

@app.put("/sqlalchemy/posts/{id}", response_model=schema.Post)
def update_post(id: int, post: schema.PostUpdate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    target_post = post_query.first()
    if target_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with {id} doesn't exist. Nothing is updated!")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post