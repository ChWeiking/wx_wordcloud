import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image
import itchat
import jieba
import re
import sys
import time
#itchat控件函数，登录后调用
def lc():
    print('\n>>>:成功登陆')
#itchat控件函数，退出后调用
def ec():
    print('\n>>>:成功退出')
#实现微信的登录，生成一个二维码，扫码之后手机端确认登录
#itchat.login()
#一定时间内重新开启可以不用重新扫码,生成一个itchat.pkl文件
itchat.auto_login(hotReload=True,loginCallback=lc, exitCallback=ec)
#列表里第一位是自己，所以从"自己"之后开始计算
friends = itchat.get_friends(update=True)[1:]
tList = []
for i in friends:
    #i["Signature"]有大量的span，class，emoji，emoji1f3c3等的字段
    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    #测试查看下签名情况
    #print(i["Signature"].translate(non_bmp_map))
    #正则过滤掉特殊字符
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)
# 拼接字符串
text = "".join(tList)
# jieba分词全模式
wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)
#获取当前py文件的绝对路径
d = os.path.dirname(__file__)
#获得图片的(宽度、高度、通道)参数
alice_coloring = np.array(Image.open(os.path.join(d, "wechat.jpg")))
#制作词云
my_wordcloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring,
                         max_font_size=40, random_state=42,
                         #引用系统自带的字体（华文行楷）
                         font_path='C:/Windows/Fonts/STXINGKA.TTF')\
    .generate(wl_space_split)
image_colors = ImageColorGenerator(alice_coloring)
plt.imshow(my_wordcloud.recolor(color_func=image_colors))
#plt.imshow(my_wordcloud)
#不带坐标
plt.axis("off")
#展示绘图
plt.show()
# 保存图片到当前路径
my_wordcloud.to_file(os.path.join(d, "wechat_cloud.png"))
# 并发送到手机，filehelper就是微信上的文件传输助手
itchat.send_image("wechat_cloud.png", 'filehelper')
time.sleep(3)
itchat.logout()
print("60秒后关机，请按ctrl+c退出！")
for i in np.linspace(1,60,60):
    time.sleep(1)
    print(">>>:{}".format(i))
else:
    os.system('shutdown -s -t 1')
   

