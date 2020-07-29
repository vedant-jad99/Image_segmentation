import numpy as np 
from random import randint
import cv2

class Segmentation:
    def __init__(self, path, k):
        super().__init__()
        try:
            self.image = cv2.imread(path)
            if len(self.image) != 0:
                self.shape = self.image.shape
                self.image = cv2.resize(self.image, (int(0.3 * self.image.shape[1]), int(0.3 * self.image.shape[0])))
                self.centers = []
                for i in range(k):
                    self.centers.append(self.image[randint(0, self.image.shape[0] - 1), randint(0, self.image.shape[1] - 1)])
                self.clusters = {}
                for i in range(0, k):
                    self.clusters[str(i + 1)] = []
            else:
                exit()
        except TypeError:
            print("Image file not found. Exiting...")
            exit()
    def k_means(self):
        m = [np.array([0, 0, 0], dtype=np.uint8)] * len(self.centers)
        while all([np.allclose(x, y) for x, y in zip(m, self.centers)]) == False:
            print("Epoching...")
            self.cluster_clear()
            for i in range(self.image.shape[0]):
                for j in range(self.image.shape[1]):
                    distances = []; count = 0 
                    for k in self.centers:
                        distances.append([np.linalg.norm(self.image[i, j] - k), str(count + 1)])
                        self.clusters[sorted(distances)[0][1]].append([i, j])
                        count += 1
            m[:] = self.centers[:]
            self.optimize()
        print("Done!!!")
        colors = []
        for i in self.centers:
            colors.append(i)
        for i in self.clusters:
            for j in self.clusters[i]:
                self.image[j[0]][j[1]] = colors[int(i) - 1]
        self.image = cv2.resize(self.image, (int(0.8 * self.shape[1]), int(0.8 * self.shape[0])))
    def optimize(self):
        for i in self.clusters:
            sum_array = np.array([0, 0, 0], dtype=np.int64)
            for j in self.clusters[i]:
                sum_array += self.image[j[0], j[1]]
            self.centers.pop(0)
            sum_array = sum_array/len(self.clusters[i])
            self.centers.append(sum_array.astype(np.int64))
        print(self.centers)
    def cluster_clear(self):
        for i in self.clusters:
            self.clusters[i] = []

seg = Segmentation("traffic.jpg", 8)
seg.k_means()
cv2.imshow("Image", seg.image)
cv2.imwrite("Saves/k=8.jpg", seg.image)
cv2.waitKey(0)