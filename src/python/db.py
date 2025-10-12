from config import logger, get_config
from typing import List, Optional, Any
import os
import pandas as pd
CSV_PATH = get_config('csv')


headers = ["id", "content"]
item_types = [int, str]
# id, content --> string


class MemoryBank():
    """For Content (NOT EMBEDDINGS (INCLUDES STRINGS))"""
    fileName: str = "data"
    headers: List[str]
    data: (str, str)

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
            self.headers = headers
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

        self.write_csv(output_full=output_full)

    def size(self) -> (int, int):
        return (len(self.data), len(self.data[0]) if len(self.data) > 0 else 0)

    def __repr__(self) -> str:
        # text = "\n".join(["|".join(row) for row in self.data])

        # return f"Size: {str(self.size())}\n\n|{" | ".join(self.headers)}|\n{self.data}"
        return ""


if __name__ == "__main__":

    db = MemoryBank(data=[["1", "world"]])
    print(db.headers)

    print(db.data)
