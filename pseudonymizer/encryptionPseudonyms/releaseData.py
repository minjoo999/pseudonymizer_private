from pseudonymizer.cryptocontainers.initTables import InitTables
from pseudonymizer.cryptocontainers.tableContainer import TableContainer
from pseudonymizer.cryptocontainers.targetTables import TargetTables
from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class ReleaseData(PyMySQLQuery):
    """결합대상정보 반출 클래스"""
    def __init__(self, external: bool, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        self.external = external
        super().__init__(pw = pw)
        super().connectDatabase(serverIP, port_num, user_name, database_name, kr_encoder)

        self.init_table = None
        self.original_target = None
        self.target = None
        self.joined_target = None
        self.result = None

    def addOriginalTarget(self, init_table: InitTables):
        """결합 이전의 타겟 테이블 스키마/테이블 내용 입력"""
        self.init_table = init_table
        self.original_target = init_table.target_table

    def addJoinedTarget(self, target: TargetTables):
        """이미 결합된 결합대상정보 스키마/테이블 내용 입력"""
        self.target = target
        self.joined_target = target.target_result

    def addResult(self, result: TableContainer):
        """반출 스키마/테이블 내용 입력"""
        self.result = result

    def rateJoinedData(self):
        """결합률 확인 메서드
           * 결합률 = 결합된 레코드 수 / 원 레코드 수
        """
        original_schema = self.original_target.getSchema()
        original_table = self.original_target.getTable()

        joined_schema = self.joined_target.getSchema()
        joined_table = self.joined_target.getTable()

        super().dataQueryLanguage(f"SELECT COUNT(*) FROM {original_schema}.{original_table}")
        original_records = super().executeQueryAsDataFrame()['COUNT(*)'][0]

        super().dataQueryLanguage(f"SELECT COUNT(*) FROM {joined_schema}.{joined_table}")
        joined_records = super().executeQueryAsDataFrame()['COUNT(*)'][0]

        joined_rate = joined_records / original_records
        return joined_rate

    def releaseData(self):
        """가명정보 결합 결과물을 DB에 저장하는 메서드
           * JoinData 클래스 결과물 중 컬럼 선택

           * 예시 쿼리
           SELECT (컬럼 나열) FROM (결합결과 테이블) LEFT JOIN (원 테이블)
	        ON (결합결과 테이블).(serial_col) = (원 테이블).(serial_col);
        """
        original_schema = self.original_target.getSchema()
        original_table = self.original_target.getTable()

        joined_schema = self.joined_target.getSchema()
        joined_table = self.joined_target.getTable()

        result_schema = self.result.getSchema()
        result_table = self.result.getTable()

        serial_col = self.init_table.serial_col

        columns = [f"{original_schema}.{original_table}.{serial_col}"]

        for tc in self.target.target_columns:
            columns.append(f"{joined_schema}.{joined_table}.{tc}")

        rate = self.rateJoinedData()
        
        if (self.external == True) & (rate >= 0.5):
            print("결합률이 50% 이상이므로 데이터 반출 불가합니다")
        else:
            super().dataQueryLanguage(f"DROP TABLE IF EXISTS {result_schema}.{result_table}")
            super().executeQuery()

            create_sql = f"CREATE TABLE {result_schema}.{result_table} AS "
            select_sql = f"SELECT {', '.join(columns)} FROM {original_schema}.{original_table} "
            join_sql = f"LEFT JOIN {joined_schema}.{joined_table} ON {joined_schema}.{joined_table}.{serial_col} = {original_schema}.{original_table}.{serial_col}"

            sql = create_sql + select_sql + join_sql

            super().dataQueryLanguage(sql)
            super().executeQuery()