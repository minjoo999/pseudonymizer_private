from pseudonymizer.pseudonymizer import Pseudonymizer
import re

class AddressMaskingModule(Pseudonymizer):
    """주소를 시군구 단위 혹은 읍면동 단위로 마스킹하는 구체 클래스"""
    def __init__(self, masking_type: str):
        """masking_type : government_area (시군구), district (읍면동)"""
        self.masking_type = masking_type

    def pseudonymizeData(self, address):
        """pseudonymizer 클래스 (추상) 기반 구체 메서드"""
        if address:
            if self.masking_type == "government_area":
                self.governmentMasking(address)
            elif self.masking_type == "district":
                self.districtMasking(address)
            else:
                print("masking_type을 정확한 형태로 적어주세요.")
        else:
            pass

    @classmethod
    def governmentMasking(cls, address):
        """시군구 레벨 마스킹 메서드 (예: 서울시 동작구 / 경기도 고양시)"""
        total_pattern = r"(\S+[시도])(\s+\S+[시군구])"

        if re.match(total_pattern, address):
            city_county_pattern = r"(\S+[시도])"
            government_pattern = r"(\b\S+[시군구])"
            result = []

            if re.match(city_county_pattern, address):
                result.append(re.match(city_county_pattern, address).group(0))
                
            if re.search(government_pattern, address):
                result.append(re.search(government_pattern, address).group(0))
            
            # print(result)

            return ' '.join(result)
        else:
            print("데이터가 시도 / 시군구 입력 형식에 맞지 않습니다.")
        

    @classmethod
    def districtMasking(cls, address):
        """읍면동 레벨 마스킹 메서드 (예: 경기도 화성시 반송동 / 서울특별시 동작구 신대방동)"""
        total_pattern = r"(\S+[시도])(\s+\S+[시군구])(\s+\S+[읍면동])"

        if re.match(total_pattern, address):
            city_county_pattern = r"(\S+[시도])"
            government_pattern = r"(\b\S+[시군구])"
            district_pattern = r"(\s+\S+[읍면동])"

            result = []

            if re.match(city_county_pattern, address):
                result.append(re.match(city_county_pattern, address).group(0))
            if re.search(government_pattern, address):
                result.append(re.search(government_pattern, address).group(0))
            if re.search(district_pattern, address):
                result.append(re.search(district_pattern, address).group(0))
        
            return ' '.join(result)
        else:
            print("데이터가 시도 / 시군구 / 읍면동 입력 형식에 맞지 않습니다.")

        
    # 예외처리 (classmethod)
    @classmethod
    def addressdef(cls):
        pass