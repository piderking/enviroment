from config import logger, get_config
from typing import List, Optional, Any
import os
import pandas as pd
CSV_PATH = get_config('csv')


# id, content --> string


item_types = [int, str]


class MemoryBank():
    """For Content (NOT EMBEDDINGS (INCLUDES STRINGS))"""
    fileName: str = "data"
    headers: List[str]
    data: item_types
    default_headers = ["id", "content"]

    @classmethod
    def verify_type_signature(cls, item: List[Any]) -> item_types:
        if not len(item_types) == len(item):
            return False

        try:

            return [tp(tm) for tp, tm in zip(item_types, item)]
        except ValueError as e:
            logger.error(f"Invalid Types for {e}")

        return []

    def data_from_csv(self) -> List[item_types]:
        data_path = os.path.join(get_config("csv"), f"{self.fileName}.csv")
        logger.debug(f"Reading {data_path}")
        if not os.path.exists(data_path):
            logger.warn(f"Data File for reading: {data_path} is empty...")
            self.headers = self.default_headers
            return []

        final = []

        # ERROR IS OCCURING IN THIS PART
        with open(data_path, "r") as file:
            delim = get_config("csv-delimiter")

            for idx, line in enumerate(file):

                line = line.strip()
                # logger.debug(f"Line#{str(idx)} == {line}")
                # line.removesuffix("\n")

                if idx == 0:
                    self.headers = line.split(delim)
                    logger.debug(f"Adding Header: {line}")
                    continue
                else:
                    splt = line.split(delim)
                    logger.debug(f"Adding Line: #{idx} {line} ")
                    if not len(splt) == len(item_types):
                        logger.error(
                            f"Invalid Size: Line: {len(splt) } != Types: {len(item_types)}; Skipping Row")
                        continue
                    try:
                        out = [typ(val) for val, typ in zip(splt, item_types)]
                        # logger.debug(f"Line Output: {out}")
                        final.append(out)
                    except ValueError as e:
                        logger.error(f"Invalid Types for Line: {idx}. {e}")

                # values = [typ(val) for val, typ in zip(
                #     line.split(delim), item_types)]
                # # Add to Final Value List

        logger.debug("Finished Reading File")
        return final

    def write_csv(self, output_full=False) -> Optional[str]:
        data_path = os.path.join(get_config("csv"), f"{self.fileName}.csv")
        if not os.path.exists(data_path):
            logger.debug(f"Data File: writing new file {data_path}...")

        with open(data_path, "w") as file:
            delim = get_config("csv-delimiter")
            header = delim.join(self.headers)
            content = "\n".join(
                [delim.join([str(item) for item in d]) for d in self.data])

            if len(self.data) > 0:
                file.write(header + "\n" + content)
            else:
                file.write(header)
            if output_full:
                return header + "\n" + content

            return

    def __init__(self, data: Optional[List[item_types]] = None):
        # parse CSV

        logger.debug("Creating MemoryBank Object from CSV File")
        self.data = self.data_from_csv()

        if data is not None:

            logger.debug("Data Given... Validating and Adding")
            self.data.extend([self.verify_type_signature(d) for d in data])

        # write any additional data to csv
        self.update(output_full=True)

    def update(self, output_full=False):

        # Updating Write to File

        self.write_csv(output_full=output_full)

    def __getitem__(self, index: int | List | str) -> item_types | List[item_types]:
        if type(index) is int:

            if len(self.data) == 0:
                raise AttributeError("Empty Data Set...")

            if index >= len(self.data):

                raise AttributeError(
                    "Not a valid point. Index exceeds size of dataset.")

            return self.data[index]

        elif type(index) == list:
            if len(index) == 0:
                logger.warning("Empty List Index Inputed")
                return []
            return [self[idx] for idx in index]

        elif type(index) == str and (index.strip().lower() == "all" or index.strip() == "*"):
            return self.data

        else:
            raise AttributeError(
                f"Data {index} Not Found. [0-{len(self.data)}]")

    def __setitem__(self, index: int | List | str, value: item_types | List[item_types]) -> item_types | List[item_types]:
        if type(index) is int and type(value) is list:

            if len(self.data) == 0:
                raise AttributeError("Empty Data Set...")

            if index >= len(self.data):

                raise AttributeError(
                    "Not a valid point. Index exceeds size of dataset.")

            temp = self.data[index]
            try:
                self.data[index] = self.verify_type_signature(value)

                # retugrn temp
            except ValueError as e:
                raise ValueError(
                    "Value passed doesn't match type signature...")
        elif type(index) == list and type(value) == list and len(value) == len(index) and all([type(val) is list for val in value]):
            for idx, val in zip(index, value):
                self[idx] = val

        elif type(index) == list and type(value) == list and len(value) == len(index):
            raise AttributeError(
                f"Mismatched Lengths (Index: {len(index)}) and (Value: {len(value)})")

        else:
            raise AttributeError(
                f"Data {index} Not Found. [0-{len(self.data)}]")

        # all updates need to get written to the file
        self.update()

    def size(self) -> (int, int):
        return (len(self.data), len(self.data[0]) if len(self.data) > 0 else 0)

    def push(self, value: item_types | List[item_types]):
        if type(value) is not list:
            raise TypeError("List of Values Must be Passed")
        if len(value) > 0 and type(value[0]) is list:
            for val in value:
                self.push(val)
        elif len(value) > 0:
            self.data.append(self.verify_type_signature(value))

        self.update()

    def remove(self, idx: int | List[int]) -> item_types | List[item_types]:

        if type(idx) is int:
            self.data.pop(idx)

        elif type(idx) is list:
            # so we don't cut anything off
            idx = sorted(idx, reverse=True)

            for id in idx:
                self.remove(id)

        self.update()

    def __repr__(self) -> str:
        text = "\n".join(["|" + "|".join([str(col)
                         for col in row]) + "|" for row in self.data])

        return f"Size: {str(self.size())}\n\n|{'|'.join(self.headers)}|\n{text}"


if __name__ == "__main__":

    db = MemoryBank(data=[["1", "world"]])

    db.push(["1", "apple"])

    print(db.data)
