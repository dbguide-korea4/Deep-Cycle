import os
import pathlib
import json

import dash_core_components as dcc
import plotly.graph_objs as go
import dash_reusable_components as drc

from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

# drc = importlib.import_module("apps.dash-iamge-processing.dash_reusable_components")

#
APP_PATH = str(pathlib.Path(__file__).parent.resolve())

# [filename, image_signature, action_stack]
STORAGE_PLACEHOLDER = json.dumps(
    {"filename": None, "image_signature": None, "action_stack": []}
)

IMAGE_STRING_PLACEHOLDER = drc.pil_to_b64(
    Image.open(os.path.join(APP_PATH, os.path.join("images", "default.jpeg"))).copy(),
    enc_format="jpeg",
)

GRAPH_PLACEHOLDER = dcc.Graph(
    id="interactive-image",
    figure={
        "data": [],
        "layout": {
            "autosize": True,
            "paper_bgcolor": "#272a31",
            "plot_bgcolor": "#272a31",
            "margin": go.Margin(l=40, b=40, t=26, r=10),
            "xaxis": {
                "range": (0, 1527),
                "scaleanchor": "y",
                "scaleratio": 1,
                "color": "white",
                "gridcolor": "#43454a",
                "tickwidth": 1,
            },
            "yaxis": {
                "range": (0, 1200),
                "color": "white",
                "gridcolor": "#43454a",
                "tickwidth": 1,
            },
            "images": [
                {
                    "xref": "x",
                    "yref": "y",
                    "x": 0,
                    "y": 0,
                    "yanchor": "bottom",
                    "sizing": "stretch",
                    "sizex": 1527,
                    "sizey": 1200,
                    "layer": "below",
                    "source": "/images/default.jpeg",
                }
            ],
            "dragmode": "select",
        },
    },
)

# Maps process name to the Image filter corresponding to that process
FILTERS_DICT = {
    "blur": ImageFilter.BLUR,
    "contour": ImageFilter.CONTOUR,
    "detail": ImageFilter.DETAIL,
    "edge_enhance": ImageFilter.EDGE_ENHANCE,
    "edge_enhance_more": ImageFilter.EDGE_ENHANCE_MORE,
    "emboss": ImageFilter.EMBOSS,
    "find_edges": ImageFilter.FIND_EDGES,
    "sharpen": ImageFilter.SHARPEN,
    "smooth": ImageFilter.SMOOTH,
    "smooth_more": ImageFilter.SMOOTH_MORE,
}

ENHANCEMENT_DICT = {
    "color": ImageEnhance.Color,
    "contrast": ImageEnhance.Contrast,
    "brightness": ImageEnhance.Brightness,
    "sharpness": ImageEnhance.Sharpness,
}


def generate_lasso_mask(image, selectedData):
    """
    Generates a polygon mask using the given lasso coordinates
    :param selectedData: The raw coordinates selected from the data
    :return: The polygon mask generated from the given coordinate
    """

    height = image.size[1]
    y_coords = selectedData["lassoPoints"]["y"]
    y_coords_corrected = [height - coord for coord in y_coords]

    coordinates_tuple = list(zip(selectedData["lassoPoints"]["x"], y_coords_corrected))
    mask = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask)
    draw.polygon(coordinates_tuple, fill=255)

    return mask


def apply_filters(image, zone, filter, mode):
    filter_selected = FILTERS_DICT[filter]

    if mode == "select":
        crop = image.crop(zone)
        crop_mod = crop.filter(filter_selected)
        image.paste(crop_mod, zone)

    elif mode == "lasso":
        im_filtered = image.filter(filter_selected)
        image.paste(im_filtered, mask=zone)


def apply_enhancements(image, zone, enhancement, enhancement_factor, mode):
    enhancement_selected = ENHANCEMENT_DICT[enhancement]
    enhancer = enhancement_selected(image)

    im_enhanced = enhancer.enhance(enhancement_factor)

    if mode == "select":
        crop = im_enhanced.crop(zone)
        image.paste(crop, box=zone)

    elif mode == "lasso":
        image.paste(im_enhanced, mask=zone)
