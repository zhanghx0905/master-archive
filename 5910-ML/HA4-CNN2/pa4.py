import pprint
import numpy as np
import tensorflow
from tensorflow.keras.preprocessing import image


def load_img(target_size=(224, 224)):
    imgs = []
    for i in range(1, 11):
        img_path = f"./{i}.png"
        img = image.load_img(img_path, target_size=target_size)
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        imgs.append(x)
    imgs = np.concatenate(imgs)
    return imgs

pp = pprint.PrettyPrinter(indent=4)


def test_img(x, model, preprocess_input, decode_predictions, model_name=""):
    preds = model.predict(preprocess_input(x))
    print(f"{model_name} Predicted:")
    pp.pprint(decode_predictions(preds, top=3))


from tensorflow.keras.applications.resnet50 import (
    ResNet50,
    preprocess_input,
    decode_predictions,
)

model = ResNet50()
test_img(load_img(), model, preprocess_input, decode_predictions, "resnet50")

from keras.applications.vgg16 import (
    VGG16,
    preprocess_input,
    decode_predictions,
)

model = VGG16()
test_img(load_img(), model, preprocess_input, decode_predictions, "vgg16")

from keras.applications.inception_v3 import (
    InceptionV3,
    preprocess_input,
    decode_predictions,
)

model = InceptionV3()
test_img(
    load_img((299, 299)), model, preprocess_input, decode_predictions, "inceptionv3"
)

from keras.applications.densenet import (
    DenseNet121,
    preprocess_input,
    decode_predictions,
)

model = DenseNet121()
test_img(load_img(), model, preprocess_input, decode_predictions, "densenet121")


from keras.applications.efficientnet import (
    EfficientNetB2,
    preprocess_input,
    decode_predictions,
)

model = EfficientNetB2()
test_img(
    load_img((260, 260)), model, preprocess_input, decode_predictions, "EfficientNetB2"
)


from keras.applications.mobilenet_v2 import (
    MobileNetV2,
    preprocess_input,
    decode_predictions,
)

model = MobileNetV2()
test_img(load_img(), model, preprocess_input, decode_predictions, "MobileNetV2")
