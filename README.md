# AI-Test-Agent-Platform

基于大模型驱动的全链路智能测试 Agent 平台。

## 架构

5 个 Agent 组成的长链推理协作架构，形成从需求到发版决策的完整闭环：

需求文档 → ① 用例生成Agent（多轮长链推理）
              ↓ 并行分发
         ② 接口自动化Agent  ③ UI自动化Agent
              ↓ 结果汇聚
         ④ 缺陷根因分析Agent（ReAct推理）
              ↓
         ⑤ 回归风险评估Agent（多因子加权推理）

## 核心特性

- 5 Agent 长链推理协作：单次完整测试流程推理链深度超过 30 步
- CoT + Few-Shot 策略：用例生成 Agent 通过 4 轮推理逐步拆解业务场景
- ReAct 推理-行动循环：缺陷分析 Agent 通过排除法定位根因
- 多因子加权推理：风险评估 Agent 综合覆盖率、缺陷等级、影响面输出发版建议

## 落地成果

| 指标 | 落地前 | 落地后 |
|---|---|---|
| 回归测试周期 | 3 天 | 4 小时 |
| 用例编写效率 | 1.5 天/需求 | 2 小时/需求 |
| 缺陷定位时间 | 4 小时 | 20 分钟 |
| 漏测率 | 基线值 | 下降 40% |

日均实际消耗约 150 万 Token，通过缓存复用策略实现 92% 的缓存命中率，等效推理量约 1800 万 Token。


## 快速开始

pip install -r requirements.txt
python demo.py

Demo 模式无需 API Key，模拟完整工作流并输出终端日志。

## 正式使用

1. 编辑 config.yaml 填入 API Key
2. 将需求文档放入 examples/ 目录
3. 运行 python main.py

## 项目结构

ai-test-agent-platform/
├── README.md
├── requirements.txt
├── config.yaml
├── main.py
├── demo.py
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── case_generator.py
│   ├── api_tester.py
│   ├── ui_tester.py
│   ├── defect_analyzer.py
│   └── risk_assessor.py
├── orchestrator/
│   ├── __init__.py
│   └── workflow.py
├── prompts/
│   ├── case_generator.txt
│   ├── api_tester.txt
│   ├── ui_tester.txt
│   ├── defect_analyzer.txt
│   └── risk_assessor.txt
└── examples/
    └── sample_requirement.md
