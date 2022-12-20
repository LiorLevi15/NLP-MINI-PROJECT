import json
from typing import List

import datasets

_CITATION = ""

_DESCRIPTION = ""

_HOMEPAGE = ""

_LICENSE = ""

# The HuggingFace Datasets library doesn't host the datasets but only points to the original raw_files.
# This can be an arbitrary nested dict/list of URLs (see below in `_split_generators` method)
_URL = "https://github.com/LiorLevi15/NLP-MINI-PROJECT/tree/master/DATA/parsed_data_splits/"
_URLS = {
    "train": _URL + "rabbi_kook_train.json",
    "test": _URL + "rabbi_kook_test.json",
    "dev": _URL + "rabbi_kook_dev.json",
}


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

    def _split_generators(self, dl_manager: datasets.DownloadManager) -> List[datasets.SplitGenerator]:
        urls_to_download = self._URLS
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        """This function returns the examples in the raw (text) form."""
        print(f'generating examples from = {filepath}')
        with open(filepath) as f:
            data_list = json.load(f)
            for data in data_list:
                yield data["id"], {
                    "paragraph": data["paragraph"],
                    "summary": data["summary"],
                    "id": data["id"],
                }
