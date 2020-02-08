import time, os
import zipfile
from lxml import etree
from plugin.exceptions import ApiError
from flask import current_app
from datetime import datetime
from werkzeug import secure_filename
from app.service.utils import allowed_file, pdf_to_image
from app.models import Book, ProjectBook
from app.service import bookHelper


def upload_book(file_):
    allow_extensions = ['epub', 'pdf']
    sub_folder = datetime.today().strftime('%Y%m%d')
    book_path = current_app.config['BOOK_PATH']
    upload_folder = os.path.join(book_path, sub_folder)
    if not os.path.isdir(upload_folder):
        os.mkdir(upload_folder)
    if file_ and allowed_file(file_.filename, allow_extensions):
        original = secure_filename(file_.filename)
        if original in allow_extensions:
            original = '.' + original
        filename = str(time.time()) + original
        book_res = os.path.join(sub_folder, filename)
        url = os.path.join('/resource/uploads/books/', book_res)
        file_.save(os.path.join(book_path, book_res))
        res = {
            "status": True,
            "url": url,
        }
        # 提取期刊或报纸(pdf)中的一页，生成预览图
        if original.split('.')[-1] == 'pdf':
            try:
                image_path = current_app.config['IMAGE_PATH']
                pdf_path = os.path.join(book_path, book_res)
                upload_image_folder = os.path.join(image_path, sub_folder)
                if not os.path.isdir(upload_image_folder):
                    os.mkdir(upload_image_folder)
                image_res = os.path.join(sub_folder, filename.replace(book_res.split('.')[-1], 'jpg'))
                img_output_path = os.path.join(image_path, image_res)
                pdf_to_image(pdf_path, img_output_path)
                res['pdf_image'] = os.path.join('/resource/uploads/images/', image_res)
            except Exception as e:
                current_app.logger.error('预览图生成失败', e)
                res['pdf_image'] = ''
        return res
    return {'status': False}

def parse_epub_info(file_):
    try:
        ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        _zip = zipfile.ZipFile(file_)
        txt = _zip.read('META-INF/container.xml')
        tree = etree.fromstring(txt)
        cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]
        cf = _zip.read(cfname)
        tree = etree.fromstring(cf)
        p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]
        metadata = {}
        for s in ['title', 'creator', 'date', 'publisher']:
            res = p.xpath('dc:%s/text()' % s, namespaces=ns)
            if res:
                metadata[s] = res[0]
            else:
                metadata[s] = None
    except:
        raise ApiError('图书格式错误')
    return metadata

def generate_opf_from_epub(file_, url):
    try:
        ns = {
            'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
            'pkg': 'http://www.idpf.org/2007/opf',
            'dc': 'http://purl.org/dc/elements/1.1/'
        }
        _zip = zipfile.ZipFile(file_)
        txt = _zip.read('META-INF/container.xml')
        tree = etree.fromstring(txt)
        cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]
        path = current_app.config['APP_PATH'] + url
        if not os.path.isdir(path + "_files"):
            os.mkdir(path + "_files")
        for names in _zip.namelist():
            _zip.extract(names, path + "_files/")
        _zip.close()
    except Exception as e:
        current_app.logger.error(e)
        raise ApiError('opf_path解析失败')
    return cfname

def get_size(url):
    size = os.path.getsize(current_app.config['APP_PATH']+url)
    return size


def get_book_query(book_type, project_id):
    if not project_id:
        query = Book.query.filter_by(book_type=book_type)
    else:
        query = Book.query. \
            join(ProjectBook, Book.id == ProjectBook.book_id). \
            filter(Book.book_type == book_type). \
            filter(ProjectBook.project_id == project_id)
    return query


def cover_path_from_epub(file_path):
    helper = bookHelper.BookHelper(inputDir=(file_path + "_files/"))
    cover_path = helper.start()
    return cover_path


def get_opf_path():
    from app import db
    books = Book.query.with_entities(Book.id, Book.file_path).filter(Book.opf_path == '').all()
    books_path = [b._asdict() for b in books]
    for book in books_path:
        try:
            book_id = book.get('id')
            path = book.get('file_path')
            book_path = os.path.join(current_app.config['APP_PATH'] + path.split('/', 1)[1][4:])
            metadata = parse_epub_info(book_path, path)
            opf_path = os.path.join((path + "_files/"), metadata['opf_path'])
            Book.query.filter(Book.id==book_id).update({'opf_path': opf_path})
            db.session.commit()
            current_app.logger.info('SUCCESS book_id:{}'.format(book_id))
        except Exception as e:
            book_id = book.get('id')
            current_app.logger.error('FAILED book_id:{}'.format(book_id))
            continue