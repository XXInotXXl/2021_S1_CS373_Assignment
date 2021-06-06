# Extension

### *class* `RGBImage`

Under file `service/RGBImage.py`. The class simply has 
one method `hue()` where you can type degree between 0 and 360,
it will transform the hue (colour) of the image.

You can expirence this functionality in `Extension.py`. You can customize the following variable:

- `filename` where your image file is located

- `degree_to_shift` a value between 0 and 360, means how many degrees you want the colour to change. Exceeding the range will cause exception.