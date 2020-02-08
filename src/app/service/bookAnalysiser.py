import os
from xml.dom.minidom import parse
import xml.dom.minidom
from flask import current_app


class BookAnalysiser(object):
    def __init__(self, book):
        self.book = book
        self.tempPath = None
        self.tocDir = None
        self.saved = []

    def analysis(self):
        self.tempPath = self.book.filePath

        # 找到 toc.ncx 文件
        self._analysisTOC()

        # 解析cover
        cover_image = self._analysisCover()
        return cover_image

    def _analysisTOC(self):
        tocPath = self._getTOC()
        self.tocDir = os.path.dirname(tocPath)

    def _analysisCover(self):

        ### 先在找 META-INF/container.xml 中找到  rootfile节点指向的 根文件 一般是  ???/content.opf
        container_DOMTree = xml.dom.minidom.parse(current_app.config['APP_PATH'] + self.tempPath + 'META-INF/container.xml')
        rootNode = container_DOMTree.documentElement.getElementsByTagName('rootfile')

        # container引用opf 是 当前压缩文件夹下的绝对路径
        opfPath = rootNode[0].getAttribute('full-path')

        ### opf 文件里面直接找 manifest节点下 id = ncx 的子节点，href 即为 ncx的 目录
        opf_DOMTree = xml.dom.minidom.parse(current_app.config['APP_PATH'] + self.tempPath + '/' + opfPath)
        metaNodes = opf_DOMTree.documentElement.getElementsByTagName('meta')

        manifestNodes = opf_DOMTree.documentElement.getElementsByTagName('manifest')
        itemNodes = manifestNodes[0].getElementsByTagName('item')

        p = ''
        for node in metaNodes:
            if (node.getAttribute('name') == 'cover'):
                coverId = node.getAttribute('content')

                for manifestNode in itemNodes:
                    if manifestNode.getAttribute('id') == coverId:
                        coverSrc = manifestNode.getAttribute('href')
                        p = self.tocDir + '/' + coverSrc
                        self.saved.append(p)
        if not self.saved:
            for manifestNode in itemNodes:
                if manifestNode.getAttribute('id') in ['cover', 'Cover']:
                    coverSrc = manifestNode.getAttribute('href')
                    p = self.tocDir + '/' + coverSrc
                    self.saved.append(p)
        return self.saved

    def _getTOC(self):
        # 找到 toc.ncx
        ### 先在找 META-INF/container.xml 中找到  rootfile节点指向的 根文件 一般是  ???/content.opf
        container_DOMTree = xml.dom.minidom.parse(current_app.config['APP_PATH'] + self.tempPath + 'META-INF/container.xml')
        rootNode = container_DOMTree.documentElement.getElementsByTagName('rootfile')

        # container引用opf 是 当前压缩文件夹下的绝对路径
        opfPath = rootNode[0].getAttribute('full-path')

        ### opf 文件里面直接找 manifest节点下 id = ncx 的子节点，href 即为 ncx的 目录
        opf_DOMTree = xml.dom.minidom.parse(current_app.config['APP_PATH'] + self.tempPath + '/' + opfPath)
        manifestNode = opf_DOMTree.documentElement.getElementsByTagName('manifest')
        itemNodes = manifestNode[0].getElementsByTagName('item')
        ncxPath = ''

        # opf 引用ncx 是相对路径
        absPath = os.path.dirname(self.tempPath + opfPath)

        for item in itemNodes:
            if item.getAttribute('id') == 'ncx':
                ncxPath = item.getAttribute('href')
                break
        p = absPath + '/' + ncxPath
        return p
