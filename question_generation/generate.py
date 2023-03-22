import argparse, json, os, itertools, random, shutil
import glob
import time
import re

parser = argparse.ArgumentParser()

# Inputs
parser.add_argument('--properties_json', default='/home/nlp/users/bkroje/clevr/image_generation/data/properties.json',
    help="JSON file containing properties.")
parser.add_argument('--scenes_dir', default='/home/nlp/users/bkroje/clevr/output/scenes/',
    help="Directory containing scene jsons.")

# Output
parser.add_argument('--output_dir', default='/home/nlp/users/bkroje/clevr/output/',
    help="The output dir")


args = parser.parse_args()
recognition_shape = {}
recognition_color = {}
binding_color_shape = {}
binding_shape_color = {}
binding_size_shape = {}
pair_binding_size = {}
pair_binding_color = {}
spatial = {}

properties = json.load(open(args.properties_json)) # dict_keys(['shapes', 'colors', 'materials', 'sizes'])
shapes = properties['shapes'].keys()
colors = properties['colors'].keys()
sizes = properties['sizes'].keys()

def gen_recognition_shape(obj1_shape, obj2_shape):
    shape_not_present = list(set(shapes) - {obj1_shape, obj2_shape})
    right1 = f"A {obj1_shape}."
    right2 = f"A {obj2_shape}."
    wrong = f"A {shape_not_present[0]}."
    return [[right1, wrong], [right2, wrong]]

def gen_recognition_color(obj1_color, obj2_color):
    color_not_present = list(set(colors) - {obj1_color, obj2_color})
    right1 = f"A {obj1_color} object."
    right2 = f"A {obj2_color} object."
    wrong = f"A {random.choice(color_not_present)} object."
    return [[right1, wrong], [right2, wrong]]
    
def gen_binding_color_shape(obj1_color, obj1_shape, obj2_color, obj2_shape):
    right1 = f"A {obj1_color} {obj1_shape}."
    wrong1 = f"A {obj2_color} {obj1_shape}."
    right2 = f"A {obj2_color} {obj2_shape}."
    wrong2 = f"A {obj1_color} {obj2_shape}."
    return [[right1, wrong1], [right2, wrong2]]

def gen_binding_size_shape(obj1_size, obj1_shape, obj2_size, obj2_shape):
    right1 = f"A {obj1_size} {obj1_shape}."
    wrong1 = f"A {obj2_size} {obj1_shape}."
    right2 = f"A {obj2_size} {obj2_shape}."
    wrong2 = f"A {obj1_size} {obj2_shape}."
    return [[right1, wrong1], [right2, wrong2]]

def gen_binding_shape_color(obj1_color, obj1_shape, obj2_color, obj2_shape):
    right1 = f"A {obj1_color} {obj1_shape}."
    wrong1 = f"A {obj1_color} {obj2_shape}."
    right2 = f"A {obj2_color} {obj2_shape}."
    wrong2 = f"A {obj2_color} {obj1_shape}."
    return [[right1, wrong1], [right2, wrong2]]

def gen_pair_binding_size(obj1_size, obj1_shape, obj2_size, obj2_shape):
    right1 = f"A {obj1_size} {obj1_shape} and a {obj2_size} {obj2_shape}."
    wrong1 = f"A {obj2_size} {obj1_shape} and a {obj1_size} {obj2_shape}."
    right2 = f"A {obj2_size} {obj2_shape} and a {obj1_size} {obj1_shape}."
    wrong2 = f"A {obj1_size} {obj2_shape} and a {obj2_size} {obj1_shape}."
    return [[right1, wrong1], [right2, wrong2]]

def gen_pair_binding_color(obj1_color, obj1_shape, obj2_color, obj2_shape):
    right1 = f"A {obj1_color} {obj1_shape} and a {obj2_color} {obj2_shape}."
    wrong1 = f"A {obj2_color} {obj1_shape} and a {obj1_color} {obj2_shape}."
    right2 = f"A {obj2_color} {obj2_shape} and a {obj1_color} {obj1_shape}."
    wrong2 = f"A {obj1_color} {obj2_shape} and a {obj2_color} {obj1_shape}."
    return [[right1, wrong1], [right2, wrong2]]

def gen_spatial(obj1_pos, obj1_color, obj1_shape, obj2_pos, obj2_color, obj2_shape):
    right1 = f"On the {obj1_pos} is a {obj1_color} {obj1_shape}."
    wrong1 = f"On the {obj2_pos} is a {obj1_color} {obj1_shape}."
    right2 = f"On the {obj2_pos} is a {obj2_color} {obj2_shape}."
    wrong2 = f"On the {obj1_pos} is a {obj2_color} {obj2_shape}."
    return [[right1, wrong1], [right2, wrong2]]


scenes = glob.glob(args.scenes_dir + '*.json')

for scene in scenes:
    img_scene = json.load(open(scene))
    fname = img_scene['image_filename']
    # print(fname)
    (obj1, obj2) = img_scene['objects']
    
    # if theres an overlap of attributes, continue
    if obj1['shape'] == obj2['shape'] or obj1['color'] == obj2['color'] or obj1['size'] == obj2['size'] or obj1['material'] == obj2['material']:
        # print(f"-------------overlap, skipping---------------")
        continue
    
    for (pos, (ob1,ob2)) in img_scene['relationships'].items():
        if pos not in ['left','right']: continue
        if ob1: obj1_rel_pos = pos
        elif ob2: obj2_rel_pos = pos
        
    recognition_shape[fname] = gen_recognition_shape(obj1['shape'], obj2['shape'])
    recognition_color[fname] = gen_recognition_color(obj1['color'], obj2['color'])
    binding_color_shape[fname] = gen_binding_color_shape(obj1['color'], obj1['shape'], obj2['color'], obj2['shape'])
    binding_shape_color[fname] = gen_binding_shape_color(obj1['color'], obj1['shape'], obj2['color'], obj2['shape'])
    binding_size_shape[fname] = gen_binding_size_shape(obj1['size'], obj1['shape'], obj2['size'], obj2['shape'])
    pair_binding_size[fname] = gen_pair_binding_size(obj1['size'], obj1['shape'], obj2['size'], obj2['shape'])
    pair_binding_color[fname] = gen_pair_binding_color(obj1['color'], obj1['shape'], obj2['color'], obj2['shape'])
    spatial[fname] = gen_spatial(obj1_rel_pos, obj1['color'], obj1['shape'], obj2_rel_pos, obj2['color'], obj2['shape'])


json.dump(recognition_shape,open(args.output_dir + 'recognition_shape.json','w'))
json.dump(recognition_color,open(args.output_dir + 'recognition_color.json','w'))
json.dump(binding_color_shape,open(args.output_dir + 'binding_color_shape.json','w'))
json.dump(binding_shape_color,open(args.output_dir + 'binding_shape_color.json','w'))
json.dump(pair_binding_size,open(args.output_dir + 'pair_binding_size.json','w'))
json.dump(pair_binding_color,open(args.output_dir + 'pair_binding_color.json','w'))
json.dump(spatial,open(args.output_dir + 'spatial.json','w'))
    
    
    
"""
Desired output:
{
    "CLEVR_new_000000.png": [
        ["correct", "incorrect"],["correct", "incorrect"],...
        ]
    
}
"""
  