import os
import numpy as np

DIGITSIZE = 28
DATADIR = "digitdata"

def makeMatrix(size=DIGITSIZE):
    return np.zeros((size, size), dtype=int)

def convertToBinary(image, size=DIGITSIZE):
    # convert datafile line to 0s and 1s
    # returns a bool np ndarray
    ret = np.zeros((size, size), dtype=bool)
    for row, line in enumerate(image):
        for col, char in enumerate(line):
            ret[row][col] = (char != ' ')
    return ret

def convertToProbMatrix(matrix, length, smoothing=1):
    # converts from int matrix to float matrix (each val between 0 and 1)
    # also applies Laplace smoothing
    if smoothing < 1 or type(smoothing) != int:
        raise ValueError("Smoothing must be a positive integer: {0}".format(smoothing))
    ret = np.zeros(matrix.shape, dtype=float)
    for row, line in enumerate(matrix):
        for col, num in enumerate(line):
            ret[row][col] = float(num + smoothing) / (length + smoothing*10)
    return ret

def parseDataFile(prefix):
    prefix = os.path.join(DATADIR, prefix)
    labelfile = prefix + "labels"
    with open(labelfile, "r") as f:
        labels = map(int, list(f))
    
    imagefile = prefix + "images"
    with open(imagefile, "r") as f:
        lines = map(lambda s: s.replace('\n', ''), list(f))
        if len(lines) % 28 != 0:
            raise ValueError("# lines of {0} must be divisible by 28: {1}", imagefile, str(lines%28))
        images = []
        for a, b in zip(range(0, len(lines)/28, 28), range(28, len(lines)/28+1, 28)):
            images.append(lines[a:b])

    # Match labels and images
    return zip(labels, map(convertToBinary, images))

def constructTrainingSet():
    trainingSet = parseDataFile("training")
    freqs = []
    for n in range(10):
        freqs.append(makeMatrix())
    for num, image in trainingSet:
        freqs[num] = np.add(freqs[num], image)
    length = len(trainingSet)
    return map(lambda freq: convertToProbMatrix(freq, length), freqs)

freqs = constructTrainingSet()
