from fastapi import FastAPI ,HTTPException , Depends  #fasapi yi içe aktardık
from pydantic import BaseModel,Field
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session



app = FastAPI()   # nesnenin fastapiye eşit olduğunu soyledik.


models.Base.metadata.create_all(bind = engine)


def get_db():
    try:
        db =SessionLocal()   ## Yeni bir oturum oluşturur
        yield db                 # Bu oturumu bağımlılık olarak sağlar
    finally:
        db.close()           # Oturumu kapatır ve kaynakları serbest bırakır



class Book(BaseModel):
    title : str =Field(min_length=1)
    author : str = Field(min_length=1,max_length=100)
    description :str =Field(min_length=1,max_length=100)
    rating : int =Field(gt = -1,lt = 101)   #  0-100 arasında tam sayı olacak.
    
    
    
BOOKS =[]


@app.get("/")    #fastapi ye bunun bir alma isteği olduğunu bildiriyoruz.
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Books).all()



@app.post("/")
def create_book(book : Book, db:Session = Depends(get_db)):
    book_model = models.Books()
    book_model.title =book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.raiting = book.rating
    
    db.add(book_model)
    db.commit()  # veritabanına uygulanıyor.
    
    return book
    
    
    
   
@app.put("/{book_id}")
def update_book(book_id : int , book :Book , db: Session = Depends(get_db)):
    
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    
    if book_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {book_id} : Does not exist"
        )
                
    book_model.title =book.title
    book_model.author = book.author
    book_model.description = book.description
    book_model.raiting = book.rating
    
    db.add(book_model)
    db.commit()
    
    return book
    
             

@app.delete("/{book_id}")
def delete_book(book_id : int ,  db: Session = Depends(get_db)):
    book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
    if book_model is None:
        raise HTTPException(
            status_code= 404,
            detail= f"ID {book_id} : Does not exist"
        )
    
    # db.delete(book_model)
    
    db.query(models.Books).filter(models.Books.id == book_id).delete()
  
   
    
    db.commit()
    return f"Silme işlemi başarılı.."




   
    
    
    
    