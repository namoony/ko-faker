import random

from datetime import date, timedelta
from typing import Tuple

from .. import Provider as PassportProvider


class Provider(PassportProvider):
    """Implement passport provider for ``ko_KR`` locale.

    Sources:

    - https://www.passport.go.kr/home/kor/contents.do?menuPos=58
    - https://www.passport.go.kr/home/kor/board.do?menuPos=62
    """

    passport_number_formats = (
        # e-Passport before 2021.12.21.(KST), ex: M12345678
        "?########",
        # Next generation e-Passport after 2021.12.21.(KST), ex: M123A4567
        "?###?####",
    )

    def passport_dates(self, birthday: date = date.today()) -> Tuple[str, str, str]:
        """Generates a formatted date of birth, issue, and expiration dates.
        issue and expiration dates are conditioned to fall within U.S. standards of 5 and 10 year expirations


        The ``birthday`` argument is a datetime.date object representing a date of birth.

        Sources:

        -https://travel.state.gov/content/travel/en/passports/passport-help/faqs.html
        """
        birth_date = birthday.strftime("%d ") + birthday.strftime("%b ") + birthday.strftime("%Y")
        today = date.today()
        age = (today - birthday).days // 365
        if age < 16:
            expiry_years = 5
            issue_date = self.generator.date_time_between(today - timedelta(days=expiry_years * 365 - 1), today)
            # Checks if age is less than 5 so issue date is not before birthdate
            if age < 5:
                issue_date = self.generator.date_time_between(birthday, today)
        elif age >= 26:
            expiry_years = 10
            issue_date = self.generator.date_time_between(today - timedelta(days=expiry_years * 365 - 1), today)
        else:
            # In cases between age 16 and 26, the issue date is 5 years ago, but expiry may be in 10 or 5 years
            expiry_years = 5
            issue_date = self.generator.date_time_between(
                today - timedelta(days=expiry_years * 365 - 1), birthday + timedelta(days=16 * 365 - 1)
            )
            # all people over 21 must have been over 16 when they recieved passport or it will be expired otherwise
            if age >= 21:
                issue_date = self.generator.date_time_between(today - timedelta(days=expiry_years * 365 - 1), today)
                expiry_years = 10

        if issue_date.day == 29 and issue_date.month == 2:
            issue_date -= timedelta(days=1)
        expiry_date = issue_date.replace(year=issue_date.year + expiry_years)

        issue_date_format = issue_date.strftime("%d ") + issue_date.strftime("%b ") + issue_date.strftime("%Y")
        expiry_date_format = expiry_date.strftime("%d ") + expiry_date.strftime("%b ") + expiry_date.strftime("%Y")
        return birth_date, issue_date_format, expiry_date_format

    def passport_gender(self, seed: int = 0) -> str:
        """Generates a string representing the gender displayed on a passport

        Sources:

        - https://williamsinstitute.law.ucla.edu/publications/x-gender-markers-passports/
        """
        if seed != 0:
            random.seed(seed)

        genders = ["M", "F", "X"]
        gender = random.choices(genders, weights=[0.493, 0.493, 0.014], k=1)[0]
        return gender

    def passport_full(self) -> str:
        """Generates a formatted sting with US Passport information"""
        dob = self.passport_dob()
        birth_date, issue_date, expiry_date = self.passport_dates(dob)
        gender_g = self.passport_gender()
        given_name, surname = self.passport_owner(gender=gender_g)
        number = self.passport_number()

        full_rep = """{first_name}\n{second_name}\n{gender}\n{dob}\n{issue}\n{expire}\n{num}\n"""
        full_rep = full_rep.format(
            first_name=given_name,
            second_name=surname,
            gender=gender_g,
            dob=birth_date,
            issue=issue_date,
            expire=expiry_date,
            num=number,
        )
        return full_rep
