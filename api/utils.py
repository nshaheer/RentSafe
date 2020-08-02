ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg", "gif"}


def get_file_type(filename):
    return filename.rsplit(".", 1)[1].lower()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
