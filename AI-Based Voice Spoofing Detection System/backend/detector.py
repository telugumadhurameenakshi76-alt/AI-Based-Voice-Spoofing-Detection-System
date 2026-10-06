import os
import joblib
import numpy as np


MODEL_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "models",
    "detector.pkl"
)


class VoiceSpoofDetector:

    def __init__(self):

        self.model = None
        self.model_available = False

        if os.path.exists(MODEL_PATH):

            self.model = joblib.load(MODEL_PATH)
            self.model_available = True

    def predict(self, features):

        if not self.model_available:

            return self.demo_prediction(features)

        features = np.asarray(features).reshape(1, -1)

        prediction = self.model.predict(features)[0]

        probability = None

        if hasattr(self.model, "predict_proba"):

            probabilities = self.model.predict_proba(features)[0]

            probability = float(
                np.max(probabilities)
            )

        label = self.convert_label(prediction)

        if probability is None:

            probability = 0.50

        return {
            "label": label,
            "confidence": probability,
            "model_type": "trained"
        }

    @staticmethod
    def convert_label(prediction):

        value = str(prediction).lower()

        if value in [
            "1",
            "spoof",
            "fake",
            "ai",
            "synthetic",
            "generated",
            "ai-generated"
        ]:

            return "AI-GENERATED"

        return "HUMAN"

    @staticmethod
    def demo_prediction(features):

        """
        Temporary demo prediction.

        This is NOT a scientifically validated
        AI voice spoofing detector.
        """

        score = float(
            np.mean(np.abs(features))
        )

        if score > 5:

            label = "AI-GENERATED"

        else:

            label = "HUMAN"

        confidence = 0.55

        return {
            "label": label,
            "confidence": confidence,
            "model_type": "demo"
        }