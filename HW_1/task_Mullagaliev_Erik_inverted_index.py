#!/usr/bin/env python3
"""
class InvertedIndex
CLI for Inverted Index
"""
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter, FileType, ArgumentTypeError
from io import TextIOWrapper
import sys
from collections import defaultdict
import struct
from abc import ABC
from abc import abstractmethod

DEFAULT_DATASET_PATH = "small.sample"
DEFAULT_INVERTED_INDEX_STORE_PATH = "inverted.index"

class EncodedFileType(FileType):
    """
    class EncodedFileType -sub class FileType
    * self - FileType
    * string - argument
    """
    def __call__(self, string):
        # the special argument "-" means sys.std{in,out}
        if string == '-':
            if 'r' in self._mode:
                stdin = TextIOWrapper(sys.stdin.buffer, self._encoding)
            return stdin
        # all other arguments are used as file names
        try:
            return open(string, self._mode, self._bufsize, self._encoding,
                        self._errors)
        except OSError as error_list:
            message = f"can't open {string}: {error_list}"
            raise ArgumentTypeError(message)

def set_default(obj):
    """
    set default parser
    * obj - parser
    """
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


class StoragePolicy(ABC):
    """
    class StoragePolicy
    * ABC - parametr
    """
    @staticmethod
    @abstractmethod
    def dump(word_to_docs_mapping, filepath: str) -> None:
        """
        dump for Storage Policy
        * word_to_docs_mapping - word to docs mapping
        * filepath - filepath for file
        """
        return None

    @staticmethod
    @abstractmethod
    def load(filepath: str) -> dict:
        """
        load for Storage Policy
        * filepath - filepath for file
        """
        return None


class StruckStoragePolicy(StoragePolicy):
    """
    sub class StruckStoragePolicy
    for class StoragePolicy
    """
    @staticmethod
    def dump(word_to_docs_mapping, filepath: str) -> None:
        """
        dump for Struck Storage Policy
        * word_to_docs_mapping - word to docs mapping
        * filepath - filepath for file
        """
        open_file = open(filepath, 'wb')

        w2d_mapping_compress = struct.pack('@I', len(word_to_docs_mapping))
        open_file.write(w2d_mapping_compress)
        for word, doc_ids in word_to_docs_mapping.items():
            word = word.encode()
            w2d_mapping_compress = struct.pack('@B', len(word))
            open_file.write(w2d_mapping_compress)

            w2d_mapping_compress = struct.pack('@{}s'.format(len(word)), word)
            open_file.write(w2d_mapping_compress)

            w2d_mapping_compress = struct.pack('@H', len(doc_ids))
            open_file.write(w2d_mapping_compress)

            doc_ids = [int(i) for i in doc_ids]
            w2d_mapping_compress = struct.pack('@{}H'.format(len(doc_ids)), *doc_ids)
            open_file.write(w2d_mapping_compress)

        open_file.close()

    @staticmethod
    def load(filepath: str) -> dict:
        """
        load for Struck Storage Policy
        * filepath - filepath for file
        """
        with open(filepath, "rb") as open_file:
            data = open_file.read(4)
            len_words_to_docs_mapping = struct.unpack('@I', data)[0]

            data_dict = defaultdict(set)
            for _ in range(len_words_to_docs_mapping):

                data = open_file.read(1)
                len_word = struct.unpack('@B', data)[0]

                data = open_file.read(len_word)
                word = struct.unpack('@'+str(len_word)+'s', data)[0]
                word = word.decode()

                data = open_file.read(2)
                len_doc_ids = struct.unpack('@H', data)[0]

                for __ in range(len_doc_ids):
                    data = open_file.read(2)
                    data_dict[word].add(struct.unpack('@H', data)[0])

        return data_dict


class InvertedIndex:
    """
    class InvertedIndex
    Inverted index is a dictionary
    where the keys are words
    """
    def __init__(self, word_to_docs_mapping):
        # make a high-level copyapt
        self.word_to_docs_mapping = {
            word: doc_ids
            for word, doc_ids in word_to_docs_mapping.items()
        }

    def __eq__(self, rhs):
        outcome = (
            self.word_to_docs_mapping == rhs.word_to_docs_mapping
        )
        return outcome

    def query(self, words: list) -> str:
        """Return the list of relevant documents for the given query"""
        assert isinstance(words, list), (
            "query should be provided with a list of words, but user provided:"
            f"{repr(words)}"
        )
        #print(f"query inverted index with request {repr(words)}")

        queries = []

        for word in words:
            try:
                queries.append(self.word_to_docs_mapping[word])
            except KeyError:
                queries.append([])

        union = set(queries[0])


        for query in queries:
            union = union.intersection(query)
        union = list(union)
        union =','.join(map(str, union))

        return union

    def dump(self, filepath: str, storage_policy=None):
        """
        method dump for InvertedIndex
        *self - obj InvertedIndex
        *filepath - filepath to file
        *storage_policy=None - class Storage Policy
        """
        storage_policy = storage_policy or StruckStoragePolicy

        storage_policy.dump(self.word_to_docs_mapping, filepath)

    def load(filepath: str, storage_policy=None):
        """
        method load for InvertedIndex
        *self - obj InvertedIndex
        *filepath - filepath to file
        *storage_policy=None - class Storage Policy
        """
        storage_policy = storage_policy or StruckStoragePolicy

        return InvertedIndex(storage_policy.load(filepath))


def load_documents(filepath: str):
    """
    function load documents for InvertedIndex
    *filepath - filepath to file
    """
    documents = {}
    with open(filepath) as fin:
        for line in fin:
            line = line.rstrip("\n")
            if line:
                doc_id, content = line.split("\t", 1)
                documents[int(doc_id)] = content
    return documents


def build_inverted_index(documents):
    """
    function build inverted index for InvertedIndex
    *documents - load documents
    """
    word_to_docs_mapping = defaultdict(set)
    for doc_id, content in documents.items():
        words = content.split()
        for word in words:
            word_to_docs_mapping[word].add(doc_id)

    inverted_index = InvertedIndex(word_to_docs_mapping)

    for key in inverted_index.word_to_docs_mapping.keys():
        inverted_index.word_to_docs_mapping[key] = set(
            inverted_index.word_to_docs_mapping[key]
        )

    return inverted_index

def callback_build(arguments):
    """
    function callback build for arguments setup parser
    *arguments - load arguments
    """
    documents = load_documents(arguments.dataset)
    inverted_index = build_inverted_index(documents)
    inverted_index.dump(arguments.output)

def callback_query(arguments):
    """
    function callback query for arguments setup parser
    *arguments - load arguments
    """
    return process_queries(
        arguments.inverted_index_filepath,
        arguments.query_file,
        arguments.query_arg
    )

def process_queries(inverted_index_filepath, query_file, query_arg):
    """
    function process queries for all arguments callback query
    *inverted_index_filepath - filepath to inverted index
    *query_file - filepath to arguments
    *query_arg - arguments to consol
    """
    inverted_index = InvertedIndex.load(inverted_index_filepath)
    #print(f"read queries from {query_file}", file=sys.stderr)
    if query_arg:
        for key in query_arg:
            result = inverted_index.query(key)
            print(result)
    else:
        for query in query_file:
            query = query.strip()
            result = inverted_index.query(query.split())
            print(result)


def setup_parser(parser):
    """
    function setup parser arguments for inverted index
    *parser - tool to build, dump, load and query inverted index
    """
    subparsers = parser.add_subparsers(help="choose command")

    build_parser = subparsers.add_parser(
        "build",
        help="build inverted index and save in binary format into hard drive",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    build_parser.add_argument(
        "-d", "--dataset", default=DEFAULT_DATASET_PATH,
        required=True,
        help="path to dataset to load, default path is %(default)s",
    )
    build_parser.add_argument(
        "-o", "--output", default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        required=True,
        help="path to store inverted index in binary format",
    )
    build_parser.set_defaults(callback=callback_build) #callback_build

    query_parser = subparsers.add_parser(
        "query",
        help="query inverted index",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    query_parser.add_argument(
        "--index", default=DEFAULT_INVERTED_INDEX_STORE_PATH,
        dest="inverted_index_filepath",
        help="path to read inverted index in binary format",
    )
    query_file_group = query_parser.add_mutually_exclusive_group(required=True)
    query_file_group.add_argument(
        "--query", dest="query_arg",
        nargs="*",
        action='append',
        help="query to get queries for inverted index",
    )
    query_file_group.add_argument(
        "--query-file-utf8", dest="query_file",
        type=EncodedFileType("r", encoding="utf-8"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="utf-8"),
        help="query to get queries for inverted index",
    )
    query_file_group.add_argument(
        "--query-file-cp1251", dest="query_file",
        type=EncodedFileType("r", encoding="cp1251"),
        default=TextIOWrapper(sys.stdin.buffer, encoding="cp1251"),
        help="query to get queries for inverted index",
    )
    query_parser.set_defaults(callback=callback_query)

if __name__ == "__main__":
    argument_parser = ArgumentParser(
        prog="inverted-index",
        description="Inverted Index Application: build, query, dump and load",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    setup_parser(argument_parser)
    arguments_parser = argument_parser.parse_args()

    arguments_parser.callback(arguments_parser)
