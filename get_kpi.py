import click
import json
import pandas as pd
import requests
from io import StringIO


DATA_API_URL = 'http://lameapi-env.ptqft8mdpd.us-east-2.elasticbeanstalk.com/data'


def get_data(start, stop, kpi_list):
    """
    gets CSV data via API call and filter by date range specified by start & stop args and by kpi_list
    returns the filered data in pandas DataFrame type.
    """
    response = requests.get(DATA_API_URL)
    res_content = json.loads(response.text)
    if not res_content.get('ok') or not res_content.get('data'):
        return pd.DataFrame()
    buffer = StringIO(res_content['data'])
    dframe = pd.read_csv(buffer)
    dframe['date'] = pd.to_datetime(dframe['date'])
    dframe = dframe[dframe['date']>=start][dframe['date']<=stop][kpi_list]
    return dframe


def get_percent_change(series):
    """
    gets the percentage change between the first and the last value of the given pandas series.
    """
    if series.empty:
        return 0
    return series.iloc[-1] / (series.iloc[0] or 1) * 100


def get_mode(series):
    """
    returns the first `mode` of series
    """
    modes = series.mode()
    return modes[0] if modes.count() > 1 else None


def get_results(dframe):
    """
    returns the desired results in python dict data type.
    input data is in pandas DataFrame and each column is list of values in Pandas Series data type for specified kpi list.
    returns the result in the following format:
    {
        "Temperature": {
            "percent_change": 13.5424,
            "last_value": 1.241,
            "first_value": 0.123,
            "lowest": 0.001,
            "highest": 3.612
            "mode": 1,
            "average": 1.234,
            "median": 1.0075
        },
        ...
    }
    """
    results = {}
    for column in dframe.columns:
        series = dframe[column]
        results[column] = {
            'percent_change': get_percent_change(series),
            'first_value': series.iloc[0],
            'last_value': series.iloc[-1],
            'lowest': series.min(),
            'highest': series.max(),
            'mode': get_mode(series),
            'average': series.mean(),
            'median': series.median(),
        }
    return results


@click.command()
@click.option("--start", help="start date of time period")
@click.option("--stop", prompt="stop date of the time period")
@click.option("--kpi_list", prompt="comma delimited list of kpis")
def main(start, stop, kpi_list):
    print(start, stop, kpi_list)
    start = pd.to_datetime(start)
    stop = pd.to_datetime(stop)
    kpi_list = kpi_list.split(',')
    dframe = get_data(start, stop, kpi_list)
    results = {}
    if not dframe.empty:
        results = get_results(dframe)
    print(results)


if __name__ == '__main__':
    main()
