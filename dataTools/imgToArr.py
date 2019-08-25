def src_to_array(src):
    import requests
    from io import BytesIO
    from matplotlib.pyplot import imread

    resp = requests.get(src)
    arr = imread(BytesIO(resp.content), format=resp.headers['Content-Type'].split('/')[-1])
    
    return arr

def path_to_array(img_path):
    import numpy
    from PIL import Image

    arr = numpy.array(Image.open(img_path).convert('RGB'))

    return arr
