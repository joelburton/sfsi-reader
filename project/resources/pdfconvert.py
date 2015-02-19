"""
Utility for PDF conversion
"""

from cStringIO import StringIO
import subprocess
import tempfile

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def py_convert_pdf_to_txt(fp):
    """Convert PDF file to text.

    :param fp: File pointer
    :returns: Unicode string of first 10 pages of PDF

    We only convert the first 10 pages for performance and storage reasons; presumably, almost all
    search terms we might find in a document should appear in the first 10 pages, anyway.
    """

    # Ugh, PDFminer is slow. Use this only if we need to!

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


def convert_pdf_to_txt(fp):
    """Convert PDF file to text.

    :param fp: File pointer
    :returns: Unicode string of first 30 pages of PDF

    We only convert the first 30 pages for performance and storage reasons; presumably, almost all
    search terms we might find in a document should appear in the first pages, anyway.
    """

    temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    fp.seek(0)
    temp_file.write(fp.read())
    name = temp_file.name
    temp_file.close()
    ret = subprocess.check_output(['pdftotext', '-l', '30', name, '-'])
    return ret