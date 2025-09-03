class SymbolTable:
    count_locals = 0
    count_params = 0
    count_fields = 0
    count_statics = 0

    _class_scope = {}
    _subroutine_scope = {}

    def start_subroutine(self):
        self._subroutine_scope = {}
        self.count_locals = 0
        self.count_params = 0

    def define(self, name, type_, kind):
        if kind in ["static", "field"]:
            if kind == "static":
                self._class_scope[name] = (type_, kind, self.count_statics)
                self.count_statics += 1
            else:
                self._class_scope[name] = (type_, kind, self.count_fields)
                self.count_fields += 1
        else:
            if kind == "local":
                self._subroutine_scope[name] = (type_, kind, self.count_locals)
                self.count_locals += 1
            else:
                self._subroutine_scope[name] = (type_, kind, self.count_params)
                self.count_params += 1

    def get_kind(self, name):
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][1]
        elif name in self._class_scope:
            return self._class_scope[name][1]
        else:
            return None

    def get_index(self, name):
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][2]
        elif name in self._class_scope:
            return self._class_scope[name][2]
        else:
            return None

    def get_type(self, name):
        if name in self._subroutine_scope:
            return self._subroutine_scope[name][0]
        elif name in self._class_scope:
            return self._class_scope[name][0]
        else:
            return name

    def get_count(self, name):
        if name == "local":
            return self.count_locals
        elif name == "argument":
            return self.count_params
        elif name == "field":
            return self.count_fields
        elif name == "static":
            return self.count_statics
        else:
            return None
