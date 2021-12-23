from textwrap import dedent
from argparse import Namespace
import pytest

from task_Mullagaliev_Erik_inverted_index import (
    InvertedIndex, StruckStoragePolicy, set_default, callback_build,
    build_inverted_index, load_documents, EncodedFileType, FileType,
    DEFAULT_INVERTED_INDEX_STORE_PATH, callback_query, process_queries,
)

DATASET_SMALL_FRATH = "small.sample"
DATASET_TINY_FRATH = "tiny.sample"


def test_can_load_documents_v1():
    # datset example:
    # 123   some words A_word and nothing
    # 2     some word B_word in this dataset
    # 5     famous_phrases to be or not to be
    # 37    all words such as A_word and B_word re here
    documents = load_documents(DATASET_TINY_FRATH)
    etalon_documents = {
        123: "some words A_word and nothing",
        2: "some word B_word in this dataset",
        5: "famous_phrases to be or not to be",
        37: "all words such as A_word and B_word re here",
    }
    assert etalon_documents == documents, (
        "load_documents incorrectly loaded dataset"
    )


def test_can_load_documents_v2(tmpdir):
    dataset_str = dedent("""\
        123	some words A_word and nothing
        2	some word B_word in this dataset
        5	famous_phrases to be or not to be
        37	all words such as A_word and B_word re here
    """)
    dataset_fio = tmpdir.join("tiny.dataset")
    dataset_fio.write(dataset_str)
    documents = load_documents(dataset_fio)
    etalon_documents = {
        123: "some words A_word and nothing",
        2: "some word B_word in this dataset",
        5: "famous_phrases to be or not to be",
        37: "all words such as A_word and B_word re here",
    }
    assert etalon_documents == documents, (
        "load_documents incorrectly loaded dataset"
    )


DATASET_TINY_STR = dedent("""\
    123	some words A_word and nothing
    2	some word B_word in this dataset
    5	famous_phrases to be or not to be
    37	all words such as A_word and B_word re here
""")

@pytest.fixture()
def tiny_dataset_fio(tmpdir):
    dataset_fio = tmpdir.join("dataset.txt")
    dataset_fio.write(DATASET_TINY_STR)
    return dataset_fio


def test_can_load_documents(tiny_dataset_fio):
    documents = load_documents(tiny_dataset_fio)
    etalon_documents = {
        123: "some words A_word and nothing",
        2: "some word B_word in this dataset",
        5: "famous_phrases to be or not to be",
        37: "all words such as A_word and B_word re here",
    }
    assert etalon_documents == documents, (
        "load_documents incorrectly loaded dataset"
    )


@pytest.mark.parametrize(
    "query, etalon_answer",
    [
        pytest.param(["A_word"], ['123', '37']),
        pytest.param(["B_word"], ['2', '37'], id="B_word"),
        pytest.param(["A_word", "B_word"], ['37'], id="both words"),
        pytest.param(["word_does_not_exist"], [''], id="word does not exist"),
    ],
)
def test_query_inverted_index_intersect_results(tiny_dataset_fio, query, etalon_answer):
    documents = load_documents(tiny_dataset_fio)
    tiny_inverted_index = build_inverted_index(documents)
    answer = tiny_inverted_index.query(query)
    assert sorted(answer.split(',')) == sorted(etalon_answer), (
        f"Expected answer is {etalon_answer}, but you got {answer}"
    )


def test_can_load_wikipedia_sample():
    documents = load_documents(DATASET_SMALL_FRATH)
    assert len(documents) == 16, (
        "you incorrectly loaded Wikipedia sample"
    )


@pytest.fixture()
def wikipedia_documents():
    documents = load_documents(DATASET_SMALL_FRATH)
    return documents


@pytest.fixture
def small_wikipedia_documents():
    documents = load_documents(DATASET_SMALL_FRATH)
    return documents


def test_can_build_and_query_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    doc_ids = wikipedia_inverted_index.query(["wikipedia"])
    assert isinstance(doc_ids, str), "inverted index query should return list"


@pytest.fixture
def wikipedia_inverted_index(wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(wikipedia_documents)
    return wikipedia_inverted_index


@pytest.fixture
def small_wikipedia_inverted_index(small_sample_wikipedia_documents):
    wikipedia_inverted_index = build_inverted_index(small_sample_wikipedia_documents)
    return wikipedia_inverted_index

def test_can_dump_and_load_inverted_index(tmpdir, wikipedia_inverted_index):
    index_fio = tmpdir.join("index.dump")
    wikipedia_inverted_index.dump(index_fio)
    loaded_inverted_index = InvertedIndex.load(index_fio)
    assert wikipedia_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


@pytest.mark.parametrize(
    ("filepath",),
    [
        pytest.param(DATASET_SMALL_FRATH, id="small dataset"),
    ]
)

def test_can_dump_and_load_inverted_index_with_array_policy_parametrized(filepath, tmpdir):
    index_fio = tmpdir.join("index.dump")
    documents = load_documents(filepath)
    etalon_inverted_index = build_inverted_index(documents)

    # class StoragePolicy:
    #    @staticmethod
    #    def dump(word_to_docs_mapping, filepath):
    #        pass
    #    
    #    @staticmethod
    #    def load(filepath):
    #        pass

    etalon_inverted_index.dump(index_fio, storage_policy=StruckStoragePolicy)
    loaded_inverted_index = InvertedIndex.load(index_fio, storage_policy=StruckStoragePolicy)
    assert etalon_inverted_index == loaded_inverted_index, (
        "load should return the same inverted index"
    )


def test_encoded_with_cp1251():
    file_type = EncodedFileType("r", encoding="cp1251")

    assert "cp1251" == file_type._encoding

def test_encoded_with_utf8():
    file_type = EncodedFileType("r", encoding="UTF-8")

    assert "UTF-8" == file_type._encoding


def test_callback_query_can_process_from_correct_file(capsys):
    with open("quries_utf8.txt") as query_fin:
        process_queries(
            inverted_index_filepath=DEFAULT_INVERTED_INDEX_STORE_PATH,
            query_file=query_fin,
            query_arg=[['two', 'words']],
        )
        captured = capsys.readouterr()
        assert "load inverted index" not in captured.out
        assert "8439" in captured.out
        assert "843999" not in captured.err


def test_process_queries_can_process_all_queries_from_correct_file(capsys):
    with open("quries_utf8.txt") as query_fin:
        process_queries(
            inverted_index_filepath=DEFAULT_INVERTED_INDEX_STORE_PATH,
            query_file=query_fin,
            query_arg=None,
        )
        captured = capsys.readouterr()
        assert "load inverted index" not in captured.out
        assert "8439" in captured.out
        assert "843999" not in captured.err


def test_missing_module_docstring_from_set_default():
    assert set_default.__doc__ != None

def test_missing_module_docstring_from_callback_build():
    assert callback_build.__doc__ != None

def test_missing_module_docstring_from_callback_query():
    assert callback_query.__doc__ != None

        
