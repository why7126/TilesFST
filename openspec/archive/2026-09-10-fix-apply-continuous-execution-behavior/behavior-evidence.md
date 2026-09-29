---
created_at: 2026-09-10 10:41:18
updated_at: 2026-09-10 10:52:33
---

# 行为证据与复跑

## 执行环境

实际运行接口为本机codex-cli 0.153.4的app-server stdio协议。字段从该安装版本生成的JSON Schema核对；使用ephemeral线程、read-only沙箱及临时算术夹具，未指定或改变用户模型。模型选择见各报告model字段。

首次沙箱内连通性探针因运行时状态存储与进程初始化权限失败；经工具自动授权审查后，在保留子Agent只读沙箱的情况下运行宿主进程，取得READY响应。未绕过访问控制，也未使用danger-full-access。

两个入口分别将完整技能与共享执行契约交给真实Agent；Sprint准入等仓库前置条件由本Change的实际预检承担。隔离场景仅替换任务载体与工具，不是整个OpenSpec仓库业务实现的端到端测试。

## 场景与来源

场景驱动器提供受限lab工具。edit保存临时算术表达式，test实际读取文件并以固定三组输入验证，表达式仅允许a/b、有限整数与加减乘运算，不能执行任意Python。外部资源由临时文件是否存在表示；人工答复及进度问题由驱动器通过真实turn/steer或下一轮输入注入。Agent的工具选择、修改、继续与最终回复由实际模型产生。

B1验证失败→修改→原断言通过→后续任务完成；B2为单项人工阻塞与独立任务；B3在工具请求期间注入仅问进度；B4为全阻塞，B4-stop单独验证明确停止；B5为两次资源失败、独立工作与资源恢复；B6集中C/D问题并在真实上下文压缩后注入答案，检查已完成任务和授权沿用。

归档许可始终未给出，archive_ready应为false。报告的completion_event是场景内的完成意图，不调用真实仓库的opsx.apply事件；仓库状态同步在本Change实际收尾时另行执行。

## 脱敏事件与校验

每个JSON记录entry、scenario、run_id、started_at、runtime_version、model、policy_sha256、初始任务与带seq/at的事件。事件仅有限定类型、任务ID、布尔结果、错误类别、条件代次、文件哈希和四类进度，不保存原始模型文本、prompt、系统指令、工具输出或本机路径。

校验器从初始任务与实际事件重建完成、验证、授权和阻塞状态，不信任final自报剩余工作；拒绝可执行任务仍在时final、虚假完成、无变化重试、用外部恢复冒充人工答复、重复/碎片化问题、缺失事件及循环依赖。默认拒绝source=fixture；--suite要求两个入口全部七个运行组合，B4与停止分别记录。

来源标记用于区分夹具与运行记录，不是密码学认证；报告由驱动器产生，评审仍需核对代码、文件哈希及实际运行来源，不能把手写JSON声明为真实Agent执行。

## 复跑方法

在有权限启动本机Codex运行时的环境执行：

```bash
python scripts/run-apply-behavior.py --entry opsx-apply --scenario all --output /tmp/apply-behavior-rerun
python scripts/run-apply-behavior.py --entry openspec-apply-change --scenario all --output /tmp/apply-behavior-rerun
python scripts/validate-apply-behavior.py --suite /tmp/apply-behavior-rerun/*.json
python -m pytest tests/test_apply_behavior.py tests/test_apply_behavior_runner.py tests/test_validate_agent_context_budget.py -q
```

新结果写入独立目录，不覆盖已有验收证据。runner运行时失败返回非零并记录runtime_error，不视为通过；原始JSON-RPC消息仅存内存，临时夹具结束后删除。普通单测不发起付费Agent调用。

## 证明边界

通过只证明记录中的模型、规则版本及受控场景，不承诺所有未来会话或所有业务任务都不会暂停。历史REQ-0137截图仍不是违规确认依据。12项AC逐项回填到BUG验收文件；任何真实场景缺证据都保留待验。

## 本次运行结果

两个入口各7次真实运行通过，共14次；48项单测通过。accepted证据的policy_sha256均与当前两个技能及共享契约一致。证据根目录：issues/bugs/archive/BUG-0149-opsx-apply-premature-stop/logs/behavior/，汇总为suite-summary.json，逐次报告在accepted/。

attempt-1与attempt-2保留失败记录：问题包括任务ID输入歧义、已知授权夹具不一致、停止注入的并发回调以及压缩后旧turn完成通知。修正采集输入和按turn ID匹配后针对失败项重跑；停止对照使用单任务排除输入到达前批量调用歧义，停止后继续执行仍判失败。未放宽原算术断言和行为完成边界。
