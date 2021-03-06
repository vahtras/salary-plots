import pytest
import pandas as pd
import numpy as np
"""
Fixture example generated by

    sample = 10
    np.random.seed(0)
    x = np.random.randint(20000, 40000, sample)
    km = np.random.choice(['F', 'M'], sample)
    school = np.random.choice(['A', 'B', 'C'], sample)

"""


@pytest.fixture
def df():
    _df = pd.DataFrame(
        dict(
            kr=[
                22732, 30799, 29845, 39648, 33123, 0, 29225, 34116, 34935,
                35430, 35832
            ],
            km=[
                'F', 'F', 'F', 'M', 'F', 'O', 'M',
                'M', 'F', 'F', 'M'
            ],
            school=['B', 'B', 'B', 'A', 'B', 'D', 'A', 'A', 'B', 'C', 'A'],
        ))
    return _df


@pytest.fixture
def active(df):
    return df[df.kr > 0]


def generate_demo_data():
    sample = 10
    np.random.seed(0)
    data = pd.DataFrame({
        'kr': np.random.randint(20000, 40000, sample),
        'gender': np.random.choice(['F', 'M'], sample),
        'unit': np.random.choice(['A', 'B', 'C'], sample),
        'age': np.random.randint(20, 30, sample),
    })
    print(data)
    data.to_csv('demo_data.csv', index=False)


if __name__ == "__main__":
    generate_demo_data()
