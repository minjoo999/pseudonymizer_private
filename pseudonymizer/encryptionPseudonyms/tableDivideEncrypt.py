from pseudonymizer.encryptionPseudonyms.divideEncrypter import DivideEncrypter


class TableDivideEncrypt:
    """테이블 1개를 결합키 / 결합대상정보 분할하고 암호화하는 클래스"""
    def __init__(self):
        self.pw = None
        self.serverIP = None
        self.port_num = None
        self.user_name = None
        self.database_name = None
        self.kr_encoder = None

        self.columns = None
        self.serial_col = None
        self.serial_text = None
        self.join_key = None
        self.salt_col = None

    def addDBInfo(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        """DB 연결 정보 입력 메서드"""
        self.pw = pw
        self.serverIP = serverIP
        self.port_num = port_num
        self.user_name = user_name
        self.database_name = database_name
        self.kr_encoder = kr_encoder

    def addSerialKeyInfo(self, columns: str, serial_col: str, serial_text: str, join_key: str, salt_col: str):
        self.columns = columns
        self.serial_col = serial_col
        self.serial_text = serial_text
        self.join_key = join_key
        self.salt_col = salt_col

    def divideEncrypt(self, original_table: tuple, key_table: tuple, target_table: tuple, func: str, salt: str):
        """원본 테이블 결합키와 결합대상정보로 분리하고 결합키 암호화"""
        divide_encrypter = DivideEncrypter()
        divide_encrypter.addDBInfo(self.pw, self.serverIP, self.port_num, self.user_name, self.database_name, self.kr_encoder)

        divide_encrypter.addTablesInfo(original_table, key_table, target_table)
        divide_encrypter.addSerialKeyInfo(self.columns, self.serial_col, self.serial_text, self.join_key, self.salt_col)
        divide_encrypter.divideOriginalTable(salt)
        divide_encrypter.encryptKeyCol(func)
    