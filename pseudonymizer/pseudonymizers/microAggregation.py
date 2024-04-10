from pseudonymizer.pseudonymizer import Pseudonymizer

class MicroAggregation(Pseudonymizer):
    """특정 그룹의 속성에서 정확한 통계값을 확인하는 가명처리기법 구체 클래스
       클래스를 통해 도출할 부분 통계값: 평균, 총합, 중간값, 최댓값, 최솟값, 최빈값
    """
    def __init__(self, calulate_type, quasi_identifier):
        self.calculate_type = calulate_type
        self.quasi_identifier = quasi_identifier

    def pseudonymizeData(self, data, attribute: str, equivalent_class: dict):
        """Pseudonym 클래스 내에서 클래스 실행하는 메서드"""
        qi_index_list = equivalent_class[self.quasi_identifier]
        attribute_location = data.columns.get_loc(attribute)
        pseudonymize_data = data.iloc[qi_index_list, attribute_location]
    
        if self.calculate_type == "average":
            # 동질집합 특정 준식별자의 속성에 대한 평균값 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.mean()
            return data[attribute]
        elif self.calculate_type == "sum":
            # 동질집합 특정 준식별자의 속성에 대한 총계 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.sum()
            return data[attribute]
        elif self.calculate_type == "median":
            # 동질집합 특정 준식별자의 속성에 대한 중간값 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.median()
            return data[attribute]
        elif self.calculate_type == "max":
            # 동질집합 특정 준식별자의 속성에 대한 최댓값 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.max()
            return data[attribute]
        elif self.calculate_type == "min":
            # 동질집합 특정 준식별자의 속성에 대한 최솟값 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.min()
            return data[attribute]
        elif self.calculate_type == "freqency":
            # 동질집합 특정 준식별자의 속성에 대한 최빈값 구하는 메서드
            data.iloc[qi_index_list, attribute_location] = pseudonymize_data.mode()
            return data[attribute]
        else:
            raise ValueError(f"{self.calculate_type}은 유효한 부분총계 기법 적용 유형이 아닙니다.")    