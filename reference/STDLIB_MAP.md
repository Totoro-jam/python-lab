# 标准库按用途速查

> 装 Python 就有的电池。能用 stdlib 解决的不要装第三方。

---

## 文件 / 路径 / 文本

| 模块 | 干啥 |
|---|---|
| `pathlib` | 现代路径操作（替代 `os.path`） |
| `os`, `os.path` | 系统、进程、env、老式路径 |
| `shutil` | 复制、移动、删除、归档 |
| `glob`, `fnmatch` | 通配匹配（`pathlib.glob` 更现代） |
| `tempfile` | 临时文件/目录 |
| `io` | StringIO/BytesIO 内存流 |
| `csv` | CSV 读写 |
| `json` | JSON 序列化 |
| `tomllib` | 3.11+ 读 TOML（写需要第三方 `tomli-w`） |
| `configparser` | INI 配置文件 |
| `xml.etree.ElementTree` | XML |

---

## 数据结构 / 算法

| 模块 | 干啥 |
|---|---|
| `collections` | `deque`, `Counter`, `defaultdict`, `OrderedDict`, `namedtuple` |
| `itertools` | 迭代器组合：`chain`, `groupby`, `islice`, `product`, `combinations` |
| `functools` | `cache`, `lru_cache`, `partial`, `reduce`, `wraps` |
| `heapq` | 小顶堆（优先队列） |
| `bisect` | 有序列表二分插入 / 查找 |
| `array` | 紧凑数值数组（numpy 之外的轻量选择） |
| `enum` | 枚举 |
| `dataclasses` | 数据类 |
| `typing` | 类型注解 |

---

## 时间 / 日期

| 模块 | 干啥 |
|---|---|
| `datetime` | 日期时间主力 |
| `time` | 时间戳、sleep、性能计时 |
| `calendar` | 日历计算 |
| `zoneinfo` | 3.9+ IANA 时区（替代 pytz） |

---

## 数学 / 随机

| 模块 | 干啥 |
|---|---|
| `math` | 浮点数学 |
| `statistics` | mean / median / stdev |
| `random` | 伪随机（**不要**用于密码学） |
| `secrets` | 密码学级随机（密码、token） |
| `decimal` | 高精度十进制 |
| `fractions` | 分数 |

---

## 并发 / 异步

| 模块 | 干啥 |
|---|---|
| `asyncio` | 协程（IO 密集型首选） |
| `threading` | 线程（受 GIL 影响，适合 IO） |
| `multiprocessing` | 多进程（CPU 密集型） |
| `concurrent.futures` | 高级线程/进程池（推荐入口） |
| `queue` | 线程安全队列 |
| `subprocess` | 跑外部命令 |
| `signal` | 信号 |

---

## 网络 / Web

| 模块 | 干啥 |
|---|---|
| `urllib.request` | 简单 HTTP（生产用 `httpx`/`requests`） |
| `urllib.parse` | URL 解析（这个常用） |
| `http.server` | 起一个临时服务器：`python -m http.server` |
| `socket` | 底层 socket |
| `ssl` | TLS |
| `email`, `smtplib`, `imaplib` | 邮件 |

---

## 测试 / 调试

| 模块 | 干啥 |
|---|---|
| `unittest` | 内置测试（生产用 `pytest`） |
| `doctest` | 文档字符串里的小测试 |
| `pdb` | 调试器：`breakpoint()` |
| `traceback` | 异常堆栈格式化 |
| `logging` | 日志（不要 print） |
| `warnings` | 警告 |

---

## 数据库

| 模块 | 干啥 |
|---|---|
| `sqlite3` | SQLite，开箱即用 |
| `dbm` | 键值持久化 |

---

## 序列化 / 压缩

| 模块 | 干啥 |
|---|---|
| `pickle` | Python 对象序列化（**安全风险**：不要 unpickle 不信任数据） |
| `gzip`, `bz2`, `lzma`, `zipfile`, `tarfile` | 各类压缩 |
| `base64` | base64 编码 |
| `hashlib` | md5/sha256 摘要 |
| `hmac` | 消息认证 |

---

## 命令行

| 模块 | 干啥 |
|---|---|
| `argparse` | 内置 CLI 解析（轻量项目够用） |
| `getopt` | 老式 C 风格（不推荐） |
| `cmd` | 交互式命令解释器 |
| `readline` | REPL 行编辑 |

生产更推荐 `typer` / `click`。

---

## 内省 / 元编程

| 模块 | 干啥 |
|---|---|
| `inspect` | 看函数签名、源码、调用栈 |
| `dis` | 反汇编字节码 |
| `ast` | 抽象语法树 |
| `importlib` | 动态 import |
| `contextlib` | `@contextmanager`, `suppress`, `ExitStack` |
| `weakref` | 弱引用 |

---

## 速记口诀

- 解析路径 → `pathlib`
- 计数 / 分组 → `collections`
- 笛卡尔积、组合、扁平 → `itertools`
- 缓存函数 → `functools.cache`
- IO 并发 → `asyncio` 或 `concurrent.futures.ThreadPoolExecutor`
- CPU 并发 → `multiprocessing` 或 `concurrent.futures.ProcessPoolExecutor`
- 临时文件 → `tempfile`
- 跑命令 → `subprocess.run(...)`
- 时区 → `zoneinfo`
- 日志 → `logging`，**不是 print**
