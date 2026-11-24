# 后端自动化测试。
#
# 跑法：cd backend && .venv/bin/python -m pytest -q
# 测试用环境变量 HISTORY_DB 把数据指到一个临时库，
# 绝不会碰你真实的 history.db。

import os
import tempfile

# 必须在 import main 之前设好：main 导入的那一刻会 init_db()
os.environ["HISTORY_DB"] = os.path.join(tempfile.mkdtemp(), "test.db")

from fastapi.testclient import TestClient
import main

client = TestClient(main.app)


def test_profile():
    r = client.get("/api/profile")
    assert r.status_code == 200
    assert r.json()["heroTitle"] == "关于我"


def test_analyze_ok():
    r = client.post("/api/analyze", json={"text": "今天天气真好"})
    assert r.status_code == 200
    data = r.json()
    assert data["text"] == "今天天气真好"
    assert isinstance(data["score"], float)
    assert data["label"] in ("偏积极", "偏消极", "中性")
    assert data["pinyin"].strip() != ""


def test_analyze_empty_rejected():
    # 空字符串会让 SnowNLP 除零，前后端约定好直接拒绝，别走到 500
    assert client.post("/api/analyze", json={"text": ""}).status_code == 422
    assert client.post("/api/analyze", json={"text": "   "}).status_code == 422


def test_history_isolated_per_session():
    # 两个访客各写一条，谁也别看到谁的
    a = TestClient(main.app)
    b = TestClient(main.app)
    a.post("/api/analyze", json={"text": "A 的记录"})
    b.post("/api/analyze", json={"text": "B 的记录"})
    assert [x["text"] for x in a.get("/api/history").json()] == ["A 的记录"]
    assert [x["text"] for x in b.get("/api/history").json()] == ["B 的记录"]


def test_clear_history():
    c = TestClient(main.app)
    c.post("/api/analyze", json={"text": "待清空"})
    assert len(c.get("/api/history").json()) == 1
    r = c.delete("/api/history")
    assert r.status_code == 200
    assert c.get("/api/history").json() == []
