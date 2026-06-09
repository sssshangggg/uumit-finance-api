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

all_products = []

# === Part 1: Programming & Career (9) ===
all_products += [
    {"title": "Python自动化办公实战手册（Excel/PDF/Word/邮件一键处理）","description": "面向零基础职场人士的Python自动化教程。覆盖四大高频场景：Excel批量处理（合并/拆分/透视/图表）、PDF提取与生成、Word模板填充、邮件自动发送。每章配有可运行代码和真实案例。附赠20个即用脚本模板。7天学习计划，每天30分钟，学完即可独立编写自动化脚本。","category": "digital_asset","tags": ["Python","自动化","办公效率","Excel","编程"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "SQL从入门到实战（50道高频面试题+真实业务场景）","description": "数据分析师必备SQL技能全攻略。从SELECT基础到窗口函数、多表JOIN、子查询优化，全程配真实业务场景数据。包含：50道大厂高频SQL面试题及详解、电商/金融/游戏三个行业实战数据集、执行计划解读与性能优化技巧。适合转行数据分析、准备技术面试的求职者。","category": "digital_asset","tags": ["SQL","数据分析","面试","数据库","编程"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "独立开发者出海技术栈指南（全栈SaaS搭建+支付+部署）","description": "面向个人开发者的全栈SaaS出海实战指南。技术选型：前端框架+后端框架+数据库+支付集成+部署平台。内容覆盖：项目脚手架搭建、用户认证系统、订阅支付集成、国际化方案、SEO优化、性能监控。附完整代码仓库和部署检查清单。","category": "digital_asset","tags": ["独立开发","SaaS","全栈","出海","技术"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "Prompt Engineering系统教程（30个高级技巧+10个行业模板）","description": "从会用AI到用好AI的进阶指南。覆盖：思维链、少样本学习、角色扮演、结构化输出、迭代优化等30个高级提示词技巧。含10个行业专用模板：法律文书/医疗问诊/教育教案/金融分析/代码生成/文案创作/翻译润色/数据标注/客服话术/产品需求。每个模板配正反案例对比。","category": "digital_asset","tags": ["Prompt","AI","提示词工程","效率工具","模板"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "常用API接口速查手册（50+免费API+调用示例+额度说明）","description": "开发者和产品经理的API字典。精选50+高质量免费API，按类别整理：天气/地图/翻译/金融数据/新闻资讯/AI模型/图像处理/短信邮件/社交媒体/电商数据。每个API包含：接口说明、免费额度、调用示例代码、常见报错处理。附带API选型决策树和替代方案对比表。","category": "digital_asset","tags": ["API","开发工具","免费资源","接口"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 1900,"has_deliverable": True},
    {"title": "薪资谈判完全指南（话术模板+行业数据+心理策略）","description": "帮你多谈薪资的系统方法论。内容覆盖：面试前薪资调研方法、期望薪资应答话术（5种场景模板）、offer比较框架（总包计算器含股权/奖金/福利折算）、离职与counter-offer应对策略、试用期谈薪时机把握。附带互联网/金融/咨询三大行业2026薪资基准数据。","category": "digital_asset","tags": ["薪资谈判","求职","面试","职场","职业发展"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "远程工作完全指南（找远程工作+高效协作+避坑清单）","description": "数字游民和远程工作者的实战手册。包含：全球远程招聘平台评测、远程面试准备（时区协调/虚拟白板/异步沟通技巧）、远程协作工具链、远程工作税务与合规处理、远程孤独感应对与精力管理。附带每日远程工作日程模板和效率自评表。","category": "digital_asset","tags": ["远程工作","数字游民","自由职业","求职"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "管理者的第一年（从IC到Manager的90天转型计划）","description": "技术人员转型管理者的实操手册。90天分阶段计划：前30天建立信任与了解团队、中30天设定目标与流程优化、后30天授权与团队文化建设。核心模块：一对一会议指南、绩效反馈框架、冲突调解SOP、向上管理技巧、技术债务与业务需求的平衡策略。附管理者的每周自检清单。","category": "digital_asset","tags": ["管理","职业发展","领导力","团队管理"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "副业赚钱完全指南（20个低门槛副业+启动SOP+收入预估）","description": "零基础可启动的副业实操手册。20个副业方向详细拆解：知识付费/社群运营/设计接单/翻译/配音/摄影/测评/二手交易/资料整理/代运营/咨询/培训/内容创作/电商/编程外包/数据标注等。每个方向含：启动成本、所需技能、收入预估、获客渠道、避坑指南。附带副业组合矩阵（主业协同型vs兴趣变现型）。","category": "digital_asset","tags": ["副业","赚钱","自由职业","创业"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
]

# === Part 2: Marketing, Design, Real Estate (10) ===
all_products += [
    {"title": "内容种草笔记全流程SOP（选题+文案+图片+投放一体化）","description": "从零做出爆款种草笔记的系统方法论。包含：产品卖点挖掘四步法（功能点/情感点/场景点/差异化）、种草文案写作公式（痛点引入+产品体验+效果展示+引导互动）、高点击封面图设计规范、关键词布局策略、投放数据复盘模板。附30个爆款笔记拆解案例。","category": "digital_asset","tags": ["种草","内容营销","电商","文案","运营"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "SEO关键词研究全流程工具包（长尾词挖掘+竞品分析+排名追踪）","description": "搜索引擎优化从关键词研究到效果追踪的完整工具链。包含：种子词扩展方法、长尾关键词筛选标准（搜索量/竞争度/商业价值三维评分）、竞品关键词反向分析方法、内容优化Checklist、排名监控与迭代策略。附带各行业关键词难度基准数据。","category": "digital_asset","tags": ["SEO","关键词","搜索引擎","流量","优化"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "社群运营完全手册（拉新+活跃+转化+防流失四步法）","description": "从建群到变现的社群运营全流程。拉新：6种低成本获客方法（内容引流/活动裂变/KOC合作/跨群互推/搜索截流/付费投放）；活跃：每日话题策划+每周活动日历+积分激励机制；转化：信任建设四阶段+社群专属优惠设计；防流失：潜水用户唤醒策略+社群生命周期管理。附50个社群话题模板和20个互动游戏。","category": "digital_asset","tags": ["社群运营","用户增长","营销","客户管理"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "短视频拍摄剪辑零基础教程（手机拍摄+剪辑软件+爆款套路）","description": "一部手机搞定短视频从拍摄到发布的全流程。拍摄篇：构图法则/光线运用/运镜技巧/收音方案/场景布置；剪辑篇：剪辑软件完整教程（分割/转场/滤镜/字幕/贴纸/画中画/关键帧/蒙版/调色）；爆款篇：黄金前3秒设计/信息密度节奏/BGM情绪匹配/评论区运营。附10个不同赛道的完整仿拍案例。","category": "digital_asset","tags": ["短视频","剪辑","拍摄","内容创作","视频"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "品牌营销策划全案模板（定位+策略+执行+复盘四件套）","description": "品牌营销策划标准模板。包含：品牌定位画布（目标用户/核心价值/差异化/品牌人格）、年度营销策略框架（预算分配/渠道组合/KPI体系）、活动执行SOP（预热期/爆发期/延续期三阶段操作手册）、效果复盘报告模板（ROI计算/渠道归因/用户反馈分析/优化建议）。附5个真实品牌案例全案拆解。","category": "digital_asset","tags": ["品牌营销","策划","方案","市场","推广"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "UI设计规范系统手册（组件库+设计规范+设计系统从0到1）","description": "从零搭建产品设计系统的完整指南。包含：设计原则定义方法（一致性/可访问性/响应式）、设计规范体系搭建（颜色/字体/间距/圆角/阴影/动效参数化）、组件库构建（按钮/输入框/卡片/导航/弹窗/表格等50+组件规范）、设计稿到代码的交接流程、设计系统的版本管理与迭代策略。","category": "digital_asset","tags": ["UI设计","设计系统","组件库","产品设计"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "PPT高级设计速成指南（咨询公司级幻灯片制作方法论）","description": "做出让人眼前一亮的演示文稿。结构化思维篇：金字塔原理/逻辑框架/故事叙述方法；视觉设计篇：配色方案库（20套行业专属配色）/字体搭配指南/图表美化技巧/数据可视化实践；效率工具篇：母版设置/快捷键大全/插件推荐/模板管理。附30套可直接使用的行业模板。","category": "digital_asset","tags": ["PPT","演示","设计","办公技能"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "Logo设计入门到精通（从草图到交付的专业流程）","description": "设计师和创业者的Logo设计完全指南。内容涵盖：品牌策略分析（行业调研/竞品分析/品牌人格提炼）、创意发散方法（思维导图/情绪板/关键词视觉化）、草图到矢量化的完整流程、字体Logo设计原则、色彩心理学应用、不同场景的Logo规范、Logo设计交付物清单与报价指南。","category": "digital_asset","tags": ["Logo","品牌设计","设计","视觉"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "买房避坑完全手册（看房检查清单+谈判策略+贷款攻略）","description": "买房全流程实操指南。看房篇：200项房屋检查清单（结构/水电/采光/隔音/物业/周边配套）、户型图解读方法；谈判篇：二手房议价策略、新房折扣获取技巧；贷款篇：商贷与公积金组合对比、等额本息与等额本金选择、提前还款策略。附主要城市购房政策速查表。","category": "digital_asset","tags": ["买房","房产","投资","避坑","贷款"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "装修预算与施工监督全流程指南（预算控制+工艺标准+验收清单）","description": "装修小白变专家的实战手册。预算篇：装修预算表模板（硬装/软装/家电/家具四类分项）、不同档位装修价格参考、隐蔽工程增项预警清单；工艺篇：五大工序验收标准（含图文说明）、常见偷工减料手法识别；流程篇：装修全流程时间线、与装修方沟通话术模板。附材料采购比价表。","category": "digital_asset","tags": ["装修","家居","预算","避坑","施工"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
]

# === Part 3: Health, Finance, Parenting, Language, Travel (11) ===
all_products += [
    {"title": "家庭常备药品与急救指南（药品清单+常见症状自查+急救方法）","description": "每个家庭都需要的健康应急手册。包含：家庭药箱配置清单（成人/儿童/老人分层推荐）、常见非处方药物的功效与用法速查、常见症状自查流程图（发烧/头痛/腹痛/过敏/皮肤问题）、急救操作方法（烫伤/割伤/扭伤/异物卡喉等）、就医时机判断指南。附录：儿童用药剂量换算表和药物相互作用警示。","category": "digital_asset","tags": ["健康","急救","家庭","用药","安全"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "居家健身完全方案（无器械+弹力带+哑铃三阶训练计划）","description": "在家就能练出好身材的系统训练方案。三阶递进：新手入门（15分钟/天全身激活）、进阶塑形（30分钟/天分部训练）、高阶雕刻（45分钟/天精准塑形）。每个动作含：标准动作图解、常见错误纠正、退阶与进阶变式。另附：训练前后拉伸完整序列、不同目标的饮食搭配方案、每周训练排课表、每月体测追踪模板。","category": "digital_asset","tags": ["健身","运动","健康","减脂","塑形"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "睡眠改善完全指南（科学疗法+睡眠卫生+环境优化方案）","description": "基于认知行为疗法的科学睡眠改善方案。包含：睡眠质量评估问卷、核心改善方法（刺激控制/睡眠限制/认知重构/放松训练）、睡眠卫生黄金法则、卧室环境优化指南（光线/温度/噪音/床品选择）、睡前仪式设计、饮食与运动对睡眠的影响速查。附21天睡眠改善打卡表和每周数据分析模板。","category": "digital_asset","tags": ["睡眠","健康","心理健康","生活方式","改善"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "个人财务管理入门指南（记账+预算+储蓄+保险四步法）","description": "从零开始的个人财务管理系统。记账篇：支出分类体系+月度财务复盘模板；预算篇：收入分配法则实操（含不同收入水平的个性化调整）；储蓄篇：紧急备用金规划+自动化储蓄系统搭建；保险篇：人生不同阶段的保险配置方案（医疗/重疾/意外/寿险）。附带个人资产负债表模板和财务进度追踪器。","category": "digital_asset","tags": ["理财","储蓄","保险","财务规划","个人财务"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "基金定投实战指南（选基方法+组合配置+止盈策略全流程）","description": "适合普通投资者的基金定投完全手册。选基篇：选基方法+基金评级解读+基金经理评估维度（从业年限/历史回报/最大回撤/管理规模）；配置篇：核心-卫星组合策略、不同风险偏好的组合模板；操作篇：定投频率与金额优化、智能定投与普通定投对比、市场变化时的调仓策略；止盈篇：三种止盈策略对比。","category": "digital_asset","tags": ["基金","定投","理财","投资","财富管理"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "0-3岁科学育儿完全指南（分月龄发育+早教游戏+喂养方案）","description": "新手父母的育儿百科全书。按月龄分段（0-3月/4-6月/7-9月/10-12月/13-18月/19-24月/25-36月），每个阶段包含：发育里程碑自查表（大运动/精细动作/语言/社交/认知五个维度）、适龄早教游戏、喂养方案（母乳/配方奶/辅食添加时间表+食谱）、睡眠规律培养方法、常见问题应对（肠绞痛/出牙/分离焦虑/如厕训练）。","category": "digital_asset","tags": ["育儿","早教","新手父母","婴儿","喂养"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "3-12岁儿童兴趣班选择指南（20种兴趣班评测+年龄匹配+费用参考）","description": "帮家长科学选择孩子的课外兴趣班。评测维度：适合起始年龄/能力培养方向/长期发展路径/考级与竞赛体系/费用预算。覆盖20种主流兴趣班：钢琴/小提琴/绘画/舞蹈/书法/围棋/编程/机器人/篮球/游泳/跆拳道/轮滑/演讲/英语戏剧/乐高/象棋/古筝/合唱团/科学实验/马术。附不同年龄段兴趣班组合推荐。","category": "digital_asset","tags": ["兴趣班","育儿","教育","儿童","特长培养"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "K12学习方法全攻略（记忆术+笔记法+考试技巧+时间管理）","description": "帮助中小学生提升学习效率的系统方法。记忆篇：遗忘曲线应用/记忆技巧/联想记忆法；笔记篇：经典笔记法/思维导图法实例；考试篇：各科应试技巧、考试焦虑应对方案、错题本高效使用方法；时间管理：专注工作法学生版/周末学习计划表/寒暑假学习攻略。附各年级学习重点规划表。","category": "digital_asset","tags": ["学习方法","K12","考试","教育","效率"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "英语自学完全路线图（零基础到流利阅读+听说突破方案）","description": "不报班也能学好英语的体系化方案。分级递进：入门级学习资源清单+60天计划、进阶级听说读写四项分训方案、高阶级学术和商务英语专项突破。核心方法：影子跟读法训练口语、精读与泛读结合提升阅读、间隔重复记忆单词、播客与纪录片学习指南。附：核心词汇表、口语模板、写作检查清单。","category": "digital_asset","tags": ["英语","自学","语言","学习","教育"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
    {"title": "中国自驾游全攻略（20条经典路线+路书+营地+车辆准备）","description": "自驾游爱好者的路线百科全书。20条经典自驾路线涵盖：高原天路/草原穿越/海岸环线/古镇探秘/冰雪秘境等。每条路线含：分段行程规划（每日里程/驾驶时长/海拔变化）、沿途景点推荐、住宿与露营地点、加油站分布、最佳出行季节。车辆准备：长途自驾检查清单/应急工具包/特殊路况驾驶注意事项。","category": "digital_asset","tags": ["自驾游","旅行","攻略","户外","路线"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 3900,"has_deliverable": True},
    {"title": "出境自由行全流程规划手册（签证+机票+住宿+行程一站搞定）","description": "从决定出发到平安归来的出境游规划系统。行前准备：签证办理攻略（热门目的地签证要求速查）/机票比价策略/住宿选择指南；行程规划：经典行程模板（多条热门路线）/当地交通攻略/美食推荐；实用锦囊：境外支付方案/通信上网方案/安全注意事项/紧急情况处理。附行李打包清单和每日花费记账表。","category": "digital_asset","tags": ["出境游","旅行","签证","攻略","自由行"],"capability_type": "data","delivery_mode": "instant","pricing_model": "fixed","price_ut": 2900,"has_deliverable": True},
]

print(f"Total products to register: {len(all_products)}")

ok = fail = 0
failed_items = []
with httpx.Client(timeout=30) as client:
    for item in all_products:
        try:
            resp = client.post(url, json=item, headers=headers)
            if resp.status_code in (200, 201):
                data = resp.json()
                item_id = data.get("data", {}).get("id", "?")
                print(f"  [OK] {item['title'][:45]}... | {item['price_ut']} UT | id={item_id}")
                ok += 1
            else:
                print(f"  [FAIL] {item['title'][:35]}... | HTTP {resp.status_code} | {resp.text[:150]}")
                fail += 1
                failed_items.append({"title": item['title'], "status": resp.status_code, "body": resp.text[:200]})
        except Exception as e:
            print(f"  [ERR] {item['title'][:35]}... | {e}")
            fail += 1
            failed_items.append({"title": item['title'], "error": str(e)})

total_ut = sum(i['price_ut'] for i in all_products[:ok])
print(f"\n--- {ok} OK, {fail} FAIL ---")
print(f"Registered UT: {total_ut} = RMB {total_ut/100}")

if failed_items:
    print(f"\nFailed items:")
    for fi in failed_items:
        print(f"  {fi['title'][:40]}...")