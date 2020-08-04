class LeaseFormatterService:
    @staticmethod
    def format_lease_for_android(lease):
        issues = []
        if lease.get("ArePetsProhibited", False):
            issues.append(
                {
                    "Title": "Pet Policy",
                    "Issue": "Landlord does not allow pets",
                    "Description": "Landlords are only able to prohibit pets if they cause significant property damage",
                    "IsWarning": False,
                }
            )

        if lease.get("AreGuestsProhibited", False):
            issues.append(
                {
                    "Title": "Guest Policy",
                    "Issue": "Landlord does not allow guests to stay overnight",
                    "Description": "Landlords are not legally allowed to prevent guests from staying overnight",
                    "IsWarning": False,
                }
            )

        if lease.get("IsRentHigherThanCurrentAverage", False):
            issues.append(
                {
                    "Title": "Rent Higher Than Average",
                    "Issue": "Your rent seems higher than average for this property",
                    "Description": "Your rent for this property seems higher than average based on our historical records",
                    "IsWarning": False,
                }
            )

        # TODO: Remove Dummy Warning Issue
        issues.append(
            {
                "Title": "Rent Deposit Required",
                "Issue": "You are being asked for a Rent Deposit",
                "Description": "A Rent Deposit cannot be more than a month's rent",
                "IsWarning": True,
            }
        )

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
