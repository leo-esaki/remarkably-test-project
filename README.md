# Remarkably test project

## How to test
1. Install pipenv. (Refer to [here](https://pipenv.kennethreitz.org/en/latest/install/).)
2. Run the following commands to get the results

```
$ pipenv shell
$ pipenv install
$ python ./get_kpi.py --kpi_list Occupancy,Light,CO2 --start "2/2/15" --stop "2/3/15"
```
