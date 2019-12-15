from PIL import Image
import os, shutil

error_folder = "../Dataset/Errors"


def file_is_image(image_path):
    try:
        test = Image.open(image_path)
        return True
    except:
        return False


def valid_folder(path, image_format):
    for item in os.listdir(path):
        image_path = os.path.join(path, item)
        print("Testing " + image_path)
        try:
            if not file_is_image(image_path):
                raise Exception("File not image")
            test = Image.open(image_path)
            if image_format is not None and image_format != test.format:
                test.close()
                raise Exception("Wrong format")
            image_format = test.format

        except Exception as e:
            print("Error on " + image_path)
            shutil.copy2(image_path, error_folder)
            os.remove(image_path)
            with open("mop_logger.txt", "a+") as f:
                f.write("Error in file {}: {}; was moved to {}\n".format(image_path, str(e), error_folder))
            valid_folder(path, image_format)


def valid_input_folder(path):
    image_format = None
    images_path = os.path.join(path, 'Positive')
    valid_folder(images_path, image_format)
    images_path = os.path.join(path, 'Negative')
    valid_folder(images_path, image_format)


def valid_image(file_path):
    if not file_is_image(file_path):
        with open("mop_logger.txt", "a+") as f:
            f.write("Error in file {}: Not an image\n".format(file_path))
        return False
    return True


# valid_input_folder("../Dataset/Train")
