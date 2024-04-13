from pseudonymizer.encryptionPseudonyms.pyMySQLQuery import PyMySQLQuery


class EncryptoKeyColumn(PyMySQLQuery):
    """결합키 일방향 암호화 클래스"""
    def __init__(self, pw: str, serverIP: str, port_num: int, user_name: str, database_name: str, kr_encoder: str):
        super().__init__(pw = pw)
        super().connectDatabase(
            serverIP, port_num, user_name, database_name, kr_encoder)

    def encryptoKeytoHashvalue(self, hash_byte_type, key_schema, key_table, key_column, salt_column):
        """SHA256 혹은 SHA512를 통해 결합키 컬럼값을 해시값으로 일방향 암호화하는 메서드"""
        if hash_byte_type == 256:
            sql = f"UPDATE {key_schema}.{key_table} SET {key_column} = SHA2(CONCAT({key_column}, {salt_column}), {hash_byte_type})"
        elif hash_byte_type == 512:
            sql = f"UPDATE {key_schema}.{key_table} SET {key_column} = SHA2(CONCAT({key_column}, {salt_column}), {hash_byte_type})"
        else: 
            raise ValueError(f"일방향 암호화 단위로 {hash_byte_type}bit를 256bit와 512bit 중 하나를 입력해야 합니다.")
        
        super().dataQueryLanguage(sql)
        super().executeQuery()
        super().commitTransaction()