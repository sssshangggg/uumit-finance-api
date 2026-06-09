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

# 30 products part 3: Health, Personal Finance, Parenting, Language, Travel, Food & more
new_products = [
    # === 健康 & 健身 (3) ===
    {
        "title": "家庭常备药品与急救指南（OTC药物清单+常见症状自查+急救SOP）",
        "description": "每个家庭都需要的健康应急手册。包含：家庭药箱配置清单（成人/儿童/老人分层推荐）、50种常见OTC药物的功效/用法/禁忌速查、常见症状自查流程图（发烧/头痛/腹痛/过敏/皮肤问题）、急救操作SOP（烫伤/割伤/扭伤/异物卡喉/心脏骤停）、就医时机判断指南（什么情况必须去医院）。附录：儿童用药剂量换算表和药物相互作用警示。",
        "category": "digital_asset", "tags": ["健康", "急救", "家庭", "用药"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "居家健身完全方案（无器械+弹力带+哑铃三阶训练计划）",
        "description": "在家就能练出好身材的系统训练方案。三阶递进：新手入门（15分钟/天×21天全身激活）、进阶塑形（30分钟/天×30天分部训练）、高阶雕刻（45分钟/天×30天精准塑形）。每个动作含：标准动作图解、常见错误纠正、退阶/进阶变式。另附：训练前后拉伸完整序列、不同目标（减脂/增肌/塑形）的饮食搭配方案、每周训练排课表、每月体测追踪模板。",
        "category": "digital_asset", "tags": ["健身", "运动", "健康", "减脂"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "睡眠改善完全指南（CBT-I疗法+睡眠卫生+环境优化方案）",
        "description": "基于认知行为疗法的科学睡眠改善方案。包含：睡眠评估问卷（匹兹堡睡眠质量指数+Epworth嗜睡量表）、CBT-I核心方法（刺激控制/睡眠限制/认知重构/放松训练）、睡眠卫生10条黄金法则、卧室环境优化指南（光线/温度/噪音/床品选择）、睡前仪式设计（不同睡眠类型的时间安排）、饮食与运动对睡眠的影响速查。附21天睡眠改善打卡表和每周睡眠数据分析模板。",
        "category": "digital_asset", "tags": ["睡眠", "健康", "心理健康", "生活方式"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    # === 个人理财 (2) ===
    {
        "title": "个人财务管理入门指南（记账+预算+储蓄+保险四步法）",
        "description": "从月光族到财务自由的入门路径。记账篇：支出分类体系（必要/需要/想要三层分类）+月度财务复盘模板；预算篇：50/30/20法则实操（含不同收入水平的个性化调整）；储蓄篇：紧急备用金规划（3-6个月生活开支计算方法）+自动化储蓄系统搭建；保险篇：人生不同阶段的保险配置方案（医疗/重疾/意外/寿险/年金）。附带个人资产负债表模板和财务自由进度追踪器。",
        "category": "digital_asset", "tags": ["理财", "储蓄", "保险", "财务规划"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "基金定投实战指南（选基方法+组合配置+止盈策略全流程）",
        "description": "适合普通投资者的基金定投完全手册。选基篇：4433选基法+晨星评级解读+基金经理评估维度（从业年限/历史回报/最大回撤/管理规模）；配置篇：核心-卫星组合策略（宽基指数+行业主题+债券基金比例配置）、不同风险偏好的组合模板；操作篇：定投频率与金额优化、智能定投vs普通定投对比、市场高估/低估时的调仓策略；止盈篇：目标收益率法/估值分位法/最大回撤法三种止盈策略对比。",
        "category": "digital_asset", "tags": ["基金", "定投", "理财", "投资"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    # === 育儿 & 教育 (3) ===
    {
        "title": "0-3岁科学育儿完全指南（分月龄发育+早教游戏+喂养方案）",
        "description": "新手父母的育儿百科全书。按月龄分段（0-3月/4-6月/7-9月/10-12月/13-18月/19-24月/25-36月），每个阶段包含：发育里程碑自查表（大运动/精细动作/语言/社交/认知五个维度）、适龄早教游戏（每阶段10个在家可做的游戏）、喂养方案（母乳/配方奶/辅食添加时间表+食谱）、睡眠规律培养方法、常见问题应对（肠绞痛/出牙/分离焦虑/如厕训练）。",
        "category": "digital_asset", "tags": ["育儿", "早教", "新手父母", "婴儿"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "3-12岁儿童兴趣班选择指南（20种兴趣班评测+年龄匹配+费用参考）",
        "description": "帮家长科学选择孩子的课外兴趣班。评测维度：适合起始年龄/能力培养（体能/思维/审美/社交）/长期发展路径/考级与竞赛体系/费用预算（课时费+器材+考级+比赛）。覆盖20种主流兴趣班：钢琴/小提琴/绘画/舞蹈/书法/围棋/编程/机器人/篮球/游泳/跆拳道/轮滑/演讲/英语戏剧/乐高/象棋/古筝/合唱团/科学实验/马术。附：不同年龄段兴趣班组合推荐和多孩家庭时间管理方案。",
        "category": "digital_asset", "tags": ["兴趣班", "育儿", "教育", "儿童"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "K12学习方法全攻略（记忆术+笔记法+考试技巧+时间管理）",
        "description": "帮助中小学生提升学习效率的系统方法。记忆篇：艾宾浩斯遗忘曲线应用/记忆宫殿法/联想记忆法；笔记篇：康奈尔笔记法/思维导图法/东京大学笔记法实例；考试篇：各科应试技巧（语文阅读理解模板/数学解题步骤规范/英语完形填空策略）、考试焦虑应对方案、错题本高效使用方法；时间管理：番茄工作法学生版/周末学习计划表/寒暑假弯道超车攻略。",
        "category": "digital_asset", "tags": ["学习方法", "K12", "考试", "教育"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    # === 语言学习 (1) ===
    {
        "title": "英语自学完全路线图（零基础到流利阅读+听说突破方案）",
        "description": "不报班、不请外教的自学英语体系化方案。分级递进：入门级(CEFR A1-A2)学习资源清单+60天计划、进阶级(B1-B2)听说读写四项分训方案、高阶级(C1)学术和商务英语专项突破。核心方法：影子跟读法训练口语、精读+泛读结合提升阅读、Anki间隔重复记忆单词、英语播客/纪录片/美剧学习指南。附：1000个高频核心词汇表、30个即用口语模板、英语写作Checklist。",
        "category": "digital_asset", "tags": ["英语", "自学", "语言", "学习"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    # === 旅游 & 出行 (2) ===
    {
        "title": "中国自驾游全攻略（20条经典路线+路书+营地+车辆准备）",
        "description": "自驾游爱好者的路线百科全书。20条经典自驾路线：川藏线/青藏线/独库公路/草原天路/海南环岛/云南大环线/丝绸之路/东北冰雪线/江南古镇线/湘西秘境线等。每条路线含：分段行程规划（每日里程/驾驶时长/海拔变化）、沿途景点推荐、住宿与露营地点、加油站与充电桩分布、最佳出行季节。车辆准备：长途自驾检查清单/应急工具包/高原驾驶注意事项。",
        "category": "digital_asset", "tags": ["自驾游", "旅行", "攻略", "户外"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "出境自由行全流程规划手册（签证+机票+住宿+行程一站搞定）",
        "description": "从决定出发到平安归来的出境游规划系统。行前准备：签证办理攻略（15个热门目的地签证要求速查）/机票比价策略（淡旺季/中转方案/里程兑换）/住宿选择指南（不同旅行方式的住宿方案）；行程规划：经典行程模板（日本7天/泰国10天/欧洲14天等5条路线）/当地交通攻略/美食推荐数据库；实用锦囊：境外支付方案/通信上网方案/安全注意事项/紧急情况处理SOP。附行李打包清单和每日花费记账表。",
        "category": "digital_asset", "tags": ["出境游", "旅行", "签证", "攻略"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
]

print(json.dumps({"count": len(new_products)}, ensure_ascii=False))