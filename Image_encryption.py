from PIL import Image
import numpy as np
import pickle

from phe import paillier


def ImgEncrypt(public_key: paillier.PublicKey, plainimg: Image.Image) -> np.ndarray:

    cipherimg = np.asarray(plainimg)
    shape = cipherimg.shape
    cipherimg = cipherimg.flatten().tolist()
    cipherimg = [public_key.encrypt(pix) for pix in cipherimg]

    return np.asarray(cipherimg).reshape(shape)


def ImgDecrypt(public_key: paillier.PublicKey, private_key: paillier.PrivateKey, cipherimg: np.ndarray) -> Image.Image:

    shape = cipherimg.shape
    plainimg = cipherimg.flatten().tolist()
    plainimg = [public_key.decrypt(private_key, pix) for pix in plainimg]
    plainimg = [pix if 0 <= pix < 255 else (255 if pix > 255 else 0) for pix in plainimg]

    return Image.fromarray(np.asarray(plainimg).reshape(shape).astype(np.uint8))


def homomorphicBrightness(public_key: paillier.PublicKey, cipherimg: np.ndarray, factor: int) -> np.ndarray:

    shape = cipherimg.shape
    brightimg = cipherimg.flatten().tolist()
    brightimg = [public_key.homomorphic_add(pix, factor) for pix in brightimg]

    return np.asarray(brightimg).reshape(shape)


def saveEncryptedImg(cipherimg: np.ndarray, filename: str) -> None:

    filename = f"encrypted-images/{filename}"
    fstream = open(filename, "wb")
    pickle.dump(cipherimg, fstream)
    fstream.close()


def loadEncryptedImg(filename: str) -> np.ndarray:

    filename = f"encrypted-images/{filename}"
    fstream = open(filename, "rb")
    cipherimg = pickle.load(fstream)
    fstream.close()
    return cipherimg
