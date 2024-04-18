from pseudonymizer.pseudonymizer import Pseudonymizer
import re

class AddressMaskingModule(Pseudonymizer):
    """
    주소 마스킹 클래스
    --------------------
    시군구 읍면동 단위의 일부를 복원할 수 없는 비가역성 기법으로 제거하는 구체 클래스
    """
    def __init__(self, masking_loca: str):
        self.masking_loca = masking_loca
        
    def pseudonymizeData(self, address: str):
        """주소의 일부에 대한 마스킹을 수행하는 메서드"""    
        # 주소 정규식 패턴
        # 주소 구조: 시도 / 시군구 / 읍면동 / 슷자 
        # 주소 구조 2 : 시도 / 시군구 / 길 / 숫자
        pattern = r'(\S+[시|도]) | (\s+\S+[시|군|구]) | (\s+\S+[읍|면|동])'
        
        # 입력받은 주소가 정규식 패턴과 일치하는지 확인
        pattern_match = re.match(pattern, address)

        if pattern_match:
            # 시군구 단위로 주소를 마스킹하는 경우
            if self.masking_loca == "시군구":
                # 시군구는 앞의 3글자 유지하고 나머지는 마스킹
                return pattern_match.group(1)[:3] + '*' * (len(pattern_match.group(1))-3) + ' ' + pattern_match.group(2) + ' ' + pattern_match.group(3)
            # 시군구 읍면동/행정동 단위로 주소를 마스킹하는 경우
            elif self.masking_loca == "읍면동":
                # 마지막 요소는 마스킹하지 않고 그대로 반환
                return pattern_match.group(1) + ' ' + pattern_match.group(2) + ' ' + pattern_match.group(3)
        else:
            print("입력받은 {}은(는) 유효한 주소 형식이 아닙니다.".format(address))
