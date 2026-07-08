# TODO — 待优化项

---

## 1. LLM 结构化输出改用 Function Calling / Tool Use

**现状：** 所有 LLM 调用通过 Prompt 约束（"返回 JSON 格式..."）+ 后期手动清洗（剥离 \`\`\`json、json.loads 异常兜底）来获取结构化数据。

**问题：**
- DeepSeek 不支持 `response_format={"type": "json_object"}`，只靠 Prompt 无法保证输出格式
- Markdown 代码块清洗逻辑脆弱，LLM 模型更新后可能变化
- 字段名不匹配时（如 LLM 返回 `comprehensive_score` 而非 `overall_score`），静默回退到默认值，难以排查
- 现在每个调用点都要写一遍容错逻辑，重复且容易遗漏

**方案：** 将所有需要结构化输出的 LLM 调用改为 Function Calling：

```python
resp = client.chat.completions.create(
    model=settings.model_name,
    messages=[{"role": "user", "content": prompt}],
    tools=[{
        "type": "function",
        "function": {
            "name": "output_match_report",
            "parameters": {
                "type": "object",
                "properties": {
                    "overall_score": {"type": "integer"},
                    "skill_match": {"type": "array", "items": {
                        "type": "object",
                        "properties": {
                            "skill": {"type": "string"},
                            "required": {"type": "boolean"},
                            "candidate_level": {"type": "integer"},
                            "jd_level": {"type": "integer"}
                        },
                        "required": ["skill", "required", "candidate_level", "jd_level"]
                    }},
                    "skill_gaps": {"type": "array", "items": {"type": "string"}},
                    ...
                },
                "required": ["overall_score", "skill_match", "skill_gaps", ...]
            }
        }
    }],
    tool_choice={"type": "function", "function": {"name": "output_match_report"}}
)
# 从 resp.choices[0].message.tool_calls[0].function.arguments 取 JSON
```

**涉及文件与调用点：**

| 文件 | 函数/节点 | 当前输出 | 优先级 |
|------|-----------|----------|--------|
| `src/agent/graph.py` | `generate_node` | 匹配报告 JSON | 高 |
| `src/agent/reflection.py` | `reflect` | 4维度评估 JSON | 高 |
| `src/api/interview.py` | `start_interview` | 面试题数组 JSON | 中 |
| `src/api/interview.py` | `submit_answer` | 回答评估 JSON | 中 |
| `src/api/interview.py` | `get_interview_report` | 面试报告 JSON | 中 |

**注意事项：**
- 需先确认 DeepSeek V4 Pro 对 Function Calling / Tool Use 的支持情况和调用方式
- 如果 DeepSeek 的 tool_use 实现与 OpenAI 兼容，可直接用 OpenAI SDK 的 `tools` 参数
- `classify_node` 和 `plan_node` 输出简单文本，不需要改造

---

✅ **已完成** (2026-07-08)

### 实施内容

1. **新建 `src/agent/llm_client.py`** — 集中化 LLM 工具模块：
   - `get_client()` — 全局单例 OpenAI 客户端（避免重复实例化）
   - `call_with_tool()` — 通用结构化输出函数，强制 LLM 通过 Tool Call 返回 JSON
   - 内置 fallback 机制：Tool Call → 内容 JSON 解析 → 默认值
   - 5 个 Tool Schema 定义：`TOOL_MATCH_REPORT`, `TOOL_REFLECTION`, `TOOL_INTERVIEW_QUESTIONS`, `TOOL_ANSWER_EVALUATION`, `TOOL_INTERVIEW_REPORT`

2. **迁移 5 个调用点** 从 Prompt 约束 + 手动清洗改为 Function Calling：
   - `graph.py:generate_node` → 使用 `call_with_tool(TOOL_MATCH_REPORT)`，结果直接存为干净 JSON
   - `reflection.py:reflect` → 使用 `call_with_tool(TOOL_REFLECTION)`
   - `interview.py:start_interview` → 使用 `call_with_tool(TOOL_INTERVIEW_QUESTIONS)`
   - `interview.py:submit_answer` → 使用 `call_with_tool(TOOL_ANSWER_EVALUATION)`
   - `interview.py:get_interview_report` → 使用 `call_with_tool(TOOL_INTERVIEW_REPORT)`

3. **清理与一致性改进**：
   - `match.py` 移除冗余的 Markdown 代码块清洗逻辑（不再需要，`generate_node` 产出已是干净 JSON）
   - `tools.py:generate_question` 改为使用集中式客户端 + 补充遗漏的 `THINKING_DISABLED`
   - 消除所有手动 `json.loads(resp.choices...)` 散落点

### 效果

- 不再依赖 LLM 的 Prompt 遵守度来保证 JSON 格式
- 字段名由 Schema 强制约束，不再出现 `comprehensive_score` vs `overall_score` 不匹配问题
- 所有错误兜底集中在 `call_with_tool` 一处，不再散落重复的 try/except
- 向后兼容：如果 DeepSeek 对 `tool_choice="function"` 支持不完善，自动 fallback 到内容解析 + 默认值
