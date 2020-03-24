import glob
import xml.etree.ElementTree as ET

classes = ["r2d2","c3po","luke-skywalker","obi-wan-kinobi","sturmtruppler"]
annotation_path = '/Users/rwartala/Google Drive/data/ix-tut-annotations/'

def convert_voc_annotation(voc_filename):
    in_file = open(voc_filename)
    tree=ET.parse(in_file)
    root = tree.getroot()
    yolo_line = ""

    image_filename = root.find('path').text

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        yolo_line = image_filename + " " + ",".join([str(a) for a in b]) + ',' + str(cls_id)

    return yolo_line


# erstelle Liste aller VOC = Bild Dateinamen mit XML
voc_filenames = glob.glob(annotation_path+'/*.xml')
voc_filenames.sort()

for voc_filename in voc_filenames:
    yolo_line = convert_voc_annotation(voc_filename)
    print(yolo_line)
