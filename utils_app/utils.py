import os
from datetime import datetime

from pytils.translit import slugify


def image_file_path(instance, filename):
    """
    Генерирует путь для сохранения изображения. Формирует имя файла на основе
    поля `title` объекта `instance`, добавляя текущую метку времени. Если
    у объекта нет атрибута `title`, используется только временная метка.
    Возвращает путь в директорию `images/` с новым именем файла.
    """
    name = ''
    ext = filename.split('.')[-1]
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        name = f'{slugify(instance.title.replace('_', '-'))}_'
    except AttributeError:
        name = ''
    finally:
        filename = f'{name}{timestamp}.{ext}'
    return os.path.join('images/', filename)
