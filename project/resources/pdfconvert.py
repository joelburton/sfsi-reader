"""
Utility for PDF conversion
"""

from cStringIO import StringIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert_pdf_to_txt(fp):
    """Convert PDF file to text.

    :param fp: File pointer
    :returns: Unicode string of first 10 pages of PDF

    We only convert the first 10 pages for performance and storage reasons; presumably, almost all
    search terms we might find in a document should appear in the first 10 pages, anyway.
    """

    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 10
    caching = True
    pagenos = set()
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,
                                  caching=caching, check_extractable=True):
        interpreter.process_page(page)
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str