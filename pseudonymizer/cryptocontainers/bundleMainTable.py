from pseudonymizer.cryptocontainers.DBContainer import DBContainer
from pseudonymizer.cryptocontainers.bundleTables import BundleTables


class BundleMainTable(BundleTables):
    """가명정보 결합대상 원본테이블 저장 상속 클래스"""
    dbtables = None

    def __init__(self):
        self.dbtables = None

    def selectTables(self, tables: DBContainer):
        """가명정보 결합대상 원본테이블 저장하는 클래스"""
        self.dbtables = tables

    def getTableList(self):
        """가명정보 결합대상 원본테이블 반환하는 메서드"""
        return self.dbtables

    def getSchemas(self):
        """스키마명 반환하는 메서드"""
        return self.dbtables.getSchema()

    def getTables(self):
        """테이블명 반환하는 메서드"""
        return self.dbtables.getTable()