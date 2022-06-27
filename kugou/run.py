# from scrapy import cmdline
#
# cmdline.execute('scrapy crawl kugou_spider'.split())
import os
a = '风吹过八千里8f6438be22711ebb1c89f318de55417649346bc0.mp3'
name,ext = os.path.splitext(a)
# print(name[:-40],ext)
song_name = name[:-40] + ext
print(song_name)