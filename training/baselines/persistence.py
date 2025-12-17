import numpy as np

class PersistenceModel:
    def predict(self, history, horizon):
        last_value = history[-1]
        return np.repeat(last_value, horizon)
