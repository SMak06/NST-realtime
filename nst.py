# importing necessary packages
import argparse
import imutils
import time
import cv2

# construct the argument parser and parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
	help="neural style transfer model")
ap.add_argument("-i", "--image", required=True,
	help="input image to apply neural style transfer to")
args = vars(ap.parse_args())

# Here, the neural style transfer model is being loaded from the directory
print("[INFO] style transfer model is being loaded...")
net = cv2.dnn.readNetFromTorch(args["model"])

# input image is anow loaded and resized to a width of 600px, and
# then image dimensions are grapped
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
(h, w) = image.shape[:2]

# construct a blob from the image, set the input, and then perform a
# forward pass of the network
blob = cv2.dnn.blobFromImage(image, 1.0, (w, h),
	(103.939, 116.779, 123.680), swapRB=False, crop=False)
net.setInput(blob)
start = time.time()
output = net.forward()
end = time.time()

# reshape the output tensor, add back in the mean subtraction, and
# then swap the channel ordering
output = output.reshape((3, output.shape[2], output.shape[3]))
output[0] += 103.939
output[1] += 116.779
output[2] += 123.680
output /= 255.0
output = output.transpose(1, 2, 0)

# show information on how long inference took
print("[INFO] neural style transfer took {:.4f} seconds".format(
	end - start))

# show the images
cv2.imshow("Input", image)
cv2.imshow("Output", output)
cv2.waitKey(0)
