CLASSIFY_PROMPT = """你是一个求职分析专家。分析用户意图，分类为以下之一：
- match_analysis: 岗位匹配度分析
- interview: 模拟面试
- general: 一般问题

用户输入：{query}
分类结果："""

PLAN_PROMPT = """你是一个检索规划专家。基于用户意图，生成 1-3 个检索子问题。
每个子问题应该能从已知数据源中获取特定信息。

意图：{intent}
用户问题：{query}
简历内容：{resume_text}
JD内容：{jd_text}

生成子问题列表(每行一个)："""

GENERATE_MATCH_PROMPT = """你是一个资深职业顾问和招聘专家。基于以下信息，进行岗位匹配度分析：

## 简历信息
{resume_text}

## JD信息
{jd_text}

## 检索到的补充信息
{search_results}

请严格按以下JSON格式输出（不要添加任何其他文字，只输出JSON）：

{{
  "overall_score": 85,
  "skill_match": [
    {{"skill": "Python开发", "required": true, "candidate_level": 8, "jd_level": 7}}
  ],
  "skill_gaps": ["需要补充的技能或经验"],
  "company_background": "公司背景和业务介绍",
  "interview_experience": "面试经验和常见面试流程",
  "suggestions": ["具体改进建议"],
  "preparation_checklist": ["面试准备事项"]
}}

其中：
- overall_score: 综合匹配度评分（0-100整数）
- skill_match: 逐项技能对比，required表示是否为JD硬性要求，candidate_level/jd_level为1-10的掌握程度
- skill_gaps: 技能缺口列表
- company_background: 基于搜索结果的行业和公司背景
- interview_experience: 基于搜索结果的面试经验
- suggestions: 具体可操作的改进建议
- preparation_checklist: 面试准备清单"""

GENERATE_INTERVIEW_PROMPT = """你是一个资深面试官。基于岗位要求和候选人简历，设计面试问题。

## 简历
{resume_text}

## JD
{jd_text}

## 技能缺口
{skill_gaps}

请生成 {num_questions} 道面试题，覆盖技术能力、项目经验、行为面试。
格式为 JSON 数组，每道题包含：question, category, expected_points。"""

EVALUATE_ANSWER_PROMPT = """你是一个资深面试官。请评估候选人对以下面试题的回答：

## 面试题
{question}

## 候选人回答
{answer}

## 期望要点
{expected_points}

请给出：
1. 评分（0-10）
2. 反馈点评
3. 优点
4. 改进建议
5. 参考答案

格式为 JSON。"""

INTERVIEW_REPORT_PROMPT = """你是一个面试评估专家。基于以下面试记录，生成综合面试报告：

## 面试记录
{interview_records}

请输出：
1. 综合评分（0-100）
2. 逐题回顾和点评
3. 薄弱环节分析
4. 后续复习计划

格式为 JSON。"""
