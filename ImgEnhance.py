from PIL import Image
from PIL import ImageEnhance

image = Image.open('ggg.jpg')

image.show()


# # Enhance Brightness
# curr_bri = ImageEnhance.Brightness(image)
# new_bri = 1.5
#
# # Brightness enhanced by a factor of 2.5
# img_brightened = curr_bri.enhance(new_bri)
#
# # shows updated image in image viewer
# img_brightened.show()

# # Enhance Color Level
# curr_col = ImageEnhance.Color(image)
# new_col = 2.5
#
# # Color level enhanced by a factor of 2.5
# img_colored = curr_col.enhance(new_col)
#
# # shows updated image in image viewer
# img_colored.show()

# # Enhance Contrast
# curr_con = ImageEnhance.Contrast(image)
# new_con = 0.3
#
# # Contrast enhanced by a factor of 0.3
# img_contrasted = curr_con.enhance(new_con)
#
# # shows updated image in image viewer
# img_contrasted.show()

# # Enhance Sharpness
# curr_sharp = ImageEnhance.Sharpness(image)
# new_sharp = 8.3
#
# # Sharpness enhanced by a factor of 8.3
# img_sharped = curr_sharp.enhance(new_sharp)
#
# # shows updated image in image viewer
# img_sharped.show()