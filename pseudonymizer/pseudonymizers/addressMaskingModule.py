from pseudonymizer.pseudonymizer import Pseudonymizer
import re

class AddressMaskingModule(Pseudonymizer):
    """주소를 시군구 단위 혹은 읍면동 단위로 마스킹하는 구체 클래스"""
    def __init__(self, masking_type: str):
        """masking_type : government_area (시군구), district (읍면동)"""
        self.masking_type = masking_type

    def pseudonymizeData(self, address):
        """pseudonymizer 클래스 (추상) 기반 구체 메서드"""
        pattern = r"(+S\+S\[시도]) (+S\+S\[시군구]) (+S\+S\[?읍|면|동]?)"
        
        pattern_match = re.match(pattern, address)

        # (시군구) (읍면동) 단위까지는 있어야 실행하도록 조건 설정

        # 특별시 / 광역시 / 특별자치시 (서울특별시, 인천광역시, 세종특별자치시 등)

        # 도 (경기도, 경상남도 등) / 특별자치도 (제주특별자치도 등)

        # 예외처리