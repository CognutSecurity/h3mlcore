"""
Preprocessor is a class used to preprocess the raw data to machine learning readable dataset.
The run method in Preprocessor will iterate over each worker to process your input data, output
is a N*D numeric trainable dataset, where N is the number of training samples, and D is the feature dimensionality.

You need to define a proper preprocessor with a proper pipeline of workers for the classifier you are using.

Author: Huang Xiao
Email: xh0217@gmail.com
Copyright@2016, Stanford
"""

import importlib

class Preprocessor(object):
    """Preprocessor main class: the pipeline for preprocessing raw data to generate vectorized feature set
    It is mainly used in the first step in any learning cycle.
    
    Example:
        import json
    
        X = json.load(open('data.json'))
        workers = [('Tokenizer', {'language': 'english', 'nonstop': 'english'}),
                   ('Stemmer', {'type': 'Poster'})]
        prep = Preprocessor(workers)
        dataset_tr = prep.run(X)

    Args:

    Returns:

    """

    def __init__(self, pipeline, feature_names=list()):
        """
        Preprocessing the raw data to build feature vectors, we use a pipeline to get our job done,
        after initialization pipeline is a list of objects to prepare the feature vectors
        
        Args:
          pipeline: a list of tuples (Worker, dict)
          feature_names: list of str for feature names
        
        """

        self._PIPELINE = list()
        self._FEATURE_NAMES = feature_names
        self._FEATURE_SIZE = 0
        for elem in pipeline:
            worker_class = getattr(importlib.import_module("h3mlcore.io.PipelineWorkers"), elem['worker'])
            if elem.has_key('params'):
                worker = worker_class(elem['params'])
            else:
                worker = worker_class()
            self._PIPELINE.append(worker)


    def run(self, data_raw, restart=False):
        """Start processing

        Args:
          data_raw: raw dataset to be preprocessed
          restart:  (Default value = False) if we should restart transform data 

        Returns:
          ndarray: feature set for training

        """

        for worker in self._PIPELINE:
            if restart or not worker.fitted:
                data_raw = worker.transform(data_raw)
            else:
                data_raw = worker.partial_transform(data_raw)

            # we set the feature names from HashParser's feature mapping
            if worker.__class__.__name__ == 'HashParser':
                self._FEATURE_NAMES = worker.feature_mapping.keys()
                
        self._FEATURE_SIZE = data_raw.shape[1]
        return data_raw

