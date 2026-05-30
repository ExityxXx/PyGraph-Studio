# Установка

## Системные требования

| Требование | Минимальные | Рекомендуемые |
|------------|-------------|---------------|
| **ОЗУ** | 64 MB | 128 MB |
| **Место на диске** | 6 MB | 25 MB |
| **Python** | 3.8+ (уже установлен) | 3.10+ |

## Установка из исходников

### 1. Клонирование репозитория

```bash
git clone https://github.com/ExityxXx/pygraph-studio
cd pygraph-studio
```

Или можете установить через [GitHub](https://github.com/ExityxXx/pygraph-studio) 

### 2. Установка зависимостей
Проект использует только стандартную библиотеку Python. Дополнительные зависимости не требуются.

Если возникает ошибка с Tkinter:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**Fedora:**
```bash
sudo dnf install python3-tkinter
```

**MacOS**
```bash
brew install python-tk
```

### Если окно не открывается
Проверьте, что у вас установлена поддерживаемая версия Python:

```bash
python --version
```

Должно быть Python 3.8 или выше.

### 3. Запуск
```bash
python main.py
```


### Удаление
Просто удалите папку с проектом.

```bash
rm -rf pygraph-studio
```

Или на Windows:

```cmd
rmdir /s pygraph-studio
```