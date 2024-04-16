from pseudonymizer.pseudonymizer import Pseudonymizer
from pseudonymizer.pseudonymizers.addressMaskingModule import AddressMaskingModule
from pseudonymizer.pseudonymizers.nameMasking import NameMaskingModule
from pseudonymizer.pseudonymizers.emailMasking import EmailMaskingModule
from pseudonymizer.pseudonymizers.residentNumMasking import ResidentNumberMaskingModule
from pseudonymizer.pseudonymizers.businessNumMasking import BusinessNumberMaskingModule
from pseudonymizer.pseudonymizers.phoneNumMasking import PhoneNumberMaskingModule

import re
from typing import *

    
class MaskingPseudonymizer(Pseudonymizer):
    def __init__(self, data_type: str, 
                 masking_domain: bool = None, 
                 masking_part: str = None,
                 masking_loca: str = None):
        """data_type은 향후 pseudonymizer.py에서 Pseudonymn 실행 클래스의 
        self._dataframe[column] 개인식별정보의 유형으로 이름, 이메일, 주민등록번호, 사업자등록번호 중 하나로 선언"""
        self.data_type = data_type
        self.email_masker = EmailMaskingModule(masking_domain)
        self.name_masker = NameMaskingModule()
        self.resident_num_masker = ResidentNumberMaskingModule()
        self.business_num_masker = BusinessNumberMaskingModule(masking_part)
        self.phone_num_masker = PhoneNumberMaskingModule()
        self.address = AddressMaskingModule(masking_loca)

    def pseudonymizeData(self, data):
        if self.data_type == "name":
            return self.name_masker.pseudonymizeData(data)
        elif self.data_type == "email":
            return self.email_masker.pseudonymizeData(data)
        elif self.data_type == "resident_number":
            return self.resident_num_masker.pseudonymizeData(data)
        elif self.data_type == "business_number":
            return self.business_num_masker.pseudonymizeData(data)
        elif self.data_type == "phone_number":
            return self.phone_num_masker.pseudonymizeData(data)
        elif self.data_type == "address":
            return self.address.pseudonymizeData(data)
        else:
            raise ValueError("유효한 마스킹 대상 개인식별정보 데이터 타입이 아닙니다.")
            