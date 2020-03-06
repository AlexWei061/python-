from math import *
from flask.views import View
from flask import Blueprint, url_for, render_template, request, jsonify, send_from_directory
from flask_login import login_required
import os
import pymongo
from bson import json_util

app_api = Blueprint('app_api', __name__)

word_dict = {
"strategy" : "战略策略",
"Penny wise and pound foolish" : "因小失大",
"R&D entries" : "研发输入",
"new pfmn" : "新速度",
"MTBF" : "故障间隔平均时间",
"revision date" : "改良日期",
"age at revision" : "改良时的年龄",
"R&D costb" : "研发费用",
"marketing decision entries" : "营销决策输入",
"promo budget" : "宣传预算",
"sales budget" : "销售预算",
"computer prediction" : "电脑测试",
"your sales forecast" : "你的销售预测",
"gross revenue forecast" : "总销售额预测",
"variable cost" : "变动成本",
"contrib margin forecast" : "贡献边际预测",
"less promo & sales" : "减去宣传销售费用",
"automation level" : "自动化程度",
"distance" : "距离",
"units" : "单位",
"production decision entries" : "生产部门决策输入",
"schedule" : "进度表",
"unit sales forecast" : "销售数量预测",
"inventory on hand" : "手头现有库存量",
"production schedule" : "生产进度表",
"production after adj" : "调整后的生产",
"physical plant" : "生产厂房",
"1st shift capacity" : "第一轮班生产能力",
"buy/sell capacity" : "买卖能力",
"automation rating" : "自动化评分",
"new automation rating" : "新自动化评分",
"investment" : "投资额",
"plant improvements" : "厂房改善",
"total investment" : "总投资额",
"sales of plant & equipment" : "厂房和设备卖出",
"common stock" : "普通股票",
"shares outstanding" : "已发行股票",
"price per share" : "每股价格",
"earnings per share" : "每股收益",
"max stock issue" : "至多发行股票数量",
"dividend per share" : "每股分红",
"current debt" : "短期债务",
"interest rate" : "利率",
"due this year" : "今年到期",
"borrow" : "借入",
"cash positions" : "现金状况",
"long term debt" : "长期债务",
"retire long term debt" : "赎买长期债务",
"issue long term debt" : "发行长期债务",
"long term interest rate" : "长期利率",
"manimum issue this year" : "今年至多发行量",
"human resources decision entries" : "人力资源缺乏决策输入",
"workforce" : "劳动力",
"complement" : "定员人数",
"needed" : "所需",
"1st shift" : "第一轮班",
"2nd shift" : "第二轮班",
"overtime%" : "加班",
"Turnover rate" : "人才流失率",
"new employees" : "流失职工",
"producivity index" : "生产效率指数",
"recruiting cost" : "招聘费用",
"separation cost" : "流逝费用",
"total HR admin costs" : "人力资源管理成本",
"process management initiative" : "程序管理项目",
"CPI system" : "CPI系统管理",
"vendor/JIT" : "卖主/准时生产",
"quality initiative training" : "质量项目培训",
"channel support system" : "渠道支持系统",
"concurrent engineering" : "协作工程",
"TQM initiative" : "全面质量管理项目",
"benchmarking" : "基准",
"quality function deployment effort" : "质量功能展开项目",
"CCE/6-Sigma training" : "CCE/6-sigma培训",
"total expenditures" : "总支出",
"projected cumulative impacts" : "预计累计效果",
"material cost reduction" : "材料成本缩减量",
"labor cost reduction" : "人工成本减少",
"reduction R&D cycle time" : "研发周期时间减少",
"reduction in admin costs" : "人工成本减少",
"demand increase" : "需求增加",
"labor negotiation" : "劳工谈判",
"current constract" : "现行合同",
"labor demands" : "工人要求",
"negotiation position" : "谈判位置",
"ceiling" : "最高限度",
"hourly wage" : "小时工资",
"benefits" : "福利待遇",
"profit sharing" : "分红制",
"annual raise" : "每年加薪",
"Advisor" : "顾问",
"Board" : "董事会",
"Board director" : "董事",
"Bill of materials" : "物料清单",
"Business administration" : "管理者",
"Chairman" : "董事长",
"Consumer behavior study" : "消费者行为研究",
"Department" : "部门",
"Deputy General Manager" : "副总经理",
"Domestic sales department" : "国内销售部",
"Employee" : "雇员",
"Executive" : "执行董事",
"Chief executive officer" : "董事代表",
"Chief financial officer" : "财务总裁",
"Industry research and analysis" : "行业调查与分析",
"Input control" : "投入管理",
"Investment consultancy" : "投资咨询",
"Management consultancy" : "管理咨询",
"Material requirements planning" : "物料需求计划",
"Market entry and expansion" : "市场进入和扩展",
"Multinational enterprise" : "跨国企业",
"On-hand balance" : "现在库存量",
"Output control" : "产出控制",
"Overseas distribution" : "海外销售部",
"Private enterprise" : "私营企业",
"Project evaluation" : "项目评估",
"Project manager" : "项目经理",
"Sales administration department" : "销售管理部",
"Senior managing director" : "高级董事",
"Storage" : "保管、贮藏",
"Small and medium-size business" : "中小企业",
"Subsidiary" : "子公司",
"taxation" : "税务",
"Warehouse" : "仓库",
"Annual bonus" : "年终分红",
"Absence management" : "缺勤管理",
"Annual leave" : "年假",
"Career planning" : "职业规划",
"Career path" : "职业道路",
"Career cycle" : "职业周期",
"Core worker" : "核心员工",
"Defined benefit" : "固定福利",
"Direct financial compensation" : "直接经济报酬",
"Dismissal" : "解雇、开除",
"Employee turnover" : "员工流动",
"Effective working hour" : "有效工时",
"Employee compensation" : "职业报酬",
"Employee equity" : "员工公平",
"Employee surplus" : "员工过剩",
"Employment interview" : "求职面试",
"Five-day workweek" : "每周五天工作制",
"Flexible benefits programs" : "弹性福利计划",
"Insurance benefits" : "保险福利",
"Individual retirement account" : "个人退休账户",
"Incentive plan" : "激励计划",
"Local market conditions" : "地方劳动力市场",
"Merit pay" : "绩效工作",
"Merit raise" : "绩效加薪",
"Non financial compensation" : "非经济报酬",
"Occupational skill" : "职业技能",
"Operative employee" : "技术员工",
"Pay grade" : "工资等级",
"Performance analysis" : "工作绩效分析",
"Profit sharing" : "分红制",
"Resignation" : "辞职",
"Sick leave" : "病假",
"Social security" : "社会保障",
"Special award" : "特殊奖励",
"Standard hour plan" : "标准工时工资",
"Supplement pay benefits" : "补充报酬福利",
"Supplement unemployment benefits" : "补充失业福利",
"Workers' benefits" : "雇员福利",
"Unfair labor practice strike" : "不正当劳工活动罢工",
"Components" : "零件",
"Cost" : "成本费用",
"Components storage" : "零件库存",
"Daily production plan" : "日生产计划",
"Demand and supply" : "需求",
"Fixed costs" : "固定成本",
"Input" : "投入",
"Material cost" : "物料花费",
"Operation scheduling" : "生产计划",
"Over production" : "生产过剩",
"Output" : "产出、产量",
"Production department" : "生产部门",
"Product line" : "生产线",
"Production capacity" : "生产力",
"Purchasing management" : "采购管理",
"Production rate" : "生产率",
"Quality control" : "质量控制",
"Raw materials" : "原料",
"Supply" : "供应",
"Sample" : "样品",
"Safe stock" : "安全库存",
"Transportation" : "运输",
"Transport costs" : "运输成本",
"Unit per hour" : "每小时的产出",
"Add agent" : "增加代理商",
"High market share global strategy" : "高市场份额全球战略",
"Imitative strategy" : "模仿战略",
"Initial agent" : "首个代理商",
"Industry attractiveness" : "行业吸引力",
"Industry dynamics" : "产业动态",
"Industry evaluation" : "产业评估",
"Internal marketing" : "内部营销",
"Inventory level" : "库存水平",
"Key accounts" : "关键客户",
"List price" : "产品定价",
"Low cost position" : "低成本地位",
"Manufacturers' agents" : "生产代理商",
"Market circumstances" : "市场环境",
"Market dimension" : "市场量度",
"Market entry strategies" : "市场进入战略",
"Market expansion strategies" : "市场扩张战略",
"Market research" : "市场调查",
"Marketing channel" : "营销渠道",
"Marketing management" : "营销管理",
"New market" : "新市场",
"Performance objectives" : "绩效目标",
"Performance standards" : "绩效标准",
"Potential market" : "潜在市场",
"Potential customers" : "潜在客户",
"Power of buyers" : "购买者能力",
"Post purchase" : "售后",
"Pay-off control" : "支出控制",
"Product specification" : "产品规格",
"Pre-test market research" : "测试前市场研究",
"Price promotion" : "价格促销",
"Pricing policies" : "价格策略",
"Promotion mix" : "促销组合",
"Purchasing agent" : "采购代理",
"Received order" : "接受订单数",
"Remove agent" : "减少代理商",
"Sales force" : "销售队伍",
"Stock level" : "存货水平",
"Satisfied order" : "生产订单数",
}


# 连接到mongodb
def connect_db(dbname):
    MONGO_URI = "mongodb://127.0.0.1:27017/"
    client = pymongo.MongoClient(MONGO_URI)
    db = client[dbname]
    return db


def find_data(col, all=True, filter=None):
    # filter = {"tagname":"Code"}  #example filter

    mydb = connect_db("alex_db")
    if all == True:
        return mydb[col].find()
    else:
        return mydb[col].find(filter)


def add_new_web(col, web):
    mydb = connect_db("alex_db")
    mydb[col].update_one({"tagname": web["tag"]},
                         {"$push": {"webs": {"$each": [{"webname": web['name'], "url": web['url']}]}}})

# 运算
@app_api.route('/api/calculate')
def add_numbers():
    calc_expression = request.args.get('calc_expression', 0, type=str)
    try:
        result = eval(calc_expression)
    except Exception as e:
        result = "Please input the correct expression!"
    return jsonify(result = result)


@app_api.route('/api/translate')
def translate():
    trans_expression = request.args.get('trans_expression', 0, type=str)
    # en_key_word
    print(trans_expression)
    ret = []
    for k, v in word_dict.items():
        if trans_expression in k:
            ret.append((k, v))
    return jsonify(result = ret)


@app_api.route('/api/collected_web')
def collected_webs():
    mywebs = find_data("myweb", all=True)
    return (json_util.dumps(mywebs))

    '''
    with open("myweb.json", 'r', encoding="UTF-8") as load_f:
        webdata = json.load(load_f)
        return jsonify(webdata)
    '''


@app_api.route('/api/add_url')
def process_add_web():
    tagname = request.args.get('tagname', 0, type=str)
    webname = request.args.get('webname', 0, type=str)
    weburl = request.args.get('weburl', 0, type=str)
    web = {
        "tag" : tagname,
        "name" : webname,
        "url" : weburl
    }
    add_new_web("myweb", web)
    return jsonify("refresh page to see the result")
