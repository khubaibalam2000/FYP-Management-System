class diagnosisDBRouter(object):
    """
    A router to control diagnosis_data db operations
    """
    def db_for_read(self, model, **hints):
        "Point all operations on diagnosis_data models to 'db_diagnosis'"
        from django.conf import settings
        if 'db_diagnosis' not in settings.DATABASES:
            return None
        if model._meta.app_label == 'diagnosis_data':
            return 'db_diagnosis'
        return None

    def db_for_write(self, model, **hints):
        "Point all operations on diagnosis_data models to 'db_diagnosis'"
        from django.conf import settings
        if 'db_diagnosis' not in settings.DATABASES:
            return None
        if model._meta.app_label == 'diagnosis_data':
            return 'db_diagnosis'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        "Allow any relation if a model in diagnosis_data is involved"
        from django.conf import settings
        if 'db_diagnosis' not in settings.DATABASES:
            return None
        if obj1._meta.app_label == 'diagnosis_data' or obj2._meta.app_label == 'diagnosis_data':
            return True
        return None

    def allow_syncdb(self, db, model):
        "Make sure the diagnosis_data app only appears on the 'diagnosis_data' db"
        from django.conf import settings
        if 'db_diagnosis' not in settings.DATABASES:
            return None
        if db == 'db_diagnosis':
            return model._meta.app_label == 'diagnosis_data'
        elif model._meta.app_label == 'diagnosis_data':
            return False
        return None