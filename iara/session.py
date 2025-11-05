class UserSession:
    def __init__(self):
        self.cod_empresa = None
        self.cod_login = None

    def login(self, user_data):
        self.cod_empresa = user_data.get('cod_empresa')
        self.cod_login = user_data.get('cod_login')

    def logout(self):
        self.cod_empresa = None
        self.cod_login = None

current_user = UserSession()