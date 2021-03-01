
import datetime
import warnings

from bson.code import Code
from bson.objectid import ObjectId
from bson.py3compat import (_unicode,
                            abc,
                            integer_types,
                            string_type)
from bson.raw_bson import RawBSONDocument
from bson.codec_options import CodecOptions
from bson.son import SON
from pymongo import (common,
                     helpers,
                     message)
from pymongo.aggregation import (_CollectionAggregationCommand,
                                 _CollectionRawAggregationCommand)
from pymongo.bulk import BulkOperationBuilder, _Bulk
from pymongo.command_cursor import CommandCursor, RawBatchCommandCursor
from pymongo.common import ORDERED_TYPES
from pymongo.collation import validate_collation_or_none
from pymongo.change_stream import CollectionChangeStream
from pymongo.cursor import Cursor, RawBatchCursor
from pymongo.errors import (BulkWriteError,
                            ConfigurationError,
                            InvalidName,
                            InvalidOperation,
                            OperationFailure)
from pymongo.helpers import (_check_write_command_response,
                             _raise_last_error)
from pymongo.message import _UNICODE_REPLACE_CODEC_OPTIONS
from pymongo.operations import IndexModel
from pymongo.read_preferences import ReadPreference
from pymongo.results import (BulkWriteResult,
                             DeleteResult,
                             InsertOneResult,
                             InsertManyResult,
                             UpdateResult)
from pymongo.write_concern import WriteConcern

_UJOIN = u"%s.%s"
_FIND_AND_MODIFY_DOC_FIELDS = {'value': 1}
_HAYSTACK_MSG = (
    "geoHaystack indexes are deprecated as of MongoDB 4.4."
    " Instead, create a 2d index and use $geoNear or $geoWithin."
    " See https://dochub.mongodb.org/core/4.4-deprecate-geoHaystack")


class ReturnDocument(object):
    """An enum used with
    :meth:`~pymongo.collection.Collection.find_one_and_replace` and
    :meth:`~pymongo.collection.Collection.find_one_and_update`.
    """
    BEFORE = False
    """Return the original document before it was updated/replaced, or
    ``None`` if no document matches the query.
    """
    AFTER = True
    """Return the updated/replaced or inserted document."""


class Collection(object):
    """A Mongo collection.
    """

    def __init__(self, database, name, create=False,
                **kwargs):

        super(Collection, self).__init__()

        if not isinstance(name, string_type):
            raise TypeError("name must be an instance "
                            "of %s" % (string_type.__name__,))

        if not name or ".." in name:
            raise InvalidName("collection names cannot be empty")
        if "$" in name and not (name.startswith("oplog.$main") or
                                name.startswith("$cmd")):
            raise InvalidName("collection names must not "
                              "contain '$': %r" % name)
        if name[0] == "." or name[-1] == ".":
            raise InvalidName("collection names must not start "
                              "or end with '.': %r" % name)
        if "\x00" in name:
            raise InvalidName("collection names must not contain the "
                              "null character")
        collation = validate_collation_or_none(kwargs.pop('collation', None))

        self.__database = database
        self.__name = _unicode(name)
        self.__full_name = _UJOIN % (self.__database.name, self.__name)
        if create or kwargs or collation:
            self.__create(kwargs, collation)

    def __create(self, options, collation, session):
        """
        创建数据库，要写入文件的那种
        """
        pass

    def __getattr__(self, name):

        if name.startswith('_'):
            full_name = _UJOIN % (self.__name, name)
            raise AttributeError(
                "Collection has no attribute %r. To access the %s"
                " collection, use database['%s']." % (
                    name, full_name, full_name))
        return self.__getitem__(name)

    def __getitem__(self, name): # TODO： 这里是要返回一个新的数据库？
        return Collection(self.__database,
                          _UJOIN % (self.__name, name),
                          False,
                          )

    def __repr__(self):
        return "Collection(%r, %r)" % (self.__database, self.__name)

    def __eq__(self, other):
        if isinstance(other, Collection):
            return (self.__database == other.database and
                    self.__name == other.name)
        return NotImplemented

    def __ne__(self, other):
        return not self == other

    @property
    def full_name(self):
        """The full name of this :class:`Collection`.

        The full name is of the form `database_name.collection_name`.
        """
        return self.__full_name

    @property
    def name(self):
        """The name of this :class:`Collection`."""
        return self.__name

    @property
    def database(self):
        return self.__database

    def _insert_one(
            self, doc):
        """Internal helper for inserting a single document."""
        # 对我来说插入这个功能可能用不上， 想要完全不改代码就替换掉mongo几乎是不可能的了，再怎么，像什么inset之类的操作，都是需要改变的
        if not isinstance(doc, RawBSONDocument):
            return doc.get('_id')

    def _insert(self, docs, ordered=True, check_keys=True,
                manipulate=False, write_concern=None, op_id=None,
                bypass_doc_val=False, session=None):
        """Internal insert helper."""
        if isinstance(docs, abc.Mapping):
            return self._insert_one(
                docs)

        ids = []

        if manipulate:
            def gen():
                """Generator that applies SON manipulators to each document
                and adds _id if necessary.
                """
                _db = self.__database
                for doc in docs:
                    # Apply user-configured SON manipulators. This order of
                    # operations is required for backwards compatibility,
                    # see PYTHON-709.
                    doc = _db._apply_incoming_manipulators(doc, self)
                    if not (isinstance(doc, RawBSONDocument) or '_id' in doc):
                        doc['_id'] = ObjectId()

                    doc = _db._apply_incoming_copying_manipulators(doc, self)
                    ids.append(doc['_id'])
                    yield doc
        else:
            def gen():
                """Generator that only tracks existing _ids."""
                for doc in docs:
                    # Don't inflate RawBSONDocument by touching fields.
                    if not isinstance(doc, RawBSONDocument):
                        ids.append(doc.get('_id'))
                    yield doc

        write_concern = write_concern or self._write_concern_for(session)
        blk = _Bulk(self, ordered, bypass_doc_val)
        blk.ops = [(message._INSERT, doc) for doc in gen()]
        try:
            blk.execute(write_concern, session=session)
        except BulkWriteError as bwe:
            _raise_last_error(bwe.details)
        return ids

    def insert_one(self, document):

        common.validate_is_document_type("document", document)
        if not (isinstance(document, RawBSONDocument) or "_id" in document):
            document["_id"] = ObjectId()

    def insert_many(self, documents, ordered=True):

        if not isinstance(documents, abc.Iterable) or not documents:
            raise TypeError("documents must be a non-empty list")
        inserted_ids = []
        def gen():
            """A generator that validates documents and handles _ids."""
            for document in documents:
                common.validate_is_document_type("document", document)
                if not isinstance(document, RawBSONDocument):
                    if "_id" not in document:
                        document["_id"] = ObjectId()
                    inserted_ids.append(document["_id"])
                yield (message._INSERT, document)

        return InsertManyResult(inserted_ids)

    def _update(self,data, collation=None, array_filters=None,
                hint=None):
        """Internal update / replace helper."""
        if collation is not None:
            pass
        if array_filters is not None:
            pass
        if hint is not None:
            pass

        return data


    def replace_one(self, filter):
        common.validate_is_mapping("filter", filter)

    def update_one(self, filter, update, upsert=False):
        pass

    def update_many(self, filter, update, upsert=False, array_filters=None,
                    bypass_document_validation=False, collation=None,
                    hint=None, session=None):
        pass

    def drop(self, session=None):

        dbo = self.__database.client.get_database(
            self.__database.name,
            self.codec_options,
            self.read_preference,
            self.write_concern,
            self.read_concern)
        dbo.drop_collection(self.__name, session=session)

    def _delete(
            self, sock_info, criteria, multi,
            write_concern=None):
        """Internal delete helper."""
        common.validate_is_mapping("filter", criteria)
        write_concern = write_concern or self.write_concern
        acknowledged = write_concern.acknowledged
        delete_doc = SON([('q', criteria),
                          ('limit', int(not multi))])

        return result

    def delete_one(self, filter, collation=None, hint=None, session=None):

        write_concern = self._write_concern_for(session)
        return

    def delete_many(self, filter, collation=None, hint=None, session=None):

        write_concern = self._write_concern_for(session)
        return

    def find_one(self, filter=None, *args, **kwargs):

        if (filter is not None and not
        isinstance(filter, abc.Mapping)):
            filter = {"_id": filter}

        cursor = self.find(filter, *args, **kwargs)
        for result in cursor.limit(-1):
            return result
        return None

    def find(self, *args, **kwargs):
        return Cursor(self, *args, **kwargs)

    def _count(self, cmd, collation=None, session=None):
        return

    def count(self, filter=None, session=None, **kwargs):


        if filter is not None:
            if "query" in kwargs:
                raise ConfigurationError("can't pass both filter and query")
            kwargs["query"] = filter
        if "hint" in kwargs and not isinstance(kwargs["hint"], string_type):
            kwargs["hint"] = helpers._index_document(kwargs["hint"])
        collation = validate_collation_or_none(kwargs.pop('collation', None))

        return self._count(collation)

    def rename(self, new_name):
        pass

    def distinct(self, key, filter=None, session=None, **kwargs):
        pass

    def find_one_and_delete(self, filter,
                            projection=None, sort=None, hint=None,
                            session=None, **kwargs):

        kwargs['remove'] = True
        return self.__find_and_modify(filter, projection, sort,
                                      hint=hint, session=session, **kwargs)

    def find_one_and_replace(self, filter, replacement,
                             projection=None, sort=None, upsert=False,
                             return_document=ReturnDocument.BEFORE,
                             hint=None, session=None, **kwargs):
        return self.__find_and_modify(filter, projection,
                                      sort, upsert, return_document,
                                      hint=hint, session=session, **kwargs)

    def find_one_and_update(self, filter, update,
                            projection=None, sort=None, upsert=False,
                            return_document=ReturnDocument.BEFORE,
                            array_filters=None, hint=None, session=None,
                            **kwargs):

        common.validate_ok_for_update(update)
        common.validate_list_or_none('array_filters', array_filters)
        kwargs['update'] = update
        return self.__find_and_modify(filter, projection,
                                      sort, upsert, return_document,
                                      array_filters, hint=hint,
                                      session=session, **kwargs)

    def save(self, to_save, manipulate=True, check_keys=True, **kwargs):

        warnings.warn("save is deprecated. Use insert_one or replace_one "
                      "instead", DeprecationWarning, stacklevel=2)
        common.validate_is_document_type("to_save", to_save)

        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)

        if not (isinstance(to_save, RawBSONDocument) or "_id" in to_save):
            return self._insert(
                to_save, True, check_keys, manipulate, write_concern)
        else:
            self._update_retryable(
                {"_id": to_save["_id"]}, to_save, True,
                check_keys, False, manipulate, write_concern,
                collation=collation)
            return to_save.get("_id")

    def insert(self, doc_or_docs, manipulate=True,
               check_keys=True, continue_on_error=False, **kwargs):

        warnings.warn("insert is deprecated. Use insert_one or insert_many "
                      "instead.", DeprecationWarning, stacklevel=2)
        write_concern = None
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._insert(doc_or_docs, not continue_on_error,
                            check_keys, manipulate, write_concern)

    def update(self, spec, document, upsert=False, manipulate=False,
               multi=False, check_keys=True, **kwargs):

        warnings.warn("update is deprecated. Use replace_one, update_one or "
                      "update_many instead.", DeprecationWarning, stacklevel=2)
        common.validate_is_mapping("spec", spec)
        common.validate_is_mapping("document", document)
        if document:

            first = next(iter(document))
            if first.startswith('$'):
                check_keys = False

        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._update_retryable(
            spec, document, upsert, check_keys, multi, manipulate,
            write_concern, collation=collation)

    def remove(self, spec_or_id=None, multi=True, **kwargs):

        warnings.warn("remove is deprecated. Use delete_one or delete_many "
                      "instead.", DeprecationWarning, stacklevel=2)
        if spec_or_id is None:
            spec_or_id = {}
        if not isinstance(spec_or_id, abc.Mapping):
            spec_or_id = {"_id": spec_or_id}
        write_concern = None
        collation = validate_collation_or_none(kwargs.pop('collation', None))
        if kwargs:
            write_concern = WriteConcern(**kwargs)
        return self._delete_retryable(
            spec_or_id, multi, write_concern, collation=collation)

    def find_and_modify(self, query={}, update=None,
                        upsert=False, sort=None, full_response=False,
                        manipulate=False, **kwargs):
        warnings.warn("find_and_modify is deprecated, use find_one_and_delete"
                      ", find_one_and_replace, or find_one_and_update instead",
                      DeprecationWarning, stacklevel=2)

        if not update and not kwargs.get('remove', None):
            raise ValueError("Must either update or remove")

        if update and kwargs.get('remove', None):
            raise ValueError("Can't do both update and remove")

        # No need to include empty args
        if query:
            kwargs['query'] = query
        if update:
            kwargs['update'] = update
        if upsert:
            kwargs['upsert'] = upsert
        if sort:
            # Accept a list of tuples to match Cursor's sort parameter.
            if isinstance(sort, list):
                kwargs['sort'] = helpers._index_document(sort)
            # Accept OrderedDict, SON, and dict with len == 1 so we
            # don't break existing code already using find_and_modify.
            elif (isinstance(sort, ORDERED_TYPES) or
                  isinstance(sort, dict) and len(sort) == 1):
                warnings.warn("Passing mapping types for `sort` is deprecated,"
                              " use a list of (key, direction) pairs instead",
                              DeprecationWarning, stacklevel=2)
                kwargs['sort'] = sort
            else:
                raise TypeError("sort must be a list of (key, direction) "
                                "pairs, a dict of len 1, or an instance of "
                                "SON or OrderedDict")

        fields = kwargs.pop("fields", None)
        if fields is not None:
            kwargs["fields"] = helpers._fields_list_to_dict(fields, "fields")

        collation = validate_collation_or_none(kwargs.pop('collation', None))

        cmd = SON([("findAndModify", self.__name)])
        cmd.update(kwargs)

        write_concern = self._write_concern_for_cmd(cmd, None)

        def _find_and_modify(session, sock_info, retryable_write):
            if (sock_info.max_wire_version >= 4 and
                    not write_concern.is_server_default):
                cmd['writeConcern'] = write_concern.document
            result = self._command(
                sock_info, cmd, read_preference=ReadPreference.PRIMARY,
                collation=collation,
                session=session, retryable_write=retryable_write,
                user_fields=_FIND_AND_MODIFY_DOC_FIELDS)

            _check_write_command_response(result)
            return result

        out = self.__database.client._retryable_write(
            write_concern.acknowledged, _find_and_modify, None)

        if full_response:
            return out
        else:
            document = out.get('value')
            if manipulate:
                document = self.__database._fix_outgoing(document, self)
            return document

    def __iter__(self):
        return self

    def __next__(self):
        raise TypeError("'Collection' object is not iterable")

    next = __next__

    def __call__(self, *args, **kwargs):
        """This is only here so that some API misusages are easier to debug.
        """
        if "." not in self.__name:
            raise TypeError("'Collection' object is not callable. If you "
                            "meant to call the '%s' method on a 'Database' "
                            "object it is failing because no such method "
                            "exists." %
                            self.__name)
        raise TypeError("'Collection' object is not callable. If you meant to "
                        "call the '%s' method on a 'Collection' object it is "
                        "failing because no such method exists." %
                        self.__name.split(".")[-1])
