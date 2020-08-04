ISSUES = {
    "Pets": {
        "Issue": "Landlord does not allow pets",
        "Title": "Pet Policy",
        "Description": "Landlords are only able to prohibit pets if they cause significant property damage",
        "IsWarning": False,
    },
    "Guests": {
        "Issue": "Landlord does not allow guests to stay overnight",
        "Title": "Guest Policy",
        "Description": "Landlords are not legally allowed to prevent guests from staying overnight",
        "IsWarning": False,
    },
    "SecurityDeposit": {
        "Issue": "A security deposit is required",
        "Title": "Security Deposit Requried",
        "Description": "A landlord cannot ask a tenant for a Security Deposit",
        "IsWarning": False,
    },
    "AverageRent": {
        "Issue": "Your rent seems higher than average for this property",
        "Title": "Rent Higher Than Average",
        "Description": "Your rent for this property seems higher than average based on our historical records",
        "IsWarning": True,
    },
    "RentDeposit": {
        "Issue": "A rent deposit is required",
        "Title": "Rent Deposit Required",
        "Description": "While a landlord has the right to ask for a rent deposit, it cannot be for more than one month's worth of rent",
        "IsWarning": True,
    },
    "KeyDeposit": {
        "Issue": "A key deposit is required",
        "Title": "Key Deposit Required",
        "Description": "While a landlord has the right to ask for a key deposit, it must be refundable (i.e. returned to you at the end of the lease period)",
        "IsWarning": True,
    },
}


class LeaseFormatterService:
    @staticmethod
    def format_lease_for_android(lease):
        issues = []
        if lease.get("ArePetsProhibited", False):
            issues.append(ISSUES["Pets"])

        if lease.get("AreGuestsProhibited", False):
            issues.append(ISSUES["Guests"])

        if lease.get("IsRentHigherThanCurrentAverage", False):
            issues.append(ISSUES["AverageRent"])

        if lease.get("IsSecurityDepositRequired", False):
            issues.append(ISSUES["SecurityDeposit"])

        if lease.get("IsRentDepositRequired", False):
            issues.append(ISSUES["RentDeposit"])

        if lease.get("IsKeyDepositRequired", False):
            issues.append(ISSUES["KeyDeposit"])

        amounts = lease.get("Amounts", None)
        dates = lease.get("Dates", None)
        locations = lease.get("Locations", None)
        orgs = lease.get("Organizations", None)

        return {
            "Id": lease["_id"],
            "DocumentName": lease.get("LeaseDocumentName"),
            "Thumbnail": lease.get("ThumbnailString", ""),
            "Status": lease["Status"],
            "Issues": issues,
            "Dates": " - ".join(dates[:2]) if dates else "",
            "Address": locations[0] if locations else "",
            "Rent": amounts[0] if amounts else 0,
            "Title": orgs[0] if orgs else "",
        }
