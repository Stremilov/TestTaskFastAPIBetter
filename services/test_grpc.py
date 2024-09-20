# import services
# import book_pb2
# import book_pb2_grpc
#
#
# def run():
#     with services.insecure_channel('localhost:50051') as channel:
#         stub = book_pb2_grpc.BookServiceStub(channel)
#
#         response = stub.GetBookById(book_pb2.BookIdRequest(id=1))
#         print(f"Book: {response.book}")
#
#         all_books = stub.GetAllBooks(book_pb2.Empty())
#         for book in all_books.books:
#             print(f"Book: {book.title}, Author: {book.author}")
#
#
# if __name__ == "__main__":
#     run()
