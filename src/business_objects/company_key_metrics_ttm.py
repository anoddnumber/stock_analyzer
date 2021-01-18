class CompanyKeyMetricsTTM:
    EPS = 'earnings'

    available_attributes = frozenset({EPS})

    def __init__(self, mapping, json_data):
        if mapping is not None and json_data is not None:
            for key in mapping:
                if key not in self.available_attributes:
                    print('Key ' + str(key) + ' is not allowed in Key Ratios')
                    continue
                json_data_key = mapping[key]
                try:
                    setattr(self, key, json_data[json_data_key])
                except KeyError:
                    print('Key Ratios: JSON key ' + str(json_data_key) + ' not found in json_data' + str(json_data))

    def get(self, attr):
        return getattr(self, attr)

    def __str__(self):
        res = ''
        for attribute in sorted(self.available_attributes):
            res += attribute + ' : ' + str(getattr(self, attribute, 'missing')) + '\n'
        return res
