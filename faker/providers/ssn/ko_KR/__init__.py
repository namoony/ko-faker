import datetime
import numbers
import zoneinfo

from typing import List, Optional
from zoneinfo import ZoneInfo

from ....typing import SexLiteral
from .. import Provider as SsnProvider


class Provider(SsnProvider):
    ssn_formats = (
        "##0#0#-1######",
        "##0#1#-1######",
        "##0#2#-1######",
        "##0#3#-1######",
        "##0#0#-2######",
        "##0#1#-2######",
        "##0#2#-2######",
    )

    RRN_TYPE = "RRN"  # Resident registration number
    MALE_RRN_PREFIX_CHOICES: List[str] = [
        "9",  # Male, 1800~1899
        "1",  # Male, 1900~1999
        "3",  # Male, 2000~2099
    ]
    FEMALE_RRN_PREFIX_CHOICES: List[str] = [
        "0",  # Female, 1800~1899
        "2",  # Female, 1990~1999
        "4",  # Female, 2000~2099
    ]

    FRN_DRN_TYPE = "FRN_DRRN"  # Foreign registration number(Domestic residence report number)
    MALE_FRN_PREFIX_CHOICES: List[str] = [
        "5",  # Foreigner, Male, 1900~1999
        "7",  # Foreigner, Male, 2000~2099
    ]
    FEMALE_FRN_PREFIX_CHOICES: List[str] = [
        "6",  # Foreigner, Female, 1990~1999
        "8",  # Foreigner, Female, 2000~2099
    ]

    # 'X' is not used in RRN and FRN in Korea.

    def generate_ymd(self) -> str:
        """
        Generate a date of birth in "YYMMDD" format.
        :return: Formatted number of "YYMMDD"(ex: 20240101)
        """
        year = self.generator.random.randint(0, 99)
        month = self.generator.random.randint(1, 12)
        day = self.generator.random.randint(1, 31)
        return f"{year:02d}{month:02d}{day:02d}"

    def rrn(self, gender: Optional[SexLiteral] = None) -> str:
        """
        Generate a Resident Registration Number(RRN).
        A Korean resident registration number is a 13-digit number with dash.
        The prefix portion(6 digits) is date of birth in YYMMDD.
        The postfix portion(7 digits) is the combined format number.
        (Note. This function is ignoring verification number of last part in postfix portion's.)
        :return: Formatted number of "######-#######"
        """
        # prefix portion(6 digits)
        prefix = self.generate_ymd()

        # postfix portion(7 digits)
        # (1) The century of birth with sex.
        if gender is not None:
            if gender == "M":
                choices = self.MALE_RRN_PREFIX_CHOICES
            elif gender == "F":
                choices = self.FEMALE_RRN_PREFIX_CHOICES
        else:
            choices = self.MALE_RRN_PREFIX_CHOICES + self.FEMALE_RRN_PREFIX_CHOICES
        cob_sex = self.generator.random.choice(choices)
        # (2~7) 5 Random number + 1 verification number(Ignoring verification).
        # Before 2020-10, 4 Regional Unique Number + 1 Order of registration + 1 verification number.
        # But after are not.
        random5 = self.generator.random.randint(0, 99999)
        # verification number
        vf_num = self.generator.random.randint(0, 9)

        rrn = f"{prefix}-{cob_sex:1}{random5:05d}{vf_num:01d}"
        return rrn

    def frn(self, gender: Optional[SexLiteral] = None) -> str:
        """
        Generate a Foreign Registration Number(FRN).  
        This includes Domestic Residence Report Number(DRRN).
        A Korean foreign registration number is a 13-digit number with dash.
        The prefix portion(6 digits) is date of birth in YYMMDD.
        The postfix portion(7 digits) is the combined format number.
        (Note. This function is ignoring the postfix portion's verification number.)
        :return: Formatted number of "######-#######"
        """
        # prefix portion(6 digits)
        prefix = self.generate_ymd()

        # postfix portion(7 digits)
        # (1) The century of birth with sex.
        if gender is not None:
            if gender == "M":
                choices = self.MALE_FRN_PREFIX_CHOICES
            elif gender == "F":
                choices = self.FEMALE_FRN_PREFIX_CHOICES
        else:
            choices = self.MALE_FRN_PREFIX_CHOICES + self.FEMALE_FRN_PREFIX_CHOICES
        cob_sex = self.generator.random.choice(choices)
        # (2~7) 5 Registration authority's serial number + 1 verification number.
        random5 = self.generator.random.randint(0, 99999)
        # verification number
        vf_num = self.generator.random.randint(0, 9)

        frn = f"{prefix}-{cob_sex:1}{random5:05d}{vf_num:01d}"
        return frn

    def ssn(self, gender: Optional[SexLiteral] = None, foreigner: Optional[bool] = None) -> str:
        """
        Generate a Korean SSN(Commonly called RRN including FRN and DRRN).
        A Korean SSN is 13-digit number with dash.
        The prefix portion(6 digits) is date of birth in YYMMDD.
        The postfix portion(7 digits) is the combined format number.
        (Note. This function is ignoring the postfix portion's verification number.)
        :param gender: "M": Male, "F": Female, None: both mixed
        :param foreigner: True: only foreigner, False: excluding foreigner, None: both mixed
        :return: Formatted number of "######-#######"
        """
        # prefix portion(6 digits)
        prefix = self.generate_ymd()

        # postfix portion(7 digits)
        # (1) The century of birth with sex.
        if foreigner is None:
            if gender == "M":
                choices = self.MALE_RRN_PREFIX_CHOICES + self.MALE_FRN_PREFIX_CHOICES
            elif gender == "F":
                choices = self.FEMALE_RRN_PREFIX_CHOICES + self.FEMALE_FRN_PREFIX_CHOICES
            else:
                choices = self.MALE_RRN_PREFIX_CHOICES + self.MALE_FRN_PREFIX_CHOICES + self.FEMALE_RRN_PREFIX_CHOICES + self.FEMALE_FRN_PREFIX_CHOICES
        elif foreigner:
            if gender == "M":
                choices = self.MALE_FRN_PREFIX_CHOICES
            elif gender == "F":
                choices = self.FEMALE_FRN_PREFIX_CHOICES
            else:
                choices = self.MALE_FRN_PREFIX_CHOICES + self.FEMALE_FRN_PREFIX_CHOICES
        else:
            if gender == "M":
                choices = self.MALE_RRN_PREFIX_CHOICES
            elif gender == "F":
                choices = self.FEMALE_RRN_PREFIX_CHOICES
            else:
                choices = self.MALE_RRN_PREFIX_CHOICES + self.FEMALE_RRN_PREFIX_CHOICES
        cob_sex = self.generator.random.choice(choices)
        # (2~7) 5 Registration authority's serial number + 1 verification number.
        random5 = self.generator.random.randint(0, 99999)
        # verification number
        vf_num = self.generator.random.randint(0, 9)

        ssn = f"{prefix}-{cob_sex:1}{random5:05d}{vf_num:01d}"
        return ssn
