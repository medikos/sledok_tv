from datetime import datetime, timedelta


class ForDayWeek:
    def __init__(self, storage_name):
        self.dict_fields = {storage_name: self.for_day_or_week}
        self.storage_name = storage_name
        self.date = datetime.now().date()


    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = 'Завтра' if self.storage_name == 'for_day' else 'Через неделю'
        setattr(instance, 'data', self.dict_fields[self.storage_name]())
        setattr(instance, 'day_or_week', value)
        return instance.data

    def __set__(self, instance, value):
        raise ValueError('You can"t set a value for an attribute')

    def for_day_or_week(self):
        if self.storage_name == 'for_day':
            return datetime.now().date() + timedelta(days=1)
        if self.storage_name == 'for_week':
            return datetime.now().date() + timedelta(days=7)

        else:
            raise ValueError('The value for the attribute is set incorrectly')


class Episodes:
    def __init__(self, date=None):
        self.date = date
