import os

import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api, Resource
from joblib import load

load_dotenv()

app = Flask(__name__)
api = Api(app)

TRANSFORMER_PATH = os.environ.get("TRANSFORMER_PATH")
MODEL_PATH = os.environ.get("MODEL_PATH")
# Load pipeline and model using the binary files
transformer = load(TRANSFORMER_PATH)
model = load(MODEL_PATH)

# Function to test if the request contains multiple


class Preds(Resource):
    def post(self):
        json_ = request.json
        # If there are multiple records to be predicted, directly convert the request json file into a pandas dataframe
        entry = pd.DataFrame(json_) if isinstance(json_["age"], list) else pd.DataFrame([json_])
        # Make predictions using data
        prediction = model.predict(transformer.transform(entry))
        res = {"prediction": prediction.tolist()}
        return res, 200  # Send the response object


api.add_resource(Preds, "/predict")

if __name__ == "__main__":
    app.run(debug=True)
