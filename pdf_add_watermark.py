#!/usr/bin/python3

from PyPDF2 import PdfFileReader, PdfFileWriter
from matplotlib import pyplot as plt
from matplotlib import rcParams
from sys import argv
from pathlib import Path
import textwrap


# support yahei
rcParams['pdf.fonttype'] = 42
rcParams['font.family'] = 'Microsoft Yahei'
rcParams['font.size'] = 80


# def generate_watermark(text: str) -> Path:
# from reportlab.pdfbase import pdfmetrics, ttfonts
# from reportlab.platypus import Paragraph
# from reportlab.pdfgen import canvas
# from reportlab.lib.styles import ParagraphStyle
# from reportlab.lib.colors import Color
# from reportlab.graphics.charts.textlabels import Label
# from reportlab.graphics.shapes import Drawing, String
#     wm_file = Path('rl_watermark.pdf').absolute()
#     # register YaHei font
#     pdfmetrics.registerFont(ttfonts.TTFont('yahei', 'msyh.ttc'))
#     transparent_blue = Color(0, 115, 255, alpha=0.2)
#     # may overwrite
#     # set style
#     style = ParagraphStyle('normal',
#                            fontName='yahei', fontSize=70, leading=70*1.5,
#                            textColor=transparent_blue,)
#                            # wordWrap='LTR')
#
#     p = Paragraph(text, style)
#     c = canvas.Canvas(str(wm_file))
#     c.setFont('yahei', 70)
#     c.setFillColor(transparent_blue)
#     w, h = c._pagesize
#     width, height = 10, 10
#     degree = 45
#     # c.rotate(degree)
#     ww, wh = p.wrapOn(c, w, h)
#     # p.drawOn(c, ww, wh)
#     p.drawOn(c, 0, h/2-(wh/2))
#     c.save()
#     return wm_file


def generate_watermark(text: str) -> Path:
    wm_file = Path('rl_watermark.pdf').absolute()
    # a4
    fig = plt.figure(1, figsize=(8.27, 11.69), dpi=72)
    wrap_text = textwrap.fill(text, width=10)
    fig.text(0.05, 0.05, wrap_text, rotation=45, alpha=0.2, color=(0, 0.5, 1),
             rasterized=True)
    plt.savefig(wm_file, transparent=True)
    return wm_file


def main():
    print('Usage: python3 pdf_add_watermark.py original.pdf watermark.pdf')
    print('Or:')
    print('Usage: python3 pdf_add_watermark.py original.pdf watermark_text')
    original = Path(argv[1])
    output = original.absolute().parent / ('new-'+original.name)
    watermark = Path(argv[2])
    if watermark.exists():
        pass
    else:
        watermark = generate_watermark(argv[2])

    wm_obj = PdfFileReader(str(watermark))
    wm_page = wm_obj.getPage(0)

    reader = PdfFileReader(str(original))
    writer = PdfFileWriter()

    for index in range(reader.getNumPages()):
        page = reader.getPage(index)
        page.mergePage(wm_page)
        writer.addPage(page)

    with open(output, 'wb') as out:
        writer.write(out)
    print('Done.')

if __name__ == '__main__':
    main()