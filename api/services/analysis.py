class AnalysisService:
    PETS_PROHIBITED_CLASS = "Pets Prohibited"
    GUESTS_PROHIBITED_CLASS = "Guests Prohibited"
    SECURITY_DEPOSIT_REQUIRED = "Security Deposit"
    RENT_DEPOSIT_REQUIRED = "Rent Deposit"
    KEY_DEPOSIT_REQUIRED = "Key Deposit"

    @staticmethod
    def analyze_classification_results(results):
        pets_prohibited = False
        guests_prohibited = False
        security_deposit_required = False
        rent_deposit_required = False
        key_deposit_required = False

        confident_results = (r for r in results if r["Classes"][0]["Score"] > 0.85)

        for result in confident_results:
            classification = result["Classes"][0]["Name"]

            if classification == AnalysisService.PETS_PROHIBITED_CLASS:
                pets_prohibited = True
            elif classification == AnalysisService.GUESTS_PROHIBITED_CLASS:
                guests_prohibited = True
            elif classification == AnalysisService.SECURITY_DEPOSIT_REQUIRED:
                security_deposit_required = True
            elif classification == AnalysisService.RENT_DEPOSIT_REQUIRED:
                rent_deposit_required = True
            elif classification == AnalysisService.KEY_DEPOSIT_REQUIRED:
                key_deposit_required = True

        return {
            "ArePetsProhibited": pets_prohibited,
            "AreGuestsProhibited": guests_prohibited,
            "IsSecurityDepositRequired": security_deposit_required,
            "IsRentDepositRequired": rent_deposit_required,
            "IsKeyDepositRequired": key_deposit_required,
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
