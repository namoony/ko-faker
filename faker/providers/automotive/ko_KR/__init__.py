from string import digits

from .. import Provider as AutomotiveProvider


class Provider(AutomotiveProvider):
    """Implement automotive provider for ``ko_KR`` locale.

    Sources:

    license_plate
    - https://www.law.go.kr/LSW//admRulLsInfoP.do?admRulId=37243&efYd=0
    - https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EC%B0%A8%EB%9F%89_%EB%B2%88%ED%98%B8%ED%8C%90
    - https://namu.wiki/w/%EC%B0%A8%EB%9F%89%20%EB%B2%88%ED%98%B8%ED%8C%90/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD

    driver_license
    - https://namu.wiki/w/%EC%9A%B4%EC%A0%84%EB%A9%B4%ED%97%88%EC%A6%9D
    """

    license_formats = (
        "##?####",
        # after 2019-09
        "###?####",
    )

    def license_plate(self) -> str:
        """Generate a license plate."""
        # 자동차 등록번호판 등의 기준에 관한 고시
        # - [시행 2024. 1. 1.] [국토교통부고시 제2023-954호, 2023. 12. 28., 일부개정]
        # - 제 5조, 제 6조
        mid_chars = "가나다라마거너더러머버서어저고노도로모보소오조구누두루무부수우주바사아자배허하호"
        # - 기타
        #   외교 영사 준외 준영 국기 협정 대표
        #   서울 부산 대구 인천 광주 대전 울산 세종 경기 강원 충북 충남 전북 전남 경북 경남 제주
        full_part = self.bothify(self.random_element(self.license_formats), letters=mid_chars)
        return full_part

    def drivers_license(self) -> str:
        """
        Generate a driver license.\n
        # "AA-BB-CCCCCC-DE" format\n
        # AA: 2 digits, locale code\n
        # BB: 2 digits, year\n
        # CCCCCC: 6 digits, serial number\n
        # D: 1 digit, checksum digit\n
        # E: 1 digit, a round of issuance\n
        """
        # "AA-BB-CCCCCC-DE" format
        # AA: 2 digits, locale code
        # BB: 2 digits, year
        # CCCCCC: 6 digits, serial number
        # D: 1 digit, checksum digit
        # E: 1 digit, a round of issuance
        locale_code = self.random_int(11, 28)
        return f"{locale_code:2d}-{self.random_int(0, 99):02d}-{self.random_int(0, 999999):06d}-{self.random_int(0, 9)}{self.random_int(0, 9)}"
