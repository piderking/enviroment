from config import logger, get_config
from typing import List, Optional
import os
CSV_PATH = get_config('csv')


type Item = (str, str)  # type: ignore
headers = ["id", "content"]
item_types = [str, str]
# id, content --> string


class MemoryBank():

    data: (str, str)

    @classmethod
    def verify_type_signature(cls, item: Item) -> bool:

        if not len(item_types) == len(item):
            return False

        return all([type(tm) is tp for tp, tm in zip(item_types, item)])

    @classmethod
    def data_from_csv(cls, fileName: str) -> List[Item]:
        data_path = os.path.join(get_config("csv"), f"{fileName}.csv")
        if not os.path.exists(data_path):
            logger.warn(f"Data File for reading: {data_path} is empty...")
            return []

        final = []
        with open(data_path, "r") as file:
            delim = get("csv-delimiter")
            for idx, line in enumerate(file):
                values = [typ(val) for val, typ in zip(
                    line.split(delim), item_types)]
                # Add to Final Value List
                final.append(values)

        return final

    def write_csv(self, fileName: str, output_full=False) -> Optional[str]:
        data_path = os.path.join(get_config("csv"), f"{fileName}.csv")
        if not os.path.exists(data_path):
            logger.error(f"Data File for writing: {data_path} is empty...")
            raise FileNotFoundError(
                f"Data File for writing: {data_path} is empty...")

        with open(data_path, "w") as file:
            delim = get("csv-delimiter")

            header = delim.join(headers)
            content = "\n".join(
                [delim.join([str(item) for item in d]) for d in data])

            file.write(header + "\n" + content)

            if output_full:
                return header + "\n" + content

            return

    def __init__(self, data: List[Item]):
        # parse CSV

        self.data = self.data_from_csv("data")
        self.data.extend([d for d in data if verify_type_signature(d)])
