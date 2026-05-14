# 阅读笔记：The Vector Grounding Problem

**论文ID**: 004
**作者**: Raphaël Millière, Dimitri Coelho Mollo
**年份**: 2026
**期刊**: Forthcoming (preprint)
**优先级**: 必读

---

## 一、核心论点

本文重新激活了经典认知科学中的"符号基础问题"（Symbol Grounding Problem, Harnad 1990），并赋予其向量时代的精确形式。核心论证：LLM的嵌入向量面临三层基础缺失——（1）因果基础缺失：训练目标（下一个token预测）与外部世界之间没有因果锚定关系；（2）功能基础缺失：向量的功能角色完全由与其他向量的共现统计关系决定，缺乏与世界的功能耦合；（3）规范性基础缺失：向量没有"正确使用条件"，任何输出的正确性仅取决于训练分布而非世界事实。结论：纯语言LLM的向量表征的语义内容完全是"派生的"（derived）——它们仅从人类解释者那里"借用"意向性。但关键限制：多模态模型可能部分克服这种基础缺失，因为视觉输入提供了因果锚定。

## 二、方法论特点

1. **概念工程**（conceptual engineering）：将Harnad的经典问题重构为适合深度学习时代的精确形式。
2. **三层分析框架**：因果层、功能层、规范层的递进检验——每一层识别一种特定的基础缺失。
3. **思想实验方法**：设计"分裂向量"（split vectors）和"向量的颠倒光谱"（inverted spectrum for vectors）等新思想实验。
4. **外在论语义学对勘**：将分析结论与Kripke、Putnam、Burge、Millikan的外在论语义学传统进行系统比较。

## 三、关键概念

- **向量基础问题**（Vector Grounding Problem）：LLM的嵌入向量是否具有独立于人类解释的内在语义内容？答案：纯语言模型中是否定的。
- **派生意向性**（derived intentionality）vs. **本有意向性**（intrinsic intentionality）：经典Searle区分在向量时代的重新表述。
- **三层基础缺失**：因果锚定缺失（没有世界→向量的因果链）、功能耦合缺失（没有向量→世界的功能链）、规范性缺失（没有"正确性"标准）。
- **多模态阶梯**（multimodal ladder）：视觉-语言模型的视觉接地可能构成从派生意向性到本有意向性的部分阶梯。

## 四、对本项目的启示

1. **对MI的"表征发现"的根本挑战**：如果Millière和Coelho Mollo是正确的，那么MI研究者声称的"发现诚实特征""定位真理方向"可能是在"创造"而非"发现"——我们将外在语义投射到无内在内容的激活模式上。
2. **三层评估框架的方法论价值**：对于每一个MI发现的"概念特征"，我们可以用三层框架评估其语义基础程度。
3. **多模态优先策略**：本文暗示多模态模型的MI研究在哲学上比纯语言模型的MI研究更有辩护力——这为我们的项目（涉及多模态模型的部分）提供了优先顺序论证。
4. **与02_alignment_frameworks的连接**：如果内部表征没有内在语义基础，那么"表征工程"（representation engineering）作为对齐方法需要重新审视其哲学预设。

## 五、批判性反思

1. 对外在论语义学的依赖——内在论者可能反驳因果/功能/规范基础的要求过强。
2. "多模态模型可能更基础"的论证目前是纲领性的，缺乏对具体视觉-语言架构的详细分析。
3. "全有或全无"的基础观可能存在"程度谬误"——语义性可能是渐进的（graded）而非二元的。
4. 未对接具体的MI文献发现——失去了一个重要的经验证据来源。

## 六、关键引用

- "In purely linguistic LLMs, the semantic content of embedding vectors is entirely derived — they borrow intentionality from human interpreters."
- "The vector grounding problem: causal anchoring missing, functional coupling absent, normative correctness undefined."
- "Multimodal models may partially overcome the grounding deficit through visual causal anchoring."

## 七、建议配对阅读

- 与 018 (Martínez) 对话：信息论表征理论可以提供"程度化基础"的概念工具
- 与 006 (Griffiths) 互补：两个不同方向的追问——向量有什么内容？符号是否必要？
- 与 003 (Smart et al.) 对立：如果LLM缺乏内在语义，将其视为扩展认知系统的合法性存疑
