from server.api.zip.views import ZipFileView, ZipConfigView


ZIP_MODULE = [
    ('/config', ZipConfigView, "config"),
    ("/zipfile", ZipFileView, "zipfile")
]