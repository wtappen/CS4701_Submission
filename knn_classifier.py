# import numpy as np


class classifier():
    def __init__(self, k, n_w, c_d, n_e, dist):
        self.k = k
        self.class_dict = c_d 
        self.neg_ex = n_e 
        self.dist_fun = dist

        self.points = []
        for label in self.class_dict:
            for vec in self.class_dict[label]:
                self.points.append((label, vec, 1))

        for vec in n_e:
            self.points.append(("neg", vec, n_w))

    def classify(self, inputvec):
        def insert_into(value, lst):
            inserted = False
            for i in range(len(lst)):
                if value[0] > lst[i][0]:
                    lst.insert(i, value)
                    inserted = True
            if not inserted:        
                lst.append(value)
            return lst

        k_closest = []

        for (label, vec, weight) in self.points:
            dist = self.dist_fun(vec, inputvec)
            if len(k_closest) < self.k:
                k_closest = insert_into((dist, label, weight), k_closest)
            elif dist < k_closest[0][0]:
                k_closest.pop(0)
                k_closest = insert_into((dist, label, weight), k_closest)

        labels = {}
        for (_, label, weight) in k_closest:
            if label in labels:
                labels[label] += weight
            else:
                labels[label] = weight

        max_val = 0
        best_label = "neg"

        for label in labels:
            if labels[label] > max_val:
                best_label = label
                max_val = labels[label]

        return best_label


def l2_dist(v1, v2):
    sum_squares = 0
    for i in range(len(v1)):
        sum_squares += (v1[i]-v2[i]) ** 2

    return sum_squares


class_dict = {}
class_dict["1"] = [[1,0,0,0,0],[2,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0]]
class_dict["2"] = [[0,2,0,0,0],[0,1,0,0,0],[0,1,0,0,0],[0,4,0,0,0]]
neg_vals = [[0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0], [0,0,0,0,0]]

neg_w = 1

c = classifier(5, .2, class_dict, neg_vals, l2_dist)
print(c.classify([500,0,0,0,0]))
print(c.classify([0,50,0,0,0]))