class MonthConverter:
    regex = "[1-9]|1[0-2]"  # Разрешаем числа от 1 до 12

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)