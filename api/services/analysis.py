import re
from operator import itemgetter

_extras = re.compile("[$,\s]")


def _is_rent(amt_str):

    stripped = _extras.sub("", amt_str)

    if stripped.isnumeric():
        int_amt = int(stripped)
        return int_amt > 500 and int_amt <= 3000

    return False


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

        results_in_order = sorted(all_results, key=itemgetter("BeginOffset"))

        amounts = [
            r["Text"]
            for r in results_in_order
            if r["Type"] == "QUANTITY" and r["Score"] > 0.9 and _is_rent(r["Text"])
        ]
        dates = [
            r["Text"]
            for r in results_in_order
            if r["Type"] == "DATE" and r["Score"] > 0.95
        ]
        locations = [
            r["Text"]
            for r in results_in_order
            if r["Type"] == "LOCATION" and r["Score"] > 0.9
        ]
        organizations = [
            r["Text"]
            for r in results_in_order
            if r["Type"] == "ORGANIZATION" and r["Score"] > 0.9
        ]
        people = [
            r["Text"]
            for r in results_in_order
            if r["Type"] == "PERSON" and r["Score"] > 0.9
        ]

        return {
            "Dates": dates,
            "Amounts": amounts,
            "Locations": locations,
            "Organizations": organizations,
            "People": people,
        }
