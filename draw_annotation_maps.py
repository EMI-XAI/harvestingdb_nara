# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw
from tqdm.auto import tqdm

#---------------------------------------------------------------------
def make_argparser():
    parser = argparse.ArgumentParser(
        "Draw annotation maps from geometry information of attentional"
        " region that is output from our annotation tool.")

    parser.add_argument("--input_name", default="./harvestingdb_nara.csv",
                        help="A list of Geometry of attentional regions."
                        " (default: ./harvestingdb_nara.csv)")
    parser.add_argument("--output_dir", default="./maps",
                        help="Output directory. (default: ./maps)")
    parser.add_argument("--annotations", type=int, nargs="+", default=[1, 2, 3],
                        help="Annotation IDs to be used for map generation."
                        " (default: 1 2 3)")

    return parser

#---------------------------------------------------------------------
def get_image_info(df, index):
    img_path = Path(df.loc[index, "Image"])
    img_cls, img_name = img_path.parts
    img_id = Path(img_name).stem

    return img_cls, img_id

def get_annotation_info(df, index):
    angle    = df.loc[index, "Answer.anno_angle"]
    cent_x   = df.loc[index, "Answer.anno_centx"]
    cent_y   = df.loc[index, "Answer.anno_centy"]
    img_ht   = df.loc[index, "Answer.anno_imght"]
    img_wd   = df.loc[index, "Answer.anno_imgwd"]
    scale    = df.loc[index, "Answer.anno_scale"]
    size_x   = df.loc[index, "Answer.anno_sizex"]
    size_y   = df.loc[index, "Answer.anno_sizey"]
    category = df.loc[index, "Answer"]

    return (category, cent_x, cent_y, size_x, size_y, angle,
            img_wd, img_ht, scale)

def get_time_info(df, index):
    sec = df.loc[index, "WorkTimeInSeconds"]

    return sec,

#---------------------------------------------------------------------
def make_blank_image(img_size, base_val=0):
    return Image.new("RGB", img_size, (base_val,) * 3)

def draw_ellipse(draw, cent, radius, angle, fill):
    assert len(cent) == 2 and len(radius) == 2
    cos, sin = np.cos(angle), np.sin(angle)

    rads = np.arange(360) / 180 * np.pi
    xs = np.cos(rads) * radius[0]
    ys = np.sin(rads) * radius[1]

    coords = []
    for x, y in zip(xs, ys):
        rx = cos * x - sin * y + cent[0]
        ry = sin * x + cos * y + cent[1]
        coords.append((rx, ry))

    draw.polygon(coords, fill=fill)

def calc_mean_image(image_list):
    mean = np.stack([np.asarray(img) for img in image_list]).mean(axis=0)
    return Image.fromarray(mean.astype(np.uint8))

#---------------------------------------------------------------------
def main(args):
    df = pd.read_csv(args.input_name)

    # Read annotation information.
    anno_list = {}
    for index in range(len(df)):
        img_cls, img_id = get_image_info(df, index)
        (category, cent_x, cent_y, size_x, size_y, angle,
         img_wd, img_ht, scale) = get_annotation_info(df, index)

        items = (category, cent_x, cent_y, size_x, size_y, angle,
                 img_wd, img_ht, scale)
        if (img_cls, img_id) not in anno_list:
            anno_list[(img_cls, img_id)] = [items]
        else:
            anno_list[(img_cls, img_id)].append(items)

    for (img_cls, img_id), items_list in tqdm(anno_list.items()):
        assert len(items_list) == 3  ## 各画像 3 アノテーションある筈

        # Draw annotation maps.
        maps = []
        for items in items_list:
            (category, cent_x, cent_y, size_x, size_y, angle,
             img_wd, img_ht, scale) = items
            img_size = img_wd, img_ht
            map = make_blank_image(img_size, base_val=0)
            draw = ImageDraw.Draw(map)
            draw_ellipse(draw, (cent_x, cent_y), (size_x, size_y), angle,
                         fill=(255, 255, 255))
            maps.append(map)

        # Combine maps.
        result_map = calc_mean_image([maps[i - 1] for i in args.annotations])

        # Save the combined map.
        map_fname = Path(args.output_dir) / img_cls / f"{img_id}.png"
        map_fname.parent.mkdir(parents=True, exist_ok=True)
        result_map.save(map_fname)

#---------------------------------------------------------------------
if __name__ == "__main__":
    parser = make_argparser()
    args = parser.parse_args()
    main(args)
