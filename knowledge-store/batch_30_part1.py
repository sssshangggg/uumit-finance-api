import json, httpx, os
from dotenv import load_dotenv
load_dotenv(r"C:\Users\MECHREVO\Documents\UUMit\finance-data-service\.env")

UUMIT_API_KEY = os.getenv("UUMIT_API_KEY")
UUMIT_USER_ID = os.getenv("UUMIT_USER_ID")
API_BASE = "https://api.uumit.com"
url = f"{API_BASE}/api/v1/capabilities"
headers = {
    "X-Api-Key": UUMIT_API_KEY,
    "X-Platform-User-Id": UUMIT_USER_ID,
    "Content-Type": "application/json",
}

# 30 new products across underserved categories
new_products = [
    # === 编程 & 技术 (5) ===
    {
        "title": "Python自动化办公实战手册（Excel/PDF/Word/邮件一键处理）",
        "description": "面向零基础职场人士的Python自动化教程。覆盖四大高频场景：Excel批量处理（合并/拆分/透视/图表）、PDF提取与生成、Word模板填充、邮件自动发送。每章配有可运行代码和真实案例。附赠20个即用脚本模板。7天学习计划，每天30分钟，学完即可独立编写自动化脚本。",
        "category": "digital_asset", "tags": ["Python", "自动化", "办公效率", "Excel", "编程"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "SQL从入门到实战（50道高频面试题+真实业务场景）",
        "description": "数据分析师必备SQL技能全攻略。从SELECT基础到窗口函数、多表JOIN、子查询优化，全程配真实业务场景数据。包含：50道大厂高频SQL面试题及详解、电商/金融/游戏三个行业实战数据集、执行计划解读与性能优化技巧。适合转行数据分析、准备技术面试的求职者。",
        "category": "digital_asset", "tags": ["SQL", "数据分析", "面试", "数据库", "编程"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "独立开发者出海技术栈指南（全栈SaaS搭建+支付+部署）",
        "description": "面向个人开发者的全栈SaaS出海实战指南。技术选型：Next.js/React前端 + Node.js/Python后端 + Supabase数据库 + Stripe支付 + Vercel部署。内容覆盖：项目脚手架搭建、用户认证系统、订阅支付集成、国际化(i18n)、SEO优化、性能监控。附完整代码仓库和部署检查清单。",
        "category": "digital_asset", "tags": ["独立开发", "SaaS", "全栈", "出海", "Stripe"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "Prompt Engineering系统教程（30个高级技巧+10个行业模板）",
        "description": "从会用AI到用好AI的进阶指南。覆盖：思维链(Chain-of-Thought)、少样本学习(Few-Shot)、角色扮演、结构化输出、迭代优化等30个高级提示词技巧。含10个行业专用模板：法律文书/医疗问诊/教育教案/金融分析/代码生成/文案创作/翻译润色/数据标注/客服话术/产品需求。每个模板配正反案例对比。",
        "category": "digital_asset", "tags": ["Prompt", "AI", "提示词工程", "效率工具", "模板"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "常用API接口速查手册（50+免费API+调用示例+额度说明）",
        "description": "开发者和产品经理的API字典。精选50+高质量免费API，按类别整理：天气/地图/翻译/金融数据/新闻资讯/AI模型/图像处理/短信邮件/社交媒体/电商数据。每个API包含：接口说明、免费额度、调用示例代码(Python/JavaScript)、常见报错处理。附带API选型决策树和替代方案对比表。",
        "category": "digital_asset", "tags": ["API", "开发工具", "免费资源", "接口"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 1900, "has_deliverable": True,
    },
    # === 职场 & 求职 (4) ===
    {
        "title": "薪资谈判完全指南（话术模板+行业数据+心理策略）",
        "description": "帮你多谈20%-50%薪资的系统方法论。内容覆盖：面试前薪资调研（如何获取真实薪资范围）、期望薪资应答话术（5种场景模板）、offer比较框架（总包计算器含股权/奖金/福利折算）、提离职与counter-offer应对策略、试用期谈薪时机把握。附带互联网/金融/咨询三大行业2026薪资基准数据。",
        "category": "digital_asset", "tags": ["薪资谈判", "求职", "面试", "职场", "职业发展"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "远程工作完全指南（找远程工作+高效协作+避坑清单）",
        "description": "数字游民和远程工作者的实战手册。包含：全球50+远程招聘平台评测（薪资水平/岗位类型/申请难度）、远程面试准备（时区协调/虚拟白板/异步沟通技巧）、远程协作工具链（项目管理/文档协作/视频会议/时间追踪）、远程工作税务与合规（跨境支付/社保/个税处理）、远程孤独感应对与精力管理。",
        "category": "digital_asset", "tags": ["远程工作", "数字游民", "自由职业", "求职"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "管理者的第一年（从IC到Manager的90天转型计划）",
        "description": "技术人员转型管理者的实操手册。90天分阶段计划：前30天（建立信任与了解团队）、中30天（设定目标与流程优化）、后30天（授权与团队文化建设）。核心模块：一对一会议指南、绩效反馈框架、冲突调解SOP、向上管理技巧、技术债务与业务需求的平衡策略。附管理者的每周自检清单。",
        "category": "digital_asset", "tags": ["管理", "职业发展", "领导力", "团队管理"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "副业赚钱完全指南（20个低门槛副业+启动SOP+收入预估）",
        "description": "零基础可启动的副业实操手册。20个副业方向详细拆解：知识付费/社群运营/AI工具变现/设计接单/翻译/配音/摄影/探店/测评/二手交易/资料整理/代运营/咨询/培训/自媒体/电商/编程外包/数据标注/问卷调查/体验测评。每个方向含：启动成本、所需技能、收入预估、获客渠道、避坑指南。附带副业组合矩阵（主业协同型vs兴趣变现型）。",
        "category": "digital_asset", "tags": ["副业", "赚钱", "自由职业", "创业"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
]

print(json.dumps({"count": len(new_products)}, ensure_ascii=False))