class Normalizer:
    max_value_in_data_set = 127
    min_value_in_data_set = 0

    def fit(self, data_set):
        self.max_value_in_data_set = max(data_set)
        self.min_value_in_data_set = min(data_set)

    def normalize(self, number):
        return (number - self.min_value_in_data_set) / (self.max_value_in_data_set - self.min_value_in_data_set)

    def scale_back(self, number):
        return number * (self.max_value_in_data_set - self.min_value_in_data_set) + self.min_value_in_data_set

