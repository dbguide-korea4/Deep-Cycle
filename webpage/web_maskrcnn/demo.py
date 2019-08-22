# Commented out IPython magic to ensure Python compatibility.
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from Mask_RCNN import temp


class InferenceConfig(temp.BalloonConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


class LoadModel():
    def __init__(self, **kwargs):
        # Import Mask RCNN
        import Mask_RCNN.mrcnn.model as modellib

        # Root directory of the project
        ROOT_DIR = os.path.abspath("./Mask_RCNN")

        # Directory to save logs and trained model
        MODEL_DIR = os.path.join(ROOT_DIR, "logs")

        # Local path to trained weights file
        COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_recycle_0030.h5")

        config = InferenceConfig()
        config.display()

        """## Create Model and Load Trained Weights"""

        # Create model object in inference mode.
        self.model = modellib.MaskRCNN(
            mode="inference", model_dir=MODEL_DIR, config=config)

        # Load weights trained on MS-COCO
        self.model.load_weights(COCO_MODEL_PATH, by_name=True)

        # Define classes
        self.class_names = ['BG', 'glass_bottle', 'pet', 'can']

    def result_visualize(self, pil, IMAGE_DIR=None):
        from Mask_RCNN.mrcnn import visualize

        """## Run Object Detection"""

        # Load a random image from the images folder
        # file_names = next(os.walk(IMAGE_DIR))[2]
        
        if IMAGE_DIR is not None:
            file_list = [f'{path}/{file}' for path, _,
                     files in os.walk(IMAGE_DIR) for file in files if 'upload' in file]
            file_name = file_list[-1]
            pil = Image.open(file_name).convert('RGB')
        else:
            pil = pil
        
        image = np.array(pil)
        # Run detection
        results = model.detect([image], verbose=1)

        # Visualize results
        r = results[0]
        print(r['class_ids'])
        visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores'])

        file_list = [f'{path}/{file}' for path, _,
                     files in os.walk(IMAGE_DIR) for file in files if 'result' in file]
        file_name = file_list[-1]
        r_pil = Image.open(file_name)
        return r_pil
