# 04 - IO / Paths: pathlib + json + csv + logging

> 把磁盘当数据库的代码写法。学完能正确处理路径、JSON/CSV、日志、临时文件，不再 `os.path.join` 拼字符串。

## 前置

- [01-fundamentals](../01-fundamentals)

## 本章目标

- 用 `pathlib.Path` 替代所有 `os.path` 操作
- 读写 JSON、JSONL、CSV、TOML 的最佳实践
- `logging` 取代 `print`：handler、formatter、级别
- `tempfile`、原子写、文件锁
- 编码与换行问题（永远 `encoding="utf-8"`，永远 `newline=""` 读 CSV）

## 推荐库 / 模块

- stdlib: `pathlib`, `json`, `csv`, `tomllib`, `logging`, `tempfile`, `shutil`
- 第三方: `orjson`（更快的 json），`structlog`（结构化日志）

## 计划要写

- `src/`: 日志配置工厂、原子写 JSON、按行流式处理大 CSV
- `tests/`: 用 `tmp_path` fixture 隔离文件 IO

## 自测

- `Path.read_text()` 默认编码是？为什么不应该信赖它？
- 为什么 csv reader 一定要 `newline=""`？
- `logging.basicConfig` 调用多次会怎样？
- 原子写为什么不能直接覆盖文件？

---

**TODO**: 待补充完整代码与测试。
