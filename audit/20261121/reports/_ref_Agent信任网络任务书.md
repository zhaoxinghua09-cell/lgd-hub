XLGD Agent Trust Network

AI Agent 信任网络技术研究任务书

一、研究目标

研究建立面向多 Agent、多平台、多工具环境的开放信任基础设施。

重点解决身份、行为证据、委托授权、动态风险、供应链和跨生态互操作问题。

二、研究工作包

WP1：Agent Identity

* 唯一身份与实体关系。
* 创建者、运营者和实现者关系。
* 版本变更和身份连续性。
* 身份冒用与撤销。

WP2：Behavioral Evidence

* Agent 行为事件模型。
* 事件来源与完整性。
* 观测证据与声明证据区分。
* 证据有效期和隐私保护。

WP3：Trust Delegation

* 委托链与权限继承。
* 委托深度和范围限制。
* 再委托控制。
* 授权撤销传播。
* 委托链审计。

WP4：Dynamic Trust

* 评测分数与授权状态分离。
* 证据可信度和运行风险分离。
* 版本变化后的状态更新。
* 过期、异常和撤销处理。

WP5：Agent Supply Chain

* Skills、MCP、API、模型和数据依赖图。
* 依赖版本和来源。
* 风险传播。
* 供应链变化后的重新评测。

WP6：Trust Discovery & Registry

* Agent 注册和发现。
* 证据查询。
* 风险状态展示。
* 兼容性和授权查询。
* 公开记录与隐私边界。

WP7：Trust API

* 身份解析。
* 证据查询。
* 评测结果查询。
* 授权检查。
* 撤销查询。
* 委托链验证。

WP8：Cross-Ecosystem Interoperability

* 现有协议映射。
* 外部身份体系对接。
* 第三方评测结果接入。
* 跨平台测试向量。

三、优先研究顺序

P0：身份、证据、授权状态分离。

P1：委托链和撤销传播。

P2：供应链依赖与动态风险。

P3：Registry 和 Trust API。

P4：跨生态互操作与第三方实现。

四、关键验收场景

1. Agent 更换版本后，旧评测证据能否被正确识别。
2. Agent 身份被冒用后，能否撤销并传播。
3. Agent B 超出 Agent A 授权范围时，能否阻断。
4. Agent C 被撤销后，依赖它的上游系统能否感知。
5. 第三方评测结果能否被独立验证。
6. 不同平台实现能否交换和解释证据。
7. UNKNOWN 和 INCOMPLETE 是否会被错误放行。

五、交付成果

* Agent Trust Architecture。
* Agent Identity Schema。
* Behavioral Evidence Schema。
* Delegation Model。
* Dynamic Trust State Model。
* Agent Supply Chain Model。
* Trust API Specification。
* Conformance Test Suite。
* Threat Model。
* Independent Reproduction Report。

六、审批边界

本任务书仅授权只读研究、架构设计和本地原型准备。

不授权新建正式项目、远端仓库修改、协议发布、对外合作、标准提交、认证承诺或商业承诺。

任何外部行动须另行取得 Steven Zhao 批准。