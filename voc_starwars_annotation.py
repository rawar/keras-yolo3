import glob
import xml.etree.ElementTree as ET

classes = ["r2d2","c3po","luke-skywalker","obi-wan-kinobi","sturmtruppler"]
annotation_path = '/Users/rwartala/Google Drive/data/ix-tut-annotations/'
image_path = '/Users/rwartala/Google Drive/data/ix-tut-processed'

def convert_voc_annotation(voc_filename, image_filename):
    in_file = open(voc_filename)
    tree=ET.parse(in_file)
    root = tree.getroot()

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


# erstelle liste aller Bild Dateinamen
image_filenames = glob.glob(image_path+'/*')
# erstelle Liste aller VOC = Bild Dateinamen mit XML
voc_filenames = glob.glob(annotation_path+'/*')

files_dict = dict(zip(voc_filenames, image_filenames))

for voc_filename in files_dict:
    yolo_line = convert_voc_annotation(voc_filename, files_dict[voc_filename])
    print(yolo_line)
