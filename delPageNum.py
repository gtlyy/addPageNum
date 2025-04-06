# 功能：抹去pdf文件的页码：用白色覆盖而已。
import sys
from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
import io

def add_page_numbers(input_pdf, output_pdf, pos_x, pos_y, size_font, skip_pages):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    
    num_all = len(reader.pages)
    for page_number in range(num_all):
        packet = io.BytesIO()
        can = canvas.Canvas(packet)
        
        # 获取当前页面的宽度和高度
        page = reader.pages[page_number]
        width = float(page.mediabox[2])  # 页面宽度
        height = float(page.mediabox[3])  # 页面高度
        
        # 设置页码位置为右上角，使用百分比
        x = width * pos_x  # 95% 的宽度
        y = height * pos_y  # 95% 的高度

        # 设置字体和大小
        can.setFont("Helvetica", size_font)

        if page_number >= int(skip_pages):
        # 绘制无边框的白色矩形覆盖原页码
            can.setFillColorRGB(1, 1, 1)  # 设置颜色为白色
            can.setStrokeColorRGB(1, 1, 1)  # 设置边框颜色为白色（无边框）
            can.rect(x - size_font*0.5, y - size_font*0.5, size_font*5, size_font*1.5, fill=1, stroke=0)  # 覆盖区域
        
        # x - 30:
        #     矩形左下角的 x 坐标。这里通过 x - 30 将矩形向左移动 30 单位，以使其覆盖页码。
        # y - 10:
        #     矩形左下角的 y 坐标。通过 y - 10 将矩形向下移动 10 单位，使其更好地覆盖页码。
        # 80:
        #     矩形的宽度。这里设置为 60 单位，确保覆盖住页码的区域。
        # 20:
        #     矩形的高度。设置为 20 单位，足以覆盖页码的高度。
        # fill=1:
        #     表示矩形将被填充。值为 1 表示填充颜色为之前设置的白色（can.setFillColorRGB(1, 1, 1)）。
        # stroke=0:
        #     表示不绘制边框。值为 0 意味着矩形没有边框（即无边框）。          
        
        # if page_number >= int(skip_pages):
        #     # 绘制页码
        #     can.setFillColorRGB(0, 0, 0)  # 设置颜色
        #     # can.drawString(x, y, str(page_number + 1))  # 页码位置
        #     can.drawString(x, y, str(page_number + 1 - int(skip_pages))+"/"+str(num_all - int(skip_pages)))  # 页码位置
        
        can.save()
        
        packet.seek(0)
        overlay = PdfReader(packet)
        page.merge_page(overlay.pages[0])
        writer.add_page(page)

    with open(output_pdf, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python add_page_numbers.py <input_pdf> <output_pdf> <skip_pages>")
        sys.exit(1)

    # 右下角
    size_font = 7
    pos_x = 0.925   # 0 -> 1  左 -> 右
    pos_y = 0.025    # 0 -> 1  下 -> 上

    input_pdf = sys.argv[1]
    output_pdf = sys.argv[2]
    skip_pages = sys.argv[3]
    
    add_page_numbers(input_pdf, output_pdf, pos_x, pos_y, size_font, skip_pages)
