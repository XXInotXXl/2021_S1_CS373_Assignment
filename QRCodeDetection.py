from matplotlib import pyplot
from matplotlib.patches import Rectangle

import imageIO.png
from service import service


def createInitializedGreyscalePixelArray(image_width, image_height, initValue=0):
    new_array = [[initValue for x in range(image_width)] for y in range(image_height)]
    return new_array


# this function reads an RGB color png file and returns width, height, as well as pixel arrays for r,g,b
def readRGBImageToSeparatePixelArrays(input_filename):
    image_reader = imageIO.png.Reader(filename=input_filename)
    # png reader gives us width and height, as well as RGB data in image_rows (a list of rows of RGB triplets)
    (image_width, image_height, rgb_image_rows, rgb_image_info) = image_reader.read()

    print("read image width={}, height={}".format(image_width, image_height))

    # our pixel arrays are lists of lists, where each inner list stores one row of greyscale pixels
    pixel_array_r = []
    pixel_array_g = []
    pixel_array_b = []

    for row in rgb_image_rows:
        pixel_row_r = []
        pixel_row_g = []
        pixel_row_b = []
        r = 0
        g = 0
        b = 0
        for elem in range(len(row)):
            # RGB triplets are stored consecutively in image_rows
            if elem % 3 == 0:
                r = row[elem]
            elif elem % 3 == 1:
                g = row[elem]
            else:
                b = row[elem]
                pixel_row_r.append(r)
                pixel_row_g.append(g)
                pixel_row_b.append(b)

        pixel_array_r.append(pixel_row_r)
        pixel_array_g.append(pixel_row_g)
        pixel_array_b.append(pixel_row_b)

    return (image_width, image_height, pixel_array_r, pixel_array_g, pixel_array_b)


# This method packs together three individual pixel arrays for r, g and b values into a single array that is fit for
# use in matplotlib's imshow method
def prepareRGBImageForImshowFromIndividualArrays(r, g, b, w, h):
    rgbImage = []
    for y in range(h):
        row = []
        for x in range(w):
            triple = []
            triple.append(r[y][x])
            triple.append(g[y][x])
            triple.append(b[y][x])
            row.append(triple)
        rgbImage.append(row)
    return rgbImage


# This method takes a greyscale pixel array and writes it into a png file
def writeGreyscalePixelArraytoPNG(output_filename, pixel_array, image_width, image_height):
    # now write the pixel array as a greyscale png
    file = open(output_filename, 'wb')  # binary mode is important
    writer = imageIO.png.Writer(image_width, image_height, greyscale=True)
    writer.write(file, pixel_array)
    file.close()


def main():
    filename = "./images/covid19QRCode/poster1small.png"

    # we read in the png file, and receive three pixel arrays for red, green and blue components, respectively
    # each pixel array contains 8 bit integer values between 0 and 255 encoding the color values
    (image_width, image_height, px_array_r, px_array_g, px_array_b) = readRGBImageToSeparatePixelArrays(filename)

    # Step 1
    origin_img = service.RGB_to_Grey(px_array_r, px_array_g, px_array_b, image_width, image_height)
    img = service.scale_and_quantize(origin_img, image_width, image_height)

    # Step 2,3,4
    img = service.computer_edges(img, image_width, image_height)

    # Step 5
    for i in range(8):
        img = service.mean_filter_3x3(img, image_width, image_height)
    img = service.scale_and_quantize(img, image_width, image_height)

    # Step 6
    # img = service.adaptive_thresholding(img, image_width, image_height)
    img = service.thresholding(img, image_width, image_height, 70)

    # Step 7
    img = service.Dilation(service.Erosion(img, image_width, image_height), image_width, image_height)
    img = service.scale_and_quantize(img, image_width, image_height)

    # Step 8
    x0, y0, x1, y1 = service.find_largest_connected_component(img, image_width, image_height)
    print(x0, y0, x1, y1)

    # Step 9
    # RGB
    px_array_r = service.border(px_array_r, image_width, image_height, x0, y0, x1, y1, 20, 0)
    px_array_g = service.border(px_array_g, image_width, image_height, x0, y0, x1, y1, 20, 255)
    px_array_b = service.border(px_array_b, image_width, image_height, x0, y0, x1, y1, 20, 0)
    # Gray
    img = service.border(origin_img, image_width, image_height, x0, y0, x1, y1, 20, 0)

    # Write grayscale image to det.png
    writeGreyscalePixelArraytoPNG("det.png", img, image_width, image_height)

    # Show RGB Image
    pyplot.imshow(
        prepareRGBImageForImshowFromIndividualArrays(px_array_r, px_array_g, px_array_b, image_width, image_height))
    # get access to the current pyplot figure
    axes = pyplot.gca()
    # create a 70x50 rectangle that starts at location 10,30, with a line width of 3
    rect = Rectangle((10, 30), 70, 50, linewidth=3, edgecolor='g', facecolor='none')
    # paint the rectangle over the current plot
    axes.add_patch(rect)

    # plot the current figure
    pyplot.show()


if __name__ == "__main__":
    main()
