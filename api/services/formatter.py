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

        return {
            "Id": lease["_id"],
            "Thumbnail": lease["ThumbnailString"],
            "Status": lease["Status"],
            "Issues": issues,
            "Dates": " - ".join(lease.get("dates", [])),
            "Address": lease.get("locations", [""])[0],
            "Rent": lease.get("amounts", [""])[0],
            "Title": lease.get("organizations", [""])[0],
        }
