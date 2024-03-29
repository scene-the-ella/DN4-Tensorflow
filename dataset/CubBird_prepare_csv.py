import os
import csv
import numpy as np
import random
from PIL import Image
import pdb

data_dir = '/FewShot/Datasets/CUB_birds'              # the path of the download dataset
save_dir = '/FewShot/Datasets/CUB_birds/For_FewShot'  # the saving path of the divided dataset

if not os.path.exists(os.path.join(save_dir, 'images')):
	os.makedirs(os.path.join(save_dir, 'images'))

images_dir = os.path.join(data_dir, 'images')
train_class_num = 130
val_class_num =  20
test_class_num = 50

# get all the dog classes
classes_list = [class_name for class_name in os.listdir(images_dir) if os.path.isdir(os.path.join(images_dir, class_name))]

# divide the train/val/test set
random.seed(200)
train_list = random.sample(classes_list, train_class_num)
remain_list = [rem for rem in classes_list if rem not in train_list]
val_list = random.sample(remain_list, val_class_num)
test_list = [rem for rem in remain_list if rem not in val_list]


def save_csv(list, printExam, filename):
    data = []

    for class_name in list:
        images = [[i, class_name] for i in os.listdir(os.path.join(images_dir, class_name))]
        data.extend(images)
        print(printExam % class_name)

        # read images and store these images
        img_paths = [os.path.join(images_dir, class_name, i) for i in os.listdir(os.path.join(images_dir, class_name))]
        for index, img_path in enumerate(img_paths):
            img = Image.open(img_path)
            img = img.convert('RGB')
            img.save(os.path.join(save_dir, 'images', images[index][0]), quality=100)

    with open(os.path.join(save_dir, filename), 'w') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['filename', 'label'])
        writer.writerows(data)

# save data into csv file----- Train
save_csv(train_list, 'Train----%s', 'train.csv')

# save data into csv file----- Val
save_csv(val_list, 'Val----%s', 'val.csv')

# save data into csv file----- Test
save_csv(test_list, 'Test----%s', 'test.csv')