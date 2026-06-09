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

# 30 products part 2: Marketing, Design, Health, Real Estate
new_products = [
    # === 营销 & 销售 (5) ===
    {
        "title": "小红书种草笔记全流程SOP（选题+文案+图片+投放一体化）",
        "description": "从零做出爆款种草笔记的系统方法论。包含：产品卖点挖掘四步法（功能点/情感点/场景点/差异化）、种草文案写作公式（痛点引入+产品体验+效果展示+引导互动）、高点击封面图设计规范（配色/构图/文字排版）、关键词布局策略（标题词/正文词/标签词三级覆盖）、投放数据复盘模板（曝光/点击/互动/转化四维分析）。附30个爆款笔记拆解案例。",
        "category": "digital_asset", "tags": ["种草", "内容营销", "电商", "文案"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "SEO关键词研究全流程工具包（长尾词挖掘+竞品分析+排名追踪）",
        "description": "搜索引擎优化从关键词研究到效果追踪的完整工具链。包含：种子词扩展方法（搜索引擎提示词/相关搜索/People Also Ask）、长尾关键词筛选标准（搜索量/竞争度/商业价值三维评分）、竞品关键词反向分析（使用SEMrush/Ahrefs数据解读方法）、内容优化Checklist（标题/描述/H标签/内链/图片ALT）、排名监控与迭代策略。",
        "category": "digital_asset", "tags": ["SEO", "关键词", "搜索引擎", "流量"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "社群运营完全手册（拉新+活跃+转化+防死群四步法）",
        "description": "从建群到变现的社群运营全流程。拉新：6种低成本获客方法（内容引流/活动裂变/KOC合作/跨群互推/搜索截流/付费投放）；活跃：每日话题策划+每周活动日历+积分激励机制；转化：信任建设四阶段（认知/兴趣/信任/下单）+社群专属优惠设计；防死群：潜水用户唤醒策略+社群生命周期管理。附50个社群话题模板和20个互动游戏。",
        "category": "digital_asset", "tags": ["社群运营", "用户增长", "私域", "营销"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "短视频拍摄剪辑零基础教程（手机拍摄+剪映剪辑+爆款套路）",
        "description": "一部手机搞定短视频从拍摄到发布的全流程。拍摄篇：构图法则/光线运用/运镜技巧/收音方案/场景布置；剪辑篇：剪映完整教程（分割/转场/滤镜/字幕/贴纸/画中画/关键帧/蒙版/调色）；爆款篇：黄金前3秒设计/信息密度节奏/BGM情绪匹配/评论区运营。附10个不同赛道的完整仿拍案例（美食/美妆/穿搭/知识/剧情/Vlog）。",
        "category": "digital_asset", "tags": ["短视频", "剪辑", "拍摄", "自媒体"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "品牌营销策划全案模板（定位+策略+执行+复盘四件套）",
        "description": "甲方和乙方通用的品牌营销策划标准模板。包含：品牌定位画布（目标用户/核心价值/差异化/品牌人格）、年度营销策略框架（预算分配/渠道组合/KPI体系）、Campaign执行SOP（预热期/爆发期/延续期三阶段操作手册）、效果复盘报告模板（ROI计算/渠道归因/用户反馈分析/优化建议）。附5个真实品牌案例全案拆解。",
        "category": "digital_asset", "tags": ["品牌营销", "策划", "方案", "市场"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    # === 设计 & 创意 (3) ===
    {
        "title": "UI设计规范系统手册（组件库+设计Token+设计系统从0到1）",
        "description": "从零搭建产品设计系统的完整指南。包含：设计原则定义方法（一致性/可访问性/响应式）、Design Token体系搭建（颜色/字体/间距/圆角/阴影/动效参数化）、组件库构建（按钮/输入框/卡片/导航/弹窗/表格 50+组件规范）、设计稿到代码的交接流程（Figma插件+自动标注+CSS变量导出）、设计系统的版本管理与迭代策略。",
        "category": "digital_asset", "tags": ["UI设计", "设计系统", "组件库", "Figma"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "PPT高级设计速成指南（麦肯锡/咨询公司级幻灯片制作）",
        "description": "做出让老板和客户惊艳的演示文稿。结构化思维篇：金字塔原理/MECE法则/SCQA故事框架；视觉设计篇：配色方案库（20套行业专属配色）/字体搭配指南/图表美化技巧/数据可视化最佳实践；效率工具篇：母版设置/快捷键大全/插件推荐/模板管理。附30套可直接使用的行业模板（战略/融资/产品/运营/市场/人力/技术）。",
        "category": "digital_asset", "tags": ["PPT", "演示", "设计", "咨询"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    {
        "title": "Logo设计入门到精通（从草图到交付的专业流程）",
        "description": "设计师和创业者的Logo设计完全指南。内容涵盖：品牌策略分析（行业调研/竞品分析/品牌人格提炼）、创意发散方法（思维导图/情绪板/关键词视觉化）、草图到矢量化的完整流程、字体Logo设计原则（衬线/无衬线/手写/定制字体选择）、色彩心理学应用、不同场景的Logo规范（网站/印刷/社交媒体/包装）、Logo设计交付物清单与报价指南。",
        "category": "digital_asset", "tags": ["Logo", "品牌设计", "设计", "VI"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 2900, "has_deliverable": True,
    },
    # === 房产 & 装修 (2) ===
    {
        "title": "买房避坑完全手册（看房200项检查清单+谈判策略+贷款攻略）",
        "description": "买房全流程实操指南，帮首次购房者避开90%的坑。看房篇：200项房屋检查清单（结构/水电/采光/隔音/物业/周边配套）、不同楼层的优劣势对比表、户型图解读方法；谈判篇：二手房砍价策略（市场数据/历史成交价/房屋缺陷作为筹码）、新房折扣获取技巧；贷款篇：商贷vs公积金组合贷计算器、等额本息vs等额本金对比、提前还款策略。附全国主要城市购房政策速查表。",
        "category": "digital_asset", "tags": ["买房", "房产", "投资", "避坑"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
    {
        "title": "装修预算与施工监督全流程指南（预算控制+工艺标准+验收清单）",
        "description": "装修小白变专家的实战手册。预算篇：装修预算表模板（硬装/软装/家电/家具四类分项）、不同档位装修价格参考（简装/精装/豪装）、隐蔽工程增项预警清单；工艺篇：水电/泥瓦/木工/油漆/安装五大工序验收标准（含图文说明）、常见偷工减料手法识别；流程篇：装修全流程时间线（拆改→水电→泥瓦→木工→油漆→安装→软装）、与装修公司/工长沟通话术模板。",
        "category": "digital_asset", "tags": ["装修", "家居", "预算", "避坑"], "capability_type": "data", "delivery_mode": "instant", "pricing_model": "fixed", "price_ut": 3900, "has_deliverable": True,
    },
]

print(json.dumps({"count": len(new_products)}, ensure_ascii=False))