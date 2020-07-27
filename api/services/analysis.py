class AnalysisService:
    PETS_PROHIBITED_CLASS = "Pets Prohibited"
    GUESTS_PROHIBITED_CLASS = "Guests Prohibited"

    @staticmethod
    def analyze_classification_results(results):
        pets_prohibited = False
        guests_prohibited = False

        confident_results = (r for r in results if r["Classes"][0]["Score"] > 0.85)

        for result in confident_results:
            classification = result["Classes"][0]["Name"]

            if classification == AnalysisService.PETS_PROHIBITED_CLASS:
                pets_prohibited = True
            elif classification == AnalysisService.GUESTS_PROHIBITED_CLASS:
                guests_prohibited = True

        return {
            "pets_prohibited": pets_prohibited,
            "guests_prohibited": guests_prohibited,
        }
