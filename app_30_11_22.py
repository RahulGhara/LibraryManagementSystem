from DbConnection_30_11_22 import app
from View.LibraryBooksApi_30_11_22 import StoreBooksApi
from View.BookAllocationApi import BookAllocationApi
from View.StudentTableApi import StudentTableApi
from JWT.LoginApi_16_12_22 import Login
from View.AdminApi_4_1_23 import AdminApi
from View.Forgot_pass_6_1_23 import Password

'''Book store routes'''
app.add_url_rule("/add_book", "StoreBooksApi.AddBook", view_func=StoreBooksApi.AddBook, methods=['POST'])
app.add_url_rule("/view_book/<book_id>", "StoreBooksApi.ViewBook", view_func=StoreBooksApi.ViewBook, methods=['GET'])
app.add_url_rule("/view_all", "StoreBooksApi.ViewAll", view_func=StoreBooksApi.ViewAll, methods=['GET'])
app.add_url_rule("/delete/<book_id>", "StoreBookApi.DeleteBook", view_func=StoreBooksApi.DeleteBook,
                 methods=['DELETE'])
app.add_url_rule("/update_record/<book_id>", "StoreBookApi.UpdateBook", view_func=StoreBooksApi.UpdateBook,
                 methods=['PUT'])

'''Book allocation routes for admin'''
app.add_url_rule("/admin/allocation/<roll_no>", "BookAllocationApi.AllocateBook",
                 view_func=BookAllocationApi.AllocateBook,
                 methods=['POST'])
app.add_url_rule('/admin/allocation_status_update/<roll_no>', "BookAllocationApi.StatusUpdate",
                 view_func=BookAllocationApi.StatusUpdate,
                 methods=['PUT'])

'''Student's data routes for admin'''
app.add_url_rule('/admin/student_entry', "StudentTableApi.AddStudent", view_func=StudentTableApi.AddStudent,
                 methods=['POST'])
app.add_url_rule('/admin/student_data/<roll_no>', 'StudentTableApi.ViewStudentData',
                 view_func=StudentTableApi.ViewStudentData,
                 methods=['GET'])
app.add_url_rule('/admin/student_semester_change/<roll_no>', "StudentTableApi.UpdateStudentData",
                 view_func=StudentTableApi.UpdateStudentData,
                 methods=['PUT'])

'''Viewing book allocation details for students'''
app.add_url_rule('/student/view_data/<roll_no>', 'BookAllocationApi.ViewDetails',
                 view_func=BookAllocationApi.ViewDetails,
                 methods=['GET'])

''' login'''

app.add_url_rule('/login', 'Login', view_func=Login, methods=['GET'])

'''admin'''

app.add_url_rule('/admin/add_admin', 'AdminApi.add_admin', view_func=AdminApi.add_admin, methods=['POST'])
app.add_url_rule('/admin/delete_admin/<prof_id>', 'AdminApi.delete_admin', view_func=AdminApi.delete_admin, methods=['DELETE'])

'''password reset'''
app.add_url_rule('/forgot_pass', 'Password.Forgot_password', view_func= Password.Forgot_password, methods=['GET'])
app.add_url_rule('/change_pass/<user_id>', 'Password.Change_password', view_func=Password.Change_password, methods=['PUT'])
if __name__ == "__main__":
    app.run(debug=True, port=600)
