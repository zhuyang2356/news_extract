from paddleocr import PaddleOCR, draw_ocr
def extract_pic(img):
    # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
    # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
    ocr = PaddleOCR(use_angle_cls=True, lang="ch") # need to run only once to download and load model into memory
#     img_path = './toutiao/今日头条/图片+新闻内容/2024年全国保密宣传教育月宣传海报/1.jpg'
    pic_text_list=[]
    result = ocr.ocr(img, cls=True)
    for i in range(len(result[0])):
        pic_text=result[0][i][-1][0]
#         print(pic_text)
        if len(pic_text)>=5:
            pic_text_list.append(pic_text)
    return pic_text_list