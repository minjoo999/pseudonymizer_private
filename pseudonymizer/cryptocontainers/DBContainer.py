class DBContainer:
    """DB에서 스키마와 테이블 이름을 저장하고 반환하는 추상 클래스"""
    def __init__(self):
        self._schema = None
        self._table = None

    def setSchemaTable(self, schema: str, table: str):
        """스키마명, 테이블명 저장 추상 메서드"""
        self._schema = schema
        self._table = table
        
    def getSchema(self):
        """스키마 이름 반환 추상 메서드"""
        return self._schema
        
    def getTable(self):
        """테이블 이름 반환 추상 메서드"""
        return self._table