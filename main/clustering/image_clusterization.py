import numpy as np
from PIL import Image

from k_means import KMeans


def load_image(image_src: str) -> np.ndarray:
    image = Image.open(image_src)
    return np.asarray(image).astype(float)


def save_image(image_path: str, image_data: np.ndarray) -> bool:
    try:
        image = Image.fromarray(image_data)
        image.save(image_path)
        return True
    except IOError as er:
        print(f'Error saving image!:\n{er}')
        return False


def clustering_image(image_src: str, image_target: str, n_clusters: int = 3, max_iters: int = 100):
    image_data = load_image(image_src)
    rows, cols, depth = image_data.shape if image_data.ndim > 2 else (*image_data.shape, 1)
    image_data = image_data.reshape((rows * cols, depth))

    k_means = KMeans()
    k_means.n_clusters = n_clusters
    k_means.max_iterations = max_iters
    k_means.fit(image_data)
    #
    # k_means.show()
    c_image = np.zeros_like(image_data)
    for center, idx in zip(k_means.clusters_centers, k_means.clusters_points_indices):
        c_image[idx] = center

    c_image = c_image.reshape((rows, cols, depth)).astype('uint8')
    save_image(image_target, c_image)


if __name__ == '__main__':
    clustering_image("../../resources/clustering/anime.jpeg",
                     "../../resources/clustering/saving/anime.png",
                     n_clusters=5)
