# Commented out IPython magic to ensure Python compatibility.
import os

from utils import temp

class InferenceConfig(temp.BalloonConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


class LoadModel():
    def __init__(self, **kwargs):
        # Root directory of the project
        ROOT_DIR = os.path.abspath("./")

        # Directory to save logs and trained model
        self.MODEL_DIR = os.path.join(ROOT_DIR, "utils/logs")

        # Local path to trained weights file
        self.COCO_MODEL_PATH = os.path.join(
            ROOT_DIR, "utils/logs/mask_rcnn_recycle_0030.h5")
        print(self.COCO_MODEL_PATH)

    def result_visualize(self, pil, IMAGE_DIR=None):
        import numpy as np
        from PIL import Image

        # Import Mask RCNN
        from utils.mrcnn.model import MaskRCNN
        from utils.mrcnn import visualize

        config = InferenceConfig()
        config.display()
        """## Create Model and Load Trained Weights"""

        # Create model object in inference mode.
        model = MaskRCNN(mode="inference", model_dir=self.MODEL_DIR, config=config)

        # Load weights trained on MS-COCO
        model.load_weights(self.COCO_MODEL_PATH, by_name=True)

        # Define classes
        class_names = ['BG', 'glass_bottle', 'pet', 'can']

        """## Run Object Detection"""

        # Load a random image from the images folder
        # file_names = next(os.walk(IMAGE_DIR))[2]

        if pil is not None:
            pil = pil.convert('RGB')
        else:
            file_list = [f'{path}/{file}' for path, _,
                         files in os.walk(IMAGE_DIR) for file in files if 'upload' in file]
            file_name = file_list[-1]
            pil = Image.open(file_name).convert('RGB')

        image = np.array(pil)
        # Run detection
        results = model.detect(image, verbose=1)

        # Visualize results
        r = results[0]
        print(r['class_ids'])
        visualize.display_instances(
            image, r['rois'], r['masks'], r['class_ids'], self.class_names, r['scores'], save=True)

        file_list = [f'{path}/{file}' for path, _,
                     files in os.walk('./images') for file in files if 'result' in file]
        file_name = file_list[-1]
        r_pil = Image.open(file_name)
        return r_pil
