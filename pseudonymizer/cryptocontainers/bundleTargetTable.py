from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.cryptocontainers.bundleTables import BundleTables


class BundleTargetTable(BundleTables):
    """결합대상 가명정보 테이블 저장 상속 클래스"""
    dbtables = None
    key_column = None

    def __init__(self):
        self.target_table = None

    @classmethod
    def addDBTables(cls, tables: DBContainer):
        """DB에서 가명결합을 수행할 원본 테이블 캡슐화하는 메서드"""
        cls.dbtables = tables

    def selectTables(self, target_table: DBContainer):
        """결합키 생성에 활용될 테이블 저장하는 클래스"""
        self.target_table = target_table

    def getTableList(self):
        """결합키 생성항목 테이블 반환하는 메서드"""
        return self.target_table

    def getSchemas(self):
        """스키마명 반환하는 메서드"""
        return self.target_table.getSchema()

    def getTables(self):
        """테이블명 반환하는 메서드"""
        return self.target_table.getTable()

    @classmethod
    def reset(cls):
        """클래스 변수 초기화"""
        cls.dbtables = None
        cls.target_columns = None
