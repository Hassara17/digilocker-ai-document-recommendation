class ConstraintEngine:

    """
    Hard eligibility filter for DigiLocker recommendations.

    Constraints are applied BEFORE XGBoost ranking.

    Example:

        age = 17
        document = Driving License

        -> NOT ELIGIBLE

    """

    def __init__(self):
        pass

    # ==========================================================
    # MAIN CHECK
    # ==========================================================

    def is_eligible(
        self,
        user,
        document,
        query=""
    ):

        if document is None:
            return False, "Document information is missing."

        constraints = getattr(
            document,
            "constraints",
            None
        )

        # If your Document object does not yet expose
        # constraints, allow the document.
        if not constraints:
            return True, "No eligibility restrictions."

        # ------------------------------------------------------
        # USER PROFILE
        # ------------------------------------------------------

        age = self._get_user_value(
            user,
            "age"
        )

        student = self._get_user_value(
            user,
            "student",
            False
        )

        vehicle_owner = self._get_user_value(
            user,
            "vehicle_owner",
            False
        )

        taxpayer = self._get_user_value(
            user,
            "taxpayer",
            False
        )

        occupation = self._get_user_value(
            user,
            "occupation",
            ""
        )

        # ======================================================
        # AGE CONSTRAINTS
        # ======================================================

        min_age = constraints.get(
            "min_age"
        )

        max_age = constraints.get(
            "max_age"
        )

        if min_age is not None:

            if age is None:
                return (
                    False,
                    f"Age information is required. "
                    f"Minimum age is {min_age}."
                )

            try:
                age_value = float(age)
                min_age_value = float(min_age)

                if age_value < min_age_value:

                    return (
                        False,
                        f"User age {age_value:g} is below "
                        f"the minimum age of {min_age_value:g}."
                    )

            except (
                ValueError,
                TypeError
            ):

                return (
                    False,
                    "Invalid age information."
                )

        if max_age is not None:

            if age is None:
                return (
                    False,
                    f"Age information is required. "
                    f"Maximum age is {max_age}."
                )

            try:
                age_value = float(age)
                max_age_value = float(max_age)

                if age_value > max_age_value:

                    return (
                        False,
                        f"User age {age_value:g} is above "
                        f"the maximum age of {max_age_value:g}."
                    )

            except (
                ValueError,
                TypeError
            ):

                return (
                    False,
                    "Invalid age information."
                )

        # ======================================================
        # STUDENT CONSTRAINT
        # ======================================================

        requires_student = constraints.get(
            "requires_student"
        )

        if requires_student is True:

            if not bool(student):

                return (
                    False,
                    "This document is intended for students."
                )

        # ======================================================
        # VEHICLE OWNER CONSTRAINT
        # ======================================================

        requires_vehicle_owner = constraints.get(
            "requires_vehicle_owner"
        )

        if requires_vehicle_owner is True:

            if not bool(vehicle_owner):

                return (
                    False,
                    "This document requires vehicle ownership."
                )

        # ======================================================
        # TAXPAYER CONSTRAINT
        # ======================================================

        requires_taxpayer = constraints.get(
            "requires_taxpayer"
        )

        if requires_taxpayer is True:

            if not bool(taxpayer):

                return (
                    False,
                    "This document requires taxpayer status."
                )

        # ======================================================
        # EMPLOYMENT CONSTRAINT
        # ======================================================

        requires_employment = constraints.get(
            "requires_employment"
        )

        if requires_employment is True:

            employment_keywords = [
                "employee",
                "government employee",
                "self employed",
                "business owner"
            ]

            occupation_lower = str(
                occupation
            ).lower().strip()

            employed = any(
                keyword in occupation_lower
                for keyword in employment_keywords
            )

            if not employed:

                return (
                    False,
                    "This document requires employment."
                )

        # ======================================================
        # MINOR / ADULT
        # ======================================================

        adults_only = constraints.get(
            "adults_only"
        )

        if adults_only is True:

            if age is None:

                return (
                    False,
                    "Age is required because this "
                    "document is restricted to adults."
                )

            try:

                if float(age) < 18:

                    return (
                        False,
                        "This document is restricted "
                        "to users aged 18 or above."
                    )

            except (
                ValueError,
                TypeError
            ):

                return (
                    False,
                    "Invalid age information."
                )

        # ======================================================
        # MINOR ELIGIBILITY
        # ======================================================

        minors_allowed = constraints.get(
            "minors_allowed"
        )

        if minors_allowed is False:

            if age is not None:

                try:

                    if float(age) < 18:

                        return (
                            False,
                            "This document is not "
                            "available to minors."
                        )

                except (
                    ValueError,
                    TypeError
                ):

                    return (
                        False,
                        "Invalid age information."
                    )

        # ======================================================
        # QUERY-SPECIFIC RESTRICTIONS
        # ======================================================

        query_lower = (
            str(query)
            .lower()
            .strip()
        )

        restricted_keywords = constraints.get(
            "restricted_query_keywords",
            []
        )

        for keyword in restricted_keywords:

            if str(keyword).lower() in query_lower:

                return (
                    False,
                    f"Document restricted for query "
                    f"condition: {keyword}"
                )

        # ======================================================
        # PASSED
        # ======================================================

        return (
            True,
            "Document satisfies all eligibility constraints."
        )

    # ==========================================================
    # USER VALUE HELPER
    # ==========================================================

    def _get_user_value(
        self,
        user,
        field,
        default=None
    ):

        if user is None:
            return default

        # Object
        if hasattr(user, field):

            value = getattr(
                user,
                field
            )

            if value is not None:
                return value

        # Dictionary
        if isinstance(user, dict):

            return user.get(
                field,
                default
            )

        return default