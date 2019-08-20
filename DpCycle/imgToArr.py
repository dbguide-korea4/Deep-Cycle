def url_to_array(url):
    import requests
    from matplotlib.pylab import imread
    from io import BytesIO

    resp = requests.get(url)
    arr = imread(BytesIO(resp.content), format=resp.headers['Content-Type'].split('/')[1])
    
    return arr

def path_to_array(img_path):
    import numpy
    from PIL import Image

    arr = numpy.array(Image.open(img_path).convert('RGB'))

    return arr