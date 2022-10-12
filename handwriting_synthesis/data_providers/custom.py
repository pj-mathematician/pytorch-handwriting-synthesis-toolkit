from .base import Provider, DataSplittingProvider

# Create a subclasses of Provider here


class MyProvider(Provider):
    name = 'example'

    def get_training_data(self):
        raise NotImplementedError

    def get_validation_data(self):
        raise NotImplementedError

class ADABProvider(Provider):
    name = 'ADAB'

    def __init__(self, data_path = None, validation_size = 0.2):
        if data_path is None:
            data_path = '../ADAB_home'
        
        f = open(data_path+'/strokes.txt','r')
        handwriting_strokes = eval(f.read())
        f.close()
        f = open(data_path+'/keys.txt','r')
        transcript_keys = eval(f.read())
        f.close()
        
        splitting_index = int(len(transcript_keys) * validation_size)

        self.validation_strokes = handwriting_strokes[0:splitting_index]
        self.training_strokes = handwriting_strokes[splitting_index:]
        self.validation_keys = transcript_keys[0:splitting_index]
        self.training_keys = transcript_keys[splitting_index:]

    def get_training_data(self):
        for handwriting, transcript in zip(self.training_strokes, self.training_keys):
            yield handwriting, transcript

    def get_validation_data(self):
        for handwriting, transcript in zip(self.validation_strokes, self.validation_keys):
            yield handwriting, transcript
