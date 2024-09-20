import grpc
from concurrent import futures

from protos import book_pb2, book_pb2_grpc

from sqlalchemy.orm import Session

from src.database import SessionLocal
from src.models import Book as BookModel


def convert_book_to_grpc(book_model):
    return book_pb2.Book(
        id=book_model.id,
        title=book_model.title,
        author=book_model.author,
        published_date=str(book_model.published_date)
    )


class BookService(book_pb2_grpc.BookServiceServicer):
    def __init__(self):
        self.db: Session = SessionLocal()

    def GetBookById(self, request, context):
        book = self.db.query(BookModel).filter(BookModel.id == request.id).first()
        if book:
            return book_pb2.BookResponse(book=convert_book_to_grpc(book))
        else:
            context.set_details('Book not found')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return book_pb2.BookResponse()

    def GetAllBooks(self, request, context):
        books = self.db.query(BookModel).all()
        books_response = [convert_book_to_grpc(book) for book in books]
        return book_pb2_grpc.BooksResponse(books=books_response)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
book_pb2_grpc.add_BookServiceServicer_to_server(BookService(), server)
server.add_insecure_port('[::]:50051')
print("gRPC server is running on port 50051")
server.start()
server.wait_for_termination()


