# https://colab.research.google.com/github/tensorflow/examples/blob/master/courses/udacity_intro_to_tensorflow_for_deep_learning/l07c01_saving_and_loading_models.ipynb#scrollTo=W_Zvg2i0fzJu

import tensorflow as tf
import tensorflow_datasets as tfds
import tensorflow_hub as hub

tfds.disable_progress_bar()

(train_examples, validation_examples),  info = tfds.load(
                        'cats_vs_dogs',
                        split=['train[:80%]', 'train[80%:]'],
                        with_info=True,
                        as_supervised=True,
)

def format_image(image, label):
    image = tf.image.resize(image, (IMAGE_RES, IMAGE_RES))/255.0
    return image, label

num_examples = info.splits['train'].num_examples

BATCH_SIZE = 32
IMAGE_RES = 224

train_batches = train_examples.cache().shuffle(num_examples//4).map(format_image).batch(BATCH_SIZE).prefetch(1)
validation_batches = validation_examples.cache().map(format_image).batch(BATCH_SIZE).prefetch(1)

URL = "https://tfhub.dev/google/tf2-preview/mobilenet_v2/feature_vector/4"
feature_extractor = hub.KerasLayer(URL, input_shape=(IMAGE_RES, IMAGE_RES, 3))

feature_extractor.trainable = False

# ==============================
# model = tf.keras.Sequential([
#             feature_extractor,
#             layers.Dense(2)
#         ])
#
# model.summary()
#
# model.compile(
#                 optimizer='adam',
#                 loss=tf.losses.SparseCategoricalCrossentropy(from_logits=True),
#                 metrics=['accuracy'])
#
# EPOCHS = 3
# history = model.fit(train_batches, epochs=EPOCHS, validation_data=validation_batches)
#
# class_names = np.array(info.features['label'].names)
#
# image_batch, label_batch = next(iter(train_batches.take(1)))
# image_batch = image_batch.numpy()
# label_batch = label_batch.numpy()
#
# predicted_batch = model.predict(image_batch)
# predicted_batch = tf.squeeze(predicted_batch).numpy()
# predicted_ids = np.argmax(predicted_batch, axis=1)
# predicted_class_names = class_names[predicted_ids]
#
# print("Labels: ", label_batch)
# print("Predicted lables: ", predicted_ids)
#
# plt.figure(figsize=(10, 9))
# for n in range(30):
#     plt.subplot(6, 5, n+1)
#     plt.imshow(image_batch[n])
#     color = "blue" if predicted_ids[n] == label_batch[n] else "red"
#     plt.title(predicted_class_names[n].title(), color=color)
#     plt.axis('off')
# _ = plt.suptitle("Model predictions (blue: correct, red: incorrect)")
#
# plt.show()
#
# t = time.time()
#
# export_path_keras = '{}.h5'.format(int(t))
# print(export_path_keras)
# model.save(export_path_keras)
#
# export_path_sm = '{}'.format(int(t))
# print(export_path_sm)
# tf.saved_model.save(model, export_path_sm)

# ===================
reloaded = tf.keras.models.load_model(
    '1607998479.h5',
    custom_objects={'KerasLayer': hub.KerasLayer})
reloaded.summary()

EPOCHS = 3

history = reloaded.fit(train_batches, epochs=EPOCHS,
                       validation_data=validation_batches)


