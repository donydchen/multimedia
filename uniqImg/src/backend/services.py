# -*- coding:utf-8 -*-
""" unique image backend

This module deal with some operation on images
including finding similar images, remove image files

"""

__all__ = ["find_simialr_imgs", "del_images"]

from PIL import Image
from imagehash import average_hash, phash, phash_simple, dhash, dhash_vertical
import os


def _get_filepaths(directory):
    file_paths = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)

    return file_paths


def find_simialr_imgs(userpath, hash_method, search_depth):
    import os
    def is_image(filename):
        f = filename.lower()
        return f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg") \
                or f.endswith(".bmp") or f.endswith(".gif")

    searchfunc = None
    if search_depth == "current":
        searchfunc = os.listdir
    elif search_depth == "recurrent":
        searchfunc = _get_filepaths
    else:
        searchfunc = os.listdir
    image_filenames = [os.path.join(userpath, path) for path in searchfunc(userpath)
                        if is_image(path)]

    hashfunc = None
    if hash_method == 'ahash':
        hashfunc = average_hash
    elif hash_method == "phash":
        hashfunc = phash
    elif hash_method == "phash-s":
        hashfunc = phash_simple
    elif hash_method == 'dhash-h':
        hashfunc = dhash
    elif hash_method == 'dhash-v':
        hashfunc = dhash_vertical

    images = {}
    for img in sorted(image_filenames):
        hash_value = hashfunc(Image.open(img))
        hash_value = str(hash_value)
        images[hash_value] = images.get(hash_value, []) + [img]

    return images


def del_images(imgs_list):
    info = "Successfully removed all the images."
    imgs_list_len = len(imgs_list)
    for idx in xrange(imgs_list_len):
        img = imgs_list.pop(0)
        try:
            os.remove(img)
        except OSError, e:
            info = "Fialed to delete file due to:\n %s"
            return False, info
    return True, info