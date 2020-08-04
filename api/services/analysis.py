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
            "ArePetsProhibited": pets_prohibited,
            "AreGuestsProhibited": guests_prohibited,
        }

    @staticmethod
    def analyze_recognition_results(results):
        all_results = []
        for result in results:
            all_results.extend([e for e in result["Entities"] if e["Score"] > 0.75])

        dates = [r["Text"] for r in all_results if r["Type"] == "DATE"]
        amounts = [
            r["Text"]
            for r in all_results
            if r["Type"] == "QUANTITY"
            and r["Text"].isnumeric()
            and int(r["Text"]) > 500
        ]
        locations = [r["Text"] for r in all_results if r["Type"] == "LOCATION"]
        organizations = [r["Text"] for r in all_results if r["Type"] == "ORGANIZATION"]
        people = [r["Text"] for r in all_results if r["Type"] == "PERSON"]

        return {
            "Dates": dates,
            "Amounts": amounts,
            "Locations": locations,
            "Organizations": organizations,
            "People": people,
        }
