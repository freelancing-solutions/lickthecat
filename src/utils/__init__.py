from os import path
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from dateutil.relativedelta import relativedelta

def static_folder() -> str:
    return path.join(path.dirname(path.abspath(__file__)), '../../static')


def documents_folder() -> str:
    return path.join(path.dirname(path.abspath(__file__)), '../../documents')


def template_folder() -> str:
    return path.join(path.dirname(path.abspath(__file__)), '../../templates')


