from __future__ import absolute_import, division, print_function
import json
import logging
import datasets

_CITATION = """\
@misc{tahayna2023arabic,
    title = {Arabic Question Answering Datasets},
    author = {Obada Tahayna},
    year = {2023},
    url = {https://github.com/obada-jaras/Arabic-QA-Datasets},
    note = {Aggregated dataset containing Arabic-SQuAD, AAQAD, TyDi QA, MLQA, and ARCD},
}
"""

_DESCRIPTION = """
Arabic-QA-Datasets is a collection of multiple Arabic question answering datasets, including Arabic-SQuAD, AAQAD, TyDi QA, MLQA, and ARCD. It contains a total of 89,927 question-answer pairs, 35,021 paragraphs, and 19,038 articles. The dataset is provided in the SQuAD format.
"""

_URLs = {
    "train": "",
    "dev": "",
}

class ArabicQADatasetsConfig(datasets.BuilderConfig):
    """BuilderConfig for Arabic-QA-Datasets."""

    def __init__(self, **kwargs):
        """BuilderConfig for Arabic-QA-Datasets.

        Args:
          **kwargs: keyword arguments forwarded to super.
        """
        super(ArabicQADatasetsConfig, self).__init__(**kwargs)

class ArabicQADatasets(datasets.GeneratorBasedBuilder):
    """Arabic-QA-Datasets: A collection of Arabic question answering datasets."""

    BUILDER_CONFIGS = [
        ArabicQADatasetsConfig(
            name="plain_text",
            version=datasets.Version("1.0.0", ""),
            description="Plain text",
        )
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "id": datasets.Value("string"),
                    "title": datasets.Value("string"),
                    "context": datasets.Value("string"),
                    "question": datasets.Value("string"),
                    "answers": datasets.features.Sequence(
                        {"text": datasets.Value(
                            "string"), "answer_start": datasets.Value("int32")}
                    ),
                }
            ),
            supervised_keys=None,
            homepage="https://github.com/obada-jaras/Arabic-QA-Datasets",
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        urls_to_download = _URLs
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            datasets.SplitGenerator(name=datasets.Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            datasets.SplitGenerator(name=datasets.Split.VALIDATION, gen_kwargs={"filepath": downloaded_files["dev"]}),
        ]

    def _generate_examples(self, filepath):
        logging.info("generating examples from = %s", filepath)

        with open(filepath, encoding="utf-8") as f:
            dataset = json.load(f)

            for article in dataset["data"]:
                title = article.get("title", "").strip()
                for paragraph in article["paragraphs"]:
                    context = paragraph["context"].strip()

                    for qa in paragraph["qas"]:
                        question = qa["question"].strip()

                        id_ = qa["id"]

                        answer_starts = [answer["answer_start"] for answer in qa["answers"]]
                        answers = [answer["text"].strip() for answer in qa["answers"]]

                        yield id_, {
                            "title": title,
                            "context": context,
                            "question": question,
                            "id": id_,
                            "answers": {"answer_start": answer_starts, "text": answers},
                        }