#! /usr/bin/env python3

from PIL import Image as IMAGE
from PIL import ImageEnhance as ENHANCE
from PIL import ImageFilter as FILTER
from PIL import ImageOps as OPERATION

test = IMAGE.open("./test.jpg")
test_sharp = ENHANCE.Sharpness(test).enhance(4.0)
test_sharp.save("./test-sharp.jpg")
test_contrast = ENHANCE.Contrast(test).enhance(2.0)
test_contrast.save("./test-contrast.jpg")
test_brightness = ENHANCE.Brightness(test).enhance(2.0)
test_brightness.save("./test-brightness.jpg")
test_cut_first = OPERATION.autocontrast(test, (10, 0))
test_cut_first.save("./test-cut-first.jpg")
test_cut_second = OPERATION.autocontrast(test, (0, 10))
test_cut_second.save("./test-cut-second.jpg")
test_cut_both = OPERATION.autocontrast(test, (10, 10))
test_cut_both.save("./test-cut-both.jpg")
