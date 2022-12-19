import json
import os

import datasets

_CITATION = ""

_DESCRIPTION = ""

_HOMEPAGE = ""

_LICENSE = ""

# The HuggingFace Datasets library doesn't host the datasets but only points to the original raw_files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/LiorLevi15/NLP-MINI-PROJECT/tree/master/DATA/parsed_data_splits"


class RabbiKook(datasets.GeneratorBasedBuilder):
    VERSION = datasets.Version("1.1.0")

    def _info(self):
        features = datasets.Features(
            {
                "id": datasets.Value("string"),
                "paragraph": datasets.Value("string"),
                "summery": datasets.Value("string"),
            }
        )
        return datasets.DatasetInfo(
            # This defines the different columns of the dataset and their types
            features=features,  # Here we define them above because they are different between the two configurations
            # If there's a common (input, target) tuple from the features, uncomment supervised_keys line below and
            # specify them. They'll be used if as_supervised=True in builder.as_dataset.
            # supervised_keys=("sentence", "label"),
        )

    def _split_generators(self, dl_manager):
        # This method is tasked with downloading/extracting the data and defining the splits.

        # dl_manager is a datasets.download.DownloadManager that can be used to download and extract URLS It can
        # accept any type or nested list/dict and will give back the same structure with the url replaced with path
        # to local raw_files. By default the archives will be extracted and a path to a cached folder where they are
        # extracted is returned instead of the archive
        data_dir = dl_manager.download_and_extract(_URL)
        return [
            datasets.SplitGenerator(
                name=datasets.Split.TRAIN,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "rabbi_kook_train.json"),
                    "split": "train",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.VALIDATION,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "rabbi_kook_validate.json"),
                    "split": "dev",
                },
            ),
            datasets.SplitGenerator(
                name=datasets.Split.TEST,
                # These kwargs will be passed to _generate_examples
                gen_kwargs={
                    "filepath": os.path.join(data_dir, "rabbi_kook_test.json"),
                    "split": "test"
                },
            ),
        ]

    # method parameters are unpacked from `gen_kwargs` as given in `_split_generators`
    def _generate_examples(self, filepath, split):
        # TODO: This method handles input defined in _split_generators to yield (key, example) tuples from the dataset.
        # The `key` is for legacy reasons (tfds) and is not important in itself, but must be unique for each example.
        with open(filepath, encoding="utf-8") as f:
            for _, row in enumerate(f):
                data = json.loads(row)
                # Yields examples as (key, example) tuples
                yield data["id"], {
                    "paragraph": data["paragraph"],
                    "summary": data["summary"],
                    "id": data["id"],
                }
