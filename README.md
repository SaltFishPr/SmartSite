# 智慧工地检查系统

## 设计目标

智慧工地检查系统是利用信息化手段，使用 Web 通信技术，取代传统人工操作，构建施工项目信息化生态圈，并将此数据在服务端进行智能分析评判。实现工程施工可视化智能管理，以提高工程管理信息化水平，从而逐步实现绿色建造和生态建造。

此系统旨在接受委托方项目委托，进行工地项目派工检查，通过 Android 端采集数据，Web 端进行管理，进行数据数字化采集和分析。

## 系统功能

1. 项目管理：
   委托方是系统使用单位直接面对对象，通过和委托方签订合同，对委托方下的项目进行派工检查，对于每一个委托方，可签订多个项目，所有检查都以项目为基本单位进行。
    - 委托方合同管理，包括新建委托方合同信息、查看合同信息、编辑和删除。委托方合同信息包括：委托方名称、委托方意向、合同编号、合同创建日期等。
    - 项目信息管理，包括新建项目（每次新建项目必须且只能选择一个委托方）、项目编辑、删除等。项目信息包括：委托方、项目类型、项目经理、项目状态（进行中/已完成）、项目创建时间等。
    - 现场检查结果，根据项目状态和创建时间，选择对应的项目，根据项目的检查体系查看项目检查结果。
    - 项目创建时，需指派一个检查小组。
2. 检查体系：
   检查体系是一个树状结构，是项目创建时的分类依据，每个项目创建时可选择多个检查体系（只选择第一级）。
    - 检查体系第一级分为安全检查、质量检查等，权重之和为百分之百。具体功能包括增加、编辑和删除。
    - 检查体系第二级为前一级的具体分项，权重之和为百分之百，要求功能同上。
3. 人员管理：
   项目检查是人工进行现场检查，需要进行合理的小组人员管理。
    - 人员录入界面，每个检察人员有唯一员工号，根据员工号进行人员区分。
    - 小组创建时从全部检察人员中进行添加（同一员工，可加入多个检查小组），每个检查小组指派不超过 3 个小组组长。
    - 小组管理，每个检查项目，指派一个小组进行检查（同一小组可检查多个项目），组员和组长均可提交检查结果，组长可设置项目检查状态。
4. 现场检查
   现场检查使用 Android 端录入并提交数据，每个检查人员进行一次检查后，生成一个现场检查记录，一个项目对应多条项目检查记录，每条检查只能选择一个体系分支。
    - 项目创建完成后，在工地现场进行项目检查，依次选择委托方、项目、体系，并在手机端填写检查部位和现场存在的问题。
    - 对于存在的问题项，拍照上传。
    - 根据现场问题情况，检察人员对问题进行风险评估，分为轻度风险、一般风险和高危风险。
    - 点击提交后，在服务端进行暂存（即：在现场检查结果页面查看不到此条检查记录），每条检查记录，需要小组组长审核后进行提交。
5. 检查结果处理
    - 对于所有项目，可在 Web 端对检查数据进行分析，以图表形式展示，显示不同体系下该项目问题数量等。
    - 若项目已完成，根据体系权重和问题风险等级对此次项目进行自动风险值计算（风险值越高，项目危险程度越高）。
    - 可按照项目风险值进行项目排名。
6. 登陆注册界面  
   要求 Web 端和 Android 端均需登录，界面美观
7. 核心数据字典
    - 委托方合同信息表：委托方 ID、委托方描述等。
    - 项目信息表：项目 ID、委托方 ID、检查体系 ID、项目状态、项目风险值、项目创建时间、项目描述、项目负责人等。
    - 检查信息表：检查 ID、项目 ID、检查体系第一级 ID、第二级 ID、问题描述等。
    - 检查体系表：当前结点 ID、前置结点 ID（第一级改字段为 0）等。
    - 人员信息表：员工 ID、员工姓名等。
    - 小组成员表：小组 ID、员工 ID、组长标志等。
