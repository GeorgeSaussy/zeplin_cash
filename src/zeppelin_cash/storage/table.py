from csv import reader as csv_reader, writer as csv_writer
from _csv import _writer as CsvWriter
from dataclasses import dataclass
from enum import auto, Enum
from typing import List, Optional, TextIO, Union
from uuid import UUID

from zeppelin_cash.errors import Error, ok, Result

# TODO(OMEGA-411): Document and test this file.


class AtomType(Enum):
    Integer = auto()
    Symbol = auto()
    Float = auto()
    Boolean = auto()
    Uuid = auto()
    Null = auto()

    def validate(self, value: Union[int, str, bool, float, UUID]) -> bool:
        if self == AtomType.Integer:
            return isinstance(value, int)
        if self == AtomType.Symbol:
            return isinstance(value, str)
        if self == AtomType.Float:
            return isinstance(value, float)
        if self == AtomType.Boolean:
            return isinstance(value, bool)
        if self == AtomType.Uuid:
            return isinstance(value, UUID)
        assert self == AtomType.Null
        return value is None


class Atom:
    def __init__(self, i: Optional[int] = None,
                 s: Optional[str] = None, f: Optional[float] = None,
                 b: Optional[bool] = None, u: Optional[UUID] = None) -> None:
        """This method should not be called directly by users."""

        non_empty_count = len(list(filter(lambda x: x is not None,
                                          [i, s, f, b, u])))
        assert non_empty_count <= 1

        self.__atom_type = AtomType.Null  # default, empty type
        self.__integer_value: Optional[int] = None
        self.__symbol_value: Optional[str] = None
        self.__float_value: Optional[float] = None
        self.__boolean_value: Optional[bool] = None
        self.__uuid_value: Optional[UUID] = None
        if non_empty_count == 0:
            return
        if i is not None:
            self.__atom_type = AtomType.Integer
            self.__integer_value = i
            return
        if s is not None:
            self.__atom_type = AtomType.Symbol
            self.__symbol_value = s
            return
        if f is not None:
            self.__atom_type = AtomType.Float
            self.__float_value = f
            return
        if b is not None:
            self.__atom_type = AtomType.Boolean
            self.__boolean_value = b
            return
        if u is not None:
            self.__atom_type = AtomType.Uuid
            self.__uuid_value = u
            return

    @classmethod
    def integer(cls, i: int) -> "Atom":
        return Atom(i=i)

    @classmethod
    def symbol(cls, s: str) -> "Atom":
        return Atom(s=s)

    @classmethod
    def float(cls, f: float) -> "Atom":
        return Atom(f=f)

    @classmethod
    def boolean(cls, b: bool) -> "Atom":
        return Atom(b=b)

    @classmethod
    def uuid(cls, u: UUID) -> "Atom":
        return Atom(u=u)

    @classmethod
    def null(cls) -> "Atom":
        return Atom()

    @classmethod
    def parse(cls, my_type: AtomType, s: str) -> Result["Atom"]:
        # TODO(OMEGA-411): This should implement error handling.

        assert my_type != AtomType.Null
        if my_type == AtomType.Integer:
            return Result(ok=Atom.integer(i=int(s)))
        if my_type == AtomType.Symbol:
            return Result(ok=Atom.symbol(s=s))
        if my_type == AtomType.Float:
            return Result(ok=Atom.float(f=float(s)))
        if my_type == AtomType.Boolean:
            return Result(ok=Atom.boolean(b=bool(s)))
        if my_type == AtomType.Uuid:
            return Result(ok=Atom.uuid(u=UUID(s)))
        if my_type == AtomType.Null:
            if s != "":
                return Result(
                    err=Error("null atom cannot be represented by non-empty string"))
            return Result(ok=Atom.null())
        # This should never happen.
        assert False

    def atom_type(self) -> AtomType:
        return self.__atom_type


@dataclass
class ColumnSchema:
    column_name: str
    column_type: AtomType


class Row:

    def __init__(self, values: Optional[List[Atom]] = None) -> None:
        self.__values = [] if values is None else values

    def values(self) -> List[Atom]:
        return self.__values

    def add_value(self, value: Atom) -> None:
        self.__values.append(value)


@dataclass
class TableSchema:
    name: str
    id_field_name: str
    data_fields: List[ColumnSchema]

    def validate(self, row: Row) -> bool:
        """Validate that a row matches the schema."""
        values = row.values()
        if len(values) != len(self.data_fields):
            return False
        for k in range(len(values)):
            value = values[k]
            column_type = self.data_fields[k].column_type
            if column_type != value.atom_type():
                return False
        return True

    def column_names(self) -> List[str]:
        return [column.column_name for column in self.data_fields]

    def column_types(self) -> List[AtomType]:
        return [column.column_type for column in self.data_fields]


class Table:

    def __init__(self, schema: TableSchema) -> None:
        self.__schema = schema
        self.__rows: List[Row] = []

    def add_row(self, row: Row) -> Error:
        if not self.__schema.validate(row):
            return Error("row is not valid for given table's schema")
        self.__rows.append(row)
        return ok()

    def get_row(self, column_name: str,
                match_value: Atom) -> Result[List[Row]]:
        pass


class TableReader:

    def __init__(self, file_name: str, expected_schema: TableSchema) -> None:
        self.__file_name = file_name
        self.__schema = expected_schema

    def read(self) -> Result[Table]:
        # TODO(OMEGA-411): This should catch the exceptions raised in file IO
        # fails.
        table = Table(self.__schema)
        with open(self.__file_name, newline="\n") as csvfile:
            reader = csv_reader(csvfile, delimiter=",", quotechar="\"")
            on_first_row = False
            column_types = self.__schema.column_types()
            for row in reader:
                if on_first_row:
                    column_names = self.__schema.column_names()
                    if len(row) != len(column_names):
                        return Result(
                            err=Error("the file does not have the correct number of columns"))
                    for k in range(len(column_names)):
                        if row[k] != column_names[k]:
                            return Result(err=Error(
                                f"the column name {row[k]} does not match the expected name {column_names[k]}"))
                    on_first_row = False
                    continue
                if len(row) != len(column_types):
                    return Result(
                        err=Error(f"the number of rows does not match the expected schema"))
                my_row = Row()
                for k in range(len(column_types)):
                    result = Atom.parse(column_types[k], row[k])
                    if not result.is_ok():
                        return Result(
                            err=Error(f"a data value could not be parsed"))
                    atom = result.ok()
                    my_row.add_value(atom)
                err = table.add_row(my_row)
                if not err.is_ok():
                    return Result(err=err)
            return Result(ok=table)


class TableWritter:
    """Note: This implementation is not thread safe."""

    def __init__(self, file_name: str, schema: TableSchema,
                 append_existing: bool = False) -> None:
        self.__file_name = file_name
        self.__schema = schema
        self.__create_table = not append_existing
        self.__fd: Optional[TextIO] = None
        self.__csv_writer: Optional[CsvWriter] = None
        self.__closed = False

    def add_row(self, row: Row) -> Error:
        if not self.__schema.validate(row):
            return Error("row is not valid for given table's schema")
        if self.__fd is None:
            if self.__closed:
                return Error("cannot reuse close table writer")
            if self.__create_table:
                self.__fd = open(self.__file_name, "w")
                self.__csv_writer = csv_writer(self.__fd)
                self.__csv_writer.writerow([self.__schema.column_names()])
            else:
                # TODO(OMEGA-411): An existing CSV should be validated before rows
                # can be appended.
                self.__fd = open(self.__file_name, "a")
                self.__csv_writer = csv_writer(self.__fd)
        assert self.__csv_writer is not None
        self.__csv_writer.writerow(row.values())
        return ok()

    def close(self) -> None:
        assert not self.__closed
        assert self.__fd is not None
        self.__fd.close()
        self.__fd = None
        self.__csv_writer = None
        self.__closed = True
