import numpy as np
from cellpose import models
import glob
from skimage.io import imread
from skimage.measure import regionprops, label
from scipy.optimize import linear_sum_assignment
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Circle
import cv2
import file_IO

# specify the path to the retrained model and load in
model_path = '/Users/tyleramos/QOI_HACAT_TRACKING/doc/retrained_nuclei'
model = models.CellposeModel(pretrained_model=model_path, gpu=False)

# set image directory path 
directory_path = '/Volumes/almc-cell-migration/Duration data + HeCAT21624__2024-02-16T15_55_35-Measurement 1/Images'
# set nuclei channel
channel_number = 2
# read in images and store in dictionary keyed by frame
tiff_images = file_IO.read_all_tiff_files(directory_path, channel_number)
sorted_frames = sorted(tiff_images.keys())

# subset movie for testing
# Get the first 7 frames
sorted_frames = sorted_frames[:7]

# Subset `tiff_images` to include only the first 7 frames
tiff_images = {key: tiff_images[key] for key in sorted_frames}

segmentation_results = []
all_centroids = []

tracks = {}
next_track_id = 0
max_distance = 20 

# segmentation and feature extraction
for idx, frame_number in enumerate(sorted_frames):
    image = tiff_images[frame_number]

    # segmentation with cellpose
    channels = [0,0]
    masks, flows, styles, diams = model.eval(image, channels=channels, diameter=None)
    segmentation_results.append(masks)

    # Feature Extraction: obtain centroids
    labeled_mask = label(masks)
    props = regionprops(labeled_mask)
    centroids = np.array([prop.centroid for prop in props])
    centroids = centroids[~np.isnan(centroids).any(axis=1)]
    all_centroids.append(centroids)

    # Tracking
    if idx == 0:
        ids = np.arange(len(centroids))
        next_track_id = len(centroids)
    else:
        prev_centroids = all_centroids[idx-1]
        prev_ids = ids

        if len(prev_centroids) == 0 or len(centroids) == 0:
            ids = np.arange(next_track_id, next_track_id + len(centroids))
            next_track_id += len(centroids)
        else:
            cost_matrix = np.linalg.norm(prev_centroids[:, np.newaxis] - centroids, axis=2)
            cost_matrix[cost_matrix > max_distance] = np.inf

            if np.isfinite(cost_matrix).any():
                row_ind, col_ind = linear_sum_assignment(cost_matrix)
                ids = -1 * np.ones(len(centroids), dtype=int)

                for r, c in zip(row_ind, col_ind):
                    if cost_matrix[r, c] != np.inf:
                        ids[c] = prev_ids[r]
                
                unmatched = np.where(ids == -1)[0]
                for idx_unmatched in unmatched:
                    ids[idx_unmatched] = next_track_id
                    next_track_id += 1
            else:
                ids = np.arange(next_track_id, next_track_id + len(centroids))
                next_track_id += len(centroids)
    
    for idx_centroid, track_id in enumerate(ids):
        centroid = centroids[idx_centroid]
        if track_id not in tracks:
            tracks[track_id] = {'frames': [], 'centroids': []}
        tracks[track_id]['frames'].append(frame_number)
        tracks[track_id]['centroids'].append(centroid)
    
    plt.imshow(image, cmap='gray')
    plt.scatter(centroids[:, 1], centroids[:, 0], c='r', marker='o')
    plt.show()

    









'''
# Tracking using Hungarian Algorithm
tracks = {}
next_track_id = 0
max_distance = 100 # change this depending on the maximum distance a cell can move between frames

prev_centroids = None
prev_ids = None

for frame_idx, centroids in enumerate(all_centroids):
    if frame_idx == 0:
        ids = np.arange(len(centroids))
        next_track_id = len(centroids)
    else: 
        if len(prev_centroids) == 0 or len(centroids) == 0:
            ids = np.arange(next_track_id, next_track_id + len(centroids))
            next_track_id += len(centroids)
        else:
            cost_matrix = np.linalg.norm(prev_centroids[:, np.newaxis] - centroids, axis=2)
            cost_matrix[cost_matrix > max_distance] = np.inf
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            ids = -1 * np.ones(len(centroids), dtype=int)
            for r, c in zip(row_ind, col_ind):
                if cost_matrix[r,c] != np.inf:
                    ids[c] = prev_ids[r]
            unmatched = np.where(ids == -1)[0]
            for idx in unmatched:
                ids[idx] = next_track_id
                next_track_id += 1
    # Store tracking data
    for idx, track_id in enumerate(ids):
        centroid = centroids[idx]
        if track_id not in tracks:
            tracks[track_id] = {'frames': [], 'centroids': []}
        tracks[track_id]['frames'].append(frame_idx)
        tracks[track_id]['centroids'].append(centroid)
    prev_centroids = centroids
    prev_ids = ids

# visualization
colors = list(mcolors.TABLEAU_COLORS.keys())
num_colors = len(colors)

# video params
first_image = imread(tiff_images[1])
frame_height, frame_width = first_image.shape
video_name = '~/tyleramos/QOI_HACAT_TRACKING/out/tracking_results.avi'
fps = 5

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_writer = cv2.VideoWriter(video_name, fourcc, fps, (frame_width, frame_height))

for frame_number in sorted_frames:
    image = tiff_images[frame_number]
    image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    for track_id, data in tracks.items():
        if frame_idx in data['frames']:
            idx = data['frames'].index(frame_idx)
            centroid = data['centroids'][idx]
            color = tuple(int(255 * c) for c in mcolors.to_rbg(colors[track_id % num_colors]))
            cv2.circle(image_rgb, (int(centroid[1]), int(centroid[0])), radius=5, color=color, thickness=-1)
            cv2.putText(image_rgb, str(track_id), (int(centroid[1]), int(centroid[0])), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    video_writer.write(image_rgb)
video_writer.release()
'''






