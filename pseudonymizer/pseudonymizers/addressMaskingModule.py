from pseudonymizer.pseudonymizer import Pseudonymizer
import re

class AddressMaskingModule(Pseudonymizer):
    """지번주소를 시군구 단위 혹은 읍면동 단위로 마스킹하는 구체 클래스"""
    def __init__(self, masking_type: str):
        """masking_type : government_area (시군구), district (읍면동)"""
        self.masking_type = masking_type

    def pseudonymizeData(self, address):
        """pseudonymizer 클래스 (추상) 기반 구체 메서드"""
        if address:
            if self.masking_type == "government_area":
                return self.governmentMasking(address)
            elif self.masking_type == "district":
                return self.districtMasking(address)
            else:
                print("masking_type을 정확한 형태로 적어주세요.")
        else:
            pass

    @classmethod
    def governmentMasking(cls, address):
        """시군구 레벨 마스킹 메서드 (예: 서울시 동작구 / 경기도 고양시)"""
        # total_pattern = r"(\S+[시도])(\s+\S+[시군구])"
        total_pattern = r"(([가-힣]+(시|도)|서울|인천|대구|광주|부산|울산|대전|세종)\s*[가-힣]+(시|군|구))"

        if re.match(total_pattern, address):
            filtered_address = re.match(total_pattern, address).group(0)
            return filtered_address
        else:
            print("데이터가 시도 / 시군구 입력 형식에 맞지 않습니다.")
        

    @classmethod
    def districtMasking(cls, address):
        """읍면동 레벨 마스킹 메서드 (예: 경기도 화성시 반송동 / 서울특별시 동작구 신대방동)
           **중요: 도로명주소 인식 불가 (경기도 고양시 덕양구 행신동 1988 등)
        """
        # total_pattern = r"(\S+[시도])(\s+\S+[시군구])(\s+\S+[읍면동])"
        total_pattern = r"(([가-힣]+(시|도)|서울|인천|대구|광주|부산|울산|대전|세종)\s*[가-힣]+(시|군|구)\s*[가-힣\d,.\s]+(읍|면|동|가|리))"

        if re.match(total_pattern, address):
            filtered_address = re.match(total_pattern, address).group(0)
            return filtered_address
        else:
            print("데이터가 시도 / 시군구 / 읍면동 입력 형식에 맞지 않습니다.")