class LeaseFormatterService:
    @staticmethod
    def format_lease_for_android(lease):
        issues = []
        if lease.get("ArePetsProhibited", False):
            issues.append(
                {
                    "Title": "Pet Policies",
                    "Issue": "Pets prohibited",
                    "Description": "Landlords are only able to prohibit pets if they case significant property damage",
                }
            )

        if lease.get("AreGuestsProhibited", False):
            issues.append(
                {
                    "Title": "Guest Policies",
                    "Issue": "Guests prohibited",
                    "Description": "Landlords are only able to prohibit guests in common areas for specific reasons",
                }
            )

        amounts = lease.get("Amounts", None)
        dates = lease.get("Dates", None)
        locations = lease.get("Locations", None)
        orgs = lease.get("Organizations", None)

        return {
            "Id": lease["_id"],
            "Thumbnail": lease.get("ThumbnailString", ""),
            "Status": lease["Status"],
            "Issues": issues,
            "Dates": " - ".join(dates[:2]) if dates else "",
            "Address": locations[0] if locations else "",
            "Rent": amounts[0] if amounts else "",
            "Title": orgs[0] if orgs else "",
        }
