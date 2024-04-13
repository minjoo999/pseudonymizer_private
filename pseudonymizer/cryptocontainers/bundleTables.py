from abc import ABC, abstractmethod


class BundleTables(ABC):
    """테이블을 저장하는 추상 클래스"""
    @abstractmethod
    def selectTables(self, data):
        """DBContainer에서 선언한 스키마.테이블 중 목적에 맞는 테이블을 저장하는 추상 메서드"""
        pass

    @abstractmethod
    def getTableList(self):
        """selectTables에서 선택한 데이터를 반환하는 추상 메서드"""
        pass

    @abstractmethod
    def getSchemas(self):
        """selectTables에서 선택한 스키마명 반환하는 추상 메서드"""
        pass
    
    @abstractmethod
    def getTables(self):
        """selectTables에서 선택한 테이블명 반환하는 추상 메서드"""
        pass    