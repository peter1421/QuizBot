
# 常用指令和配置

## 安裝和更新依賴

1. **安裝項目依賴**：
   ```powershell
   poetry install
   ```

2. **添加新依賴**：
   ```powershell
   poetry add <package_name>
   ```

3. **添加開發依賴**：
   ```powershell
   poetry add --dev <package_name>
   ```

4. **更新所有依賴**：
   ```powershell
   poetry update
   ```

## 格式化和修復代碼

1. **使用 `ruff` 修復代碼**：
   ```powershell
   poetry run ruff . --fix
   ```

2. **使用 `isort` 格式化導入**：
   ```powershell
   poetry run isort .
   ```

3. **使用 `black` 格式化代碼**：
   ```powershell
   poetry run black .
   ```

## 配置文件（`pyproject.toml`）

確保在你的 `pyproject.toml` 文件中有以下配置：

```toml
[tool.isort]
profile = "black"
skip = ["env"]

[tool.ruff]
line-length = 120
target-version = "py39"
select = [
  "F", "E", "W", "N", "PL", "C90", "I", "D", "UP", "A", "COM", "B", "C4", "TCH", "DTZ", "T20", "TID", "Q", "PTH", "ICN", "DJ"
]
ignore = [
  "D100", "D101", "D102", "D103", "D104", "D105", "D106", "D107", "D212", "D203", "D202"
]
exclude = ["env"]

[tool.poetry]
name = "QuizBot_django"
version = "0.1.0"
description = ""
authors = ["林子白 <abcde12345326@gmail.com>"]

[tool.poetry.dependencies]
python = "^3.9"

[tool.poetry.group.lint.dependencies]
ruff = "^0.1.6"
black = "^23.11.0"
pyright = "^1.1.337"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

這樣的配置和指令應該能夠滿足你日常的開發需求。如果還有其他特定需求或問題，請隨時告訴我。