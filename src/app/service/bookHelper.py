from app.service.bookAnalysiser import BookAnalysiser


class BookInfo(object):
    def __init__(self, filePath):
        self.filePath = filePath


class BookHelper(object):
    def __init__(self, inputDir):
        self.inputDir = inputDir

    def start(self):
        bookInfoItem = BookInfo(self.inputDir)
        cover_image = BookAnalysiser(bookInfoItem).analysis()
        return cover_image

