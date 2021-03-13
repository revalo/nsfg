import pandas as pd

def parse_sps(dat_filename, sps_filename):
    with open(sps_filename) as f:
        spec = f.read()

    column_spec = spec[spec.index("DATA LIST FILE=DATA/"):]
    column_spec = column_spec[:column_spec.index("*")]

    cleaned = ''.join(column_spec.split('\n')[1:]).split()[:-1]
    groups = []

    for i in range(0, len(cleaned)-1, 2):
        groups.append((cleaned[i], cleaned[i+1]))

    headers = []
    widths = []

    for header, cursor in groups:
        headers.append(header)

        if '-' in cursor:
            a, b = (int(x) for x in cursor.split('-'))
            widths.append(b - a + 1)
        else:
            widths.append(1)

    return pd.read_fwf(dat_filename, widths=widths, names=headers)

def load_dataframe(prefix):
    """Load NSFG dataset as a Pandas Dataframe.

    Args:
        prefix(str): Filename prefix, e.g. '2017_2019_FemResp'.
    """
    return parse_sps(prefix + "Data.dat", prefix + "Setup.sps")
