from django.core.files.storage import FileSystemStorage

def handle_uploaded_file(f):
    print('handle_uploaded_file')
    fs = FileSystemStorage()
    fs.save(f.name, f)
        