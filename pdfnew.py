

# ###################################
# Help
def drawMyRuler(pdf):
    pdf.drawString(100,810, 'x100')
    pdf.drawString(200,810, 'x200')
    pdf.drawString(300,810, 'x300')
    pdf.drawString(400,810, 'x400')
    pdf.drawString(500,810, 'x500')

    pdf.drawString(10,100, 'y100')
    pdf.drawString(10,200, 'y200')
    pdf.drawString(10,300, 'y300')
    pdf.drawString(10,400, 'y400')
    pdf.drawString(10,500, 'y500')
    pdf.drawString(10,600, 'y600')
    pdf.drawString(10,700, 'y700')
    pdf.drawString(10,800, 'y800')    








# ###################################
# Content
fileName = 'MyDoc1.pdf'
documentTitle = 'Document title!'
title = 'Tasmanian devil'
subTitle = 'The largest carnivorous marsupial'

textLines = [
'The Tasmanian devil (Sarcophilus harrisii) is',
'a carnivorous marsupial of the family',
'Dasyuridae.'
]

image = 'media/images/Screenshot_2021-11-01_at_13.36.09_FJ6U12a.png'
image1 = '23-03-2022 kaata bill-9.jpg'

# ###################################
# 0) Create document 
from reportlab.pdfgen import canvas 

pdf = canvas.Canvas(fileName)
pdf.setTitle(documentTitle)



drawMyRuler(pdf)
# ###################################
# 1) Title :: Set fonts 
# # Print available fonts
# for font in pdf.getAvailableFonts():
#     print(font)

# Register a new font
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

pdfmetrics.registerFont(
    TTFont('abc', 'SakBunderan.ttf')
)
pdf.setFont('abc', 36)
pdf.drawCentredString(300, 770, title)

# ###################################
# 2) Sub Title 
# RGB - Red Green and Blue
pdf.setFillColorRGB(0, 0, 255)
pdf.setFont("Courier-Bold", 24)
pdf.drawCentredString(290,720, subTitle)


# ###################################
# 3) Draw a line
pdf.line(30, 710, 550, 710)


# ###################################
# 4) Text object :: for large amounts of text
from reportlab.lib import colors

text = pdf.beginText(40, 680)
text.setFont("Courier", 18)
text.setFillColor(colors.red)
for line in textLines:
    text.textLine(line)

pdf.drawText(text)


# ###################################
# 5) Draw a image
pdf.drawInlineImage(image, 130, 400)

pdf.drawInlineImage(image1,20,0)


pdf.save()