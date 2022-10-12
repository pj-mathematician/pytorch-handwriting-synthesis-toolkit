from .base import Provider, DataSplittingProvider
import xml.etree.ElementTree as ET
import os
# Create a subclasses of Provider here


class MyProvider(Provider):
    name = 'example'

    def get_training_data(self):
        raise NotImplementedError

    def get_validation_data(self):
        raise NotImplementedError

class DummyProvider(Provider):
    name = 'ADAB'

    def __init__(self, data_path = None, validation_size = 0.2):
        if data_path is None:
            data_path = '/content'

        handwriting_strokes = []
        transcript_keys = []
        for k in [1,2,3]:
          for i in os.listdir(data_path+'/set_{}/inkml'.format(k)):
            f = open(data_path+'/set_{}/inkml/'.format(k)+i)
            x = f.read()
            f.close()
            tree = ET.fromstring(x)
            temp = []
            for i in tree[2:]:
              temp.append([tuple(map(int,(i.split()[0],i.split()[1]))) for i in i.text.split(',')])
            # [tuple(map(int,(i.split()[0],i.split()[1]))) for i in tree[2].text.split(',')] # from 2 till end
            handwriting_strokes.append(temp)
        for k in [1,2,3]:
          for i in os.listdir(data_path+'/set_{}/upx'.format(k)):
            f = open(data_path+'/set_{}/upx/'.format(k)+i)
            x = f.read()
            f.close()
            tree = ET.fromstring(x)
            transcript_keys.append(tree[2][0][0][0].attrib['value'])
        data_strokes_modified = []
        for i in handwriting_strokes:
          data_strokes_modified.append(i[::-1])
        handwriting_strokes = data_strokes_modified
        # print('loaded')
        splitting_index = int(len(transcript_keys) * validation_size)
        # print(splitting_index)
        self.validation_strokes = handwriting_strokes[0:splitting_index]
        self.training_strokes = handwriting_strokes[splitting_index:]
        self.validation_keys = transcript_keys[0:splitting_index]
        self.training_keys = transcript_keys[splitting_index:]
        # print(len(self.training_keys), len(self.validation_keys))
        # print("split")
    def get_training_data(self):
        for handwriting, transcript in zip(self.training_strokes, self.training_keys):
            yield handwriting, transcript

    def get_validation_data(self):
        for handwriting, transcript in zip(self.validation_strokes, self.validation_keys):
            yield handwriting, transcript
