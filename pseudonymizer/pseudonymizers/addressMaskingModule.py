from pseudonymizer.pseudonymizer import Pseudonymizer


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
        # 시군구 단위
        if self.masking_loca == "시군구":
            # 시군구는 앞의 3글자 유지하고 나머지는 마스킹
            return address[:3] + '*' * (len(address)-3)
        # 시군구 읍면동/행정동 단위
        elif self.masking_loca == "읍면동":
            # 주소를 공백을 기준으로 나누어 리스트로 변환
            parts = address.split()
            if len(parts) > 1:
                # 마지막 요소는 마스킹하지 않고 그대로 반환
                return ' '.join(parts[:-1]) + ' ' + parts[-1]
            else:
                return address
        else:
            print("입력받은 {}은(는) 주소가 아닙니다.".format(address))

# 테스트
address_masker = AddressMaskingModule("시군구")
masked_address = address_masker.pseudonymizeData("서울특별시 강남구 역삼동")
print("마스킹된 주소:", masked_address)