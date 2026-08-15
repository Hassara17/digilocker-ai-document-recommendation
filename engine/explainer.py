class RecommendationExplainer:

    def explain(self, user, document):

        reasons = []

        if user.student and "Class" in document.document_name:
            reasons.append(
                "You are registered as a student."
            )

        if user.vehicle_owner and document.category == "Driving & Traffic Documents":
            reasons.append(
                "You own a vehicle."
            )

        if user.taxpayer and document.category == "Financial & Tax Documents":
            reasons.append(
                "You are a taxpayer."
            )

        if len(reasons) == 0:
            reasons.append(
                "This document matches your profile."
            )

        return " ".join(reasons)