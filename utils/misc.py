
import pandas as pd
from json import loads


def csv_to_dict(csv_file):

    csv_data = pd.read_csv(csv_file).to_json(orient="records")

    return loads(csv_data)
