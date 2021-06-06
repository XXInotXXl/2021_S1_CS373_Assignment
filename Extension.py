from matplotlib import pyplot
from matplotlib.patches import Rectangle

from QRCodeDetection import prepareRGBImageForImshowFromIndividualArrays, readRGBImageToSeparatePixelArrays
from service.RGBImage import RGBImage


def EXT(img_file_name, degree_to_shift):
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(img_file_name)
    img = RGBImage(px_array_r, px_array_g, px_array_b)
    img.hue(degree_to_shift)
    pyplot.imshow(prepareRGBImageForImshowFromIndividualArrays(img.r, img.g, img.b, image_width, image_height))
    axes = pyplot.gca()
    rect = Rectangle((10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none')
    axes.add_patch(rect)
    pyplot.show()


filename = "./images/angel.png"  # chose your image
degree_to_shift = 210  # Type in your degree!

if __name__ == "__main__":
    EXT(filename, degree_to_shift)
