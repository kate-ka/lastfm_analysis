# -*- coding: utf-8 -*-
# from __future__ import print_function
# import os
#
# from PIL import Image
#
# files = [
#   '/home/kate/code/lastfm_analysis/media/album_images/0aeada36c70943c999fd1b8434000fbd.png',
#     '/home/kate/code/lastfm_analysis/media/album_images/0aeada36c70943c999fd1b8434000fbd_6a4rwXr.png',
#     '/home/kate/code/lastfm_analysis/media/album_images/9f9a1f01241c4294808c169d810cd3c4_Olc13c9.png',
#       '/home/kate/code/lastfm_analysis/media/album_images/9feb80b2d0f249349512d3376b3e5112_zW5C4A0.png']
#
# result = Image.new("RGB", (348, 348))
#
# for index, file in enumerate(files):
#   # path = os.path.expanduser(file)
#   img = Image.open(file)
#   img.thumbnail((174, 174), Image.ANTIALIAS)
#   x = index // 4 * 174
#   y = index % 4 * 174
#   w, h = img.size
#   print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
#   result.paste(img, (x, y, x + w, y + h))
#
# result.save(os.path.expanduser('~/Завантаження/pics/image.jpg'))
y = 0
x = 0
coords = []
for i in range(1,13):
    coords.append((x, y))
    y += 174
    if not i % 4:
        y = 0
        x +=174
print coords

