XLGD Trust Lifecycle & Assurance

信任生命周期与保证体系——工程任务书

一、目标

建立覆盖注册、身份验证、证据采集、独立评测、授权、运行监控、风险处置、撤销和重新评测的完整生命周期。

核心原则：

* Registration ≠ Verification
* Verification ≠ Evaluation
* Evaluation ≠ Authorization
* Authorization ≠ Permanent Trust
* CI Green ≠ Security Assurance
* Self-evaluation ≠ Independent Certification

二、六个工作包

WP1：Trust Revocation（信任撤销）

* 定义证据失效、身份撤销、授权撤销、版本撤销。
* 定义撤销原因、时间、影响范围和恢复条件。
* 设计撤销状态传播机制。
* 验证下游系统能否及时识别已撤销对象。

验收：撤销记录可追踪，下游能够识别失效状态，不能继续把旧授权当作有效授权。

WP2：Version & Compatibility（版本与兼容）

* 建立 UIBC、LGD Rules、LGD-Eval Engine 的版本关系。
* 定义证据适用版本和兼容范围。
* 定义重大规则变化后的重新评测条件。
* 保留旧版本证据，不得静默覆盖。

验收：给定旧证据、旧规则和新引擎，能够明确判断是否兼容、是否需要重新评测。

WP3：Adversarial Assurance（对抗性保证）

至少覆盖：

* 证据伪造与重新签名。
* 身份冒用与密钥替换。
* 证据重放、过期和撤销绕过。
* 恶意技能与依赖污染。
* 权限提升和沙箱逃逸。
* UNKNOWN、INCOMPLETE 状态被错误放行。

验收：每个攻击场景有测试输入、预期结果、实际结果和可复现证据；失败测试不得被统计为通过。

WP4：Independent Reproduction（独立复现）

* 提供独立测试包和标准测试语料。
* 提供测试命令、输入、预期输出和判定规则。
* 允许外部开发者不依赖项目内部环境运行。
* 记录复现者、环境、版本和差异。
* 区分自测、关联方复测、独立复现。

验收：至少一个核心模块由非关联第三方独立复现；没有实际第三方证据，不得标记为独立验证完成。

WP5：Commercial Assurance Boundary（商业责任边界）

明确产品输出的法律和技术含义：

* Registry：登记记录，不代表安全认证。
* Evidence：证据记录，不代表事实绝对真实。
* Evaluation：按公开方法进行的技术评估，不代表零风险。
* Authorization：明确主体、范围、期限和条件的授权决定。
* Monitoring：持续监测，不代表持续安全保证。

验收：每种报告和产品输出均有用途、限制、责任边界和适用版本说明。

WP6：Operational Continuity（运营连续性）

* 定义规则维护、漏洞响应和版本支持责任人。
* 建立漏洞严重程度和响应时限。
* 定义证据保存、备份和导出规则。
* 建立项目停止、服务中断和维护者退出机制。
* 保证用户可以导出自己的数据和证据。

验收：发生维护者退出、服务停止或关键组件失效时，用户仍可读取、验证和迁移已有证据。

三、统一状态模型

建议统一研究以下状态：

REGISTERED
→ EVIDENCE_PENDING
→ VERIFIED
→ EVALUATED
→ AUTHORIZATION_PENDING
→ AUTHORIZED
→ MONITORED

异常状态：

UNKNOWN / INCOMPLETE / EXPIRED / REVOKED / SUSPENDED / FAILED

注意：状态转换必须由明确证据和授权规则触发，不允许仅凭评分自动获得 AUTHORIZED。

四、实施顺序

第一阶段：只读盘点现有仓库、协议、接口和测试。

第二阶段：形成统一状态模型、接口草案和威胁模型。

第三阶段：在本地建立测试原型和负向测试。

第四阶段：组织独立复现，记录差异。

第五阶段：评估商业产品化条件。

五、审批边界

本任务书仅授权研究、只读审计、设计和本地测试准备。

未经 Steven Zhao 单独批准，不得：

* 修改远端仓库或合并 PR。
* 推送代码、发布版本或部署服务。
* 修改许可证、版权和作者署名。
* 对外宣称获得独立认证或标准采纳。
* 对外提交、联系客户或作出商业承诺。

六、最终交付物

1. Trust Lifecycle Architecture
2. Revocation & Expiration Specification
3. Version Compatibility Matrix
4. Adversarial Test Suite
5. Independent Reproduction Kit
6. Commercial Assurance Boundary
7. Operational Continuity Plan
8. Evidence-backed Acceptance Report

所有结论必须附实际证据、版本、测试时间和复核状态。未验证事项明确标记 NOT VERIFIED。