
import random
import math
import copy
import time
from tkinter import *
import numpy as np

NUM_OF_POINTS = 20000
INTERVAL = 5000
DEVIATION = 100
WINDOW_SIZE = 720

colors = ['black', 'cyan', 'darkgreen', 'darkkhaki', 'darkviolet', 'deeppink', 'dimgrey', 'forestgreen', 'gold', 'hotpink', 'lawngreen', 'maroon', 'midnightblue', 'orange', 'red', 'saddlebrown', 'seagreen', 'slateblue', 'springgreen', 'violetred']

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.cluster_id = None
        self.not_in_cluster = True

# prvych 20 unikatnych points
def init():
    first_20 = []
    unique_rand_nums = set()

    while True:
        rand_num = random.randint(-INTERVAL, INTERVAL)
        unique_rand_nums.add(rand_num)

        if len(unique_rand_nums) == 40:
            break

    for index in range(20):
        first_20.append(Point(unique_rand_nums.pop(), unique_rand_nums.pop()))

    return first_20

def generate_others(first_20):
    all_points = []
    all_points += first_20
    counter = 0

    while counter < NUM_OF_POINTS:
        point = random.choice(all_points)

        x_offset = int(random.gauss(-DEVIATION, DEVIATION))
        y_offset = int(random.gauss(-DEVIATION, DEVIATION))

        new_point = Point(point.x + x_offset, point.y + y_offset)
        all_points.append(new_point)
        counter += 1

    return all_points

# vypocita vzdialenost dvoch bodov
def euclidean_dist(point_1, point_2):
    return math.sqrt(math.pow(point_1.x - point_2.x, 2) + math.pow(point_1.y - point_2.y, 2))

def k_means(k, points, medoid_flag):

    clusters = [[] for _ in range(k)]

    # create "k" clusters
    for cluster_num in range(k):
        centroid = random.choice(points)
        points[points.index(centroid)].cluster_id = cluster_num
        clusters[cluster_num].append(centroid)

    # rozdelenie points do clusterou podla toho k comu bude najblizsie
    for point in points:
        best_euclid_dist = 999999999
        for cluster in clusters:
            euclid_dist = euclidean_dist(cluster[0], point)

            if euclid_dist < best_euclid_dist:
                point.cluster_id = clusters.index(cluster)
                best_euclid_dist = euclid_dist

        clusters[point.cluster_id].append(point)

    # 20 krat prepocitaj stred a preskup clustre
    for i in range(20):
        print(f"Iter: {i}")
        clusters_new = []
        # vypocitanie novych centroidov
        for cluster_num in range(k):
            mean_x = np.mean([point.x for point in clusters[cluster_num]])
            mean_y = np.mean([point.y for point in clusters[cluster_num]])
            new_mid = Point(mean_x, mean_y)

            # z centroid urob medoid
            if medoid_flag:
                best_euclid_dist = 999999999
                for point_temp in points:

                    euclid_dist = euclidean_dist(new_mid, point_temp)

                    if euclid_dist < best_euclid_dist:
                        new_mid_2 = point_temp
                        best_euclid_dist = euclid_dist

                new_mid = new_mid_2

            str_temp = "medoid" if medoid_flag else "centroid"
            print(f"Cluster: {cluster_num}, {str_temp}: x:{new_mid.x} y:{new_mid.y}")
            clusters_new.append(new_mid)

        # vytvor nove clustre na zaklade novych stredov
        clusters = [[] for _ in range(k)]
        for point in points:
            best_euclid_dist = 999999999
            for cluster_centroid in clusters_new:
                euclid_dist = euclidean_dist(cluster_centroid, point)

                if euclid_dist < best_euclid_dist:
                    point.cluster_id = clusters_new.index(cluster_centroid)
                    best_euclid_dist = euclid_dist

            clusters[point.cluster_id].append(point)
        print()

    return points

def coordinates(point):
    size = (INTERVAL + DEVIATION) * 4
    left = WINDOW_SIZE / 2 - 1
    right = WINDOW_SIZE / 2 + 1
    return int(point.x / size * WINDOW_SIZE + left), int(point.y / size * WINDOW_SIZE + left), int(point.x / size * WINDOW_SIZE + right), int(point.y / size * WINDOW_SIZE + right)

def draw(points, title):
    master = Tk()
    master.title(title)
    canvas = Canvas(master, width=WINDOW_SIZE, height=WINDOW_SIZE, bg='whitesmoke')
    canvas.pack()

    for point in points:
        canvas.create_oval(coordinates(point), fill=colors[point.cluster_id], outline='')

    master.mainloop()
    pass

def main():
    print("Pycharm starting..")
    random.seed(420)

    first_20 = init()
    all_points = generate_others(first_20)

    user_choise = input("1) K-Means with centroid\n2) K-Means with medoid\n3) Divisive clustering\n4) Agglomerative clustering\nYour choice: ")
    k = 20

    if user_choise == "1":
        start_time = time.time()
        all_points = k_means(k, copy.deepcopy(all_points), False)
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 3), "min")
        draw(all_points, "k_means, centroid")
        # average = summarize(clusters)
        pass

    elif user_choise == "2":
        start_time = time.time()
        all_points = k_means(k, copy.deepcopy(all_points), True)
        end_time = time.time()
        print("Time:", round((end_time - start_time) / 60, 3), "min")
        draw(all_points, "k_means, medoid")
        # average = summarize(clusters)
        pass

    elif user_choise == "3":
        pass
    elif user_choise == "4":
        pass
    pass


if __name__ == "__main__":
    main()
# end