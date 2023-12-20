PROMPT_QUERY_CLS="""你是数据库专家，以下是一些金融数据表信息：
        {info}
        问题是：
        {input}
        如果能通过查询这些数据表来回答问题请输出”是s“
        如果需要通过查看招股说明书来回答问题请输出”否“
        只需回答“是”或“否”
"""
PROMPT_KB_CHAT="""  你是金融领域专家，以下是部分招股说明书信息：
{info}
 问题：
{input}
请从招股说明书信息得到对应答案,保留原问题中的公司名称。
"""

PROMPT_TABLE_SELECT=""" 以下是若干数据表的信息:
    {table_info}
    请确定需要查询哪些表来得到答案,请正确回答表名,并说明理由。
    问题: 
    {input}
    答案请从以下表名选择:
    {table_names}
"""

PROMPT_SQL_GENERATE_GG="""
你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"帮我算一下在20190828,代码为08613的港股日价格振幅是多少，小数点后保留不超过3位。":"SELECT ROUND((("最高价(元)") - ("最低价(元)")) / ("昨收盘(元)"), 3) AS "日价格振幅" FROM "港股票日行情表" WHERE "股票代码" = '08613' AND "交易日" = '20190828';":"SELECT COUNT(*) FROM 港股票日行情表 WHERE 交易日='20190723' AND "收盘价(元)" < "昨收盘(元)";"
"20190723港股下跌的股票家数有多少家?":
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""
PROMPT_SQL_GENERATE_BASE="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
部分示例如下:
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""
PROMPT_SQL_GENERATE_HY="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
部分示例如下
"在20201022，按照中信行业分类的行业划分标准，哪个一级行业的A股公司数量最多?":"SELECT "一级行业名称" FROM "A股公司行业划分表" WHERE "交易日期" = '20201022' AND "行业划分标准" = '中信行业分类' GROUP BY "一级行业名称"  ORDER BY COUNT(DISTINCT "股票代码") DESC LIMIT 1;",
"请问在钢铁行业，20190223行业的A股公司有多少?":"SELECT COUNT(DISTINCT "股票代码") FROM "A股公司行业划分表" WHERE  "一级行业名称" = '钢铁' AND "交易日期" = '20190223';"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_AG_GP="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"帮我查一下在2018年，代码为000001的A股股票今开盘高于昨收盘的天数？":"SELECT  COUNT(*) FROM "A股票日行情表" WHERE "股票代码"='000001' AND "交易日" LIKE '2018%'  AND "今开盘(元)">"昨收盘(元)";",
"请帮我查询下股票代码为000001的股票在2021年内最高日收盘价是多少？":"SELECT  MAX("收盘价(元)") FROM "A股票日行情表" WHERE "股票代码"='000001' and "交易日" LIKE '2021%';",
"股票600386在20210901日期中的收盘价是多少?（小数点保留3位）":"SELECT ROUND("收盘价(元)",3) FROM "A股票日行情表" WHERE "股票代码"='600386' AND "交易日"='20210901';",
"请查询在2019年度，002093股票涨停天数？   解释：（收盘价/昨日收盘价-1）》=9.8% 视作涨停":"SELECT COUNT(交易日) as 涨停天数 FROM A股票日行情表 WHERE 股票代码 = '603789' AND ("收盘价(元)"/"昨收盘(元)"-1) >=0.098 AND "交易日" LIKE '2019%'",
"请帮我计算，代码为000001的股票，2020年一年持有的年化收益率有多少？百分数请保留两位小数。年化收益率定义为：（（有记录的一年的最终收盘价-有记录的一年的年初当天开盘价）/有记录的一年的当天开盘价）* 100%。":
"SELECT ROUND(((SELECT "收盘价(元)"
                FROM "A股票日行情表"
                WHERE "股票代码" = '000001'
                AND "交易日" LIKE '2020%'
                ORDER BY "交易日" DESC
                LIMIT 1) /
              (SELECT "今开盘(元)"
               FROM "A股票日行情表"
               WHERE "股票代码" = '000001'
               AND "交易日" LIKE '2020%'
               ORDER BY "交易日"
               LIMIT 1) - 1) * 100, 2)||'%' AS "年化收益率";",
"20190408日，开盘价较上一交易日最高价高的股票有多少只？（如上一交易日没有某只股票，则不统计在内）":"SELECT COUNT(*)
FROM (
  SELECT A."股票代码",
         A."今开盘(元)",
				 A."交易日",
         LAG(A."最高价(元)") OVER (PARTITION BY A."股票代码" ORDER BY A."交易日") AS 前日最高
  FROM "A股票日行情表" AS A
  WHERE A."交易日" <= '20190408'
) AS B
WHERE B."今开盘(元)" > B."前日最高"
  AND B."交易日" = '20190408'
  AND B."前日最高" IS NOT NULL;"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.

"""
PROMPT_SQL_GENERATE_AG_HY="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"请帮我查询出20210415日，建筑材料一级行业涨幅超过5%（不包含）的股票数量":"SELECT COUNT(*)FROM "A股票日行情表" AS 股票 JOIN "A股公司行业划分表" AS 行业 ON 股票."股票代码" = 行业."股票代码" WHERE 行业."一级行业名称" = '建筑材料' AND 股票."交易日" = '20210415' AND (股票."收盘价(元)" - 股票."昨收盘(元)") / 股票."昨收盘(元)" > 0.05;",
"请帮我计算，在20190312，中信行业分类划分的一级行业为消费者服务行业中，涨跌幅最大股票的股票代码是？涨跌幅是多少？百分数保留两位小数。股票涨跌幅定义为：（收盘价 - 前一日收盘价 / 前一日收盘价）* 100%。":"SELECT "股票代码",ROUND(("收盘价(元)"-"昨收盘(元)")/"昨收盘(元)"*100,2)||'%' AS "涨跌幅" FROM "A股票日行情表"WHERE "交易日"='20190312' AND "股票代码" IN (SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "行业划分标准" = '中信行业分类' AND "一级行业名称" = '消费者服务') ORDER BY "涨跌幅" DESC LIMIT 1;",
"假设股票日收益率计算公式为：日收益率 = （当日收盘价-昨收盘价）/昨收盘价。请帮我找到在2021年，申万行业分类行业划分标准,银行一级行业中, 代码为多少的股票的日均收益率最高？":"SELECT "股票代码" FROM "A股票日行情表" WHERE "交易日" LIKE '2021%'AND "股票代码" IN (SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "行业划分标准" = '申万行业分类' AND "一级行业名称" = '银行') GROUP BY "股票代码" ORDER BY AVG(("收盘价(元)"-"昨收盘(元)")/"昨收盘(元)") DESC LIMIT 1;",
"请查询在20200623日期，中信行业分类下汽车一级行业中，当日收盘价波动最大（即最高价与最低价之差最大）的股票代码是什么？":"  SELECT "股票代码"  FROM "A股票日行情表" WHERE "交易日" = '20200623' AND "股票代码" IN (  SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "一级行业名称" = '汽车' AND "交易日期" = '20200623' AND "行业划分标准" = '中信行业分类') GROUP BY "股票代码" ORDER BY ("最高价(元)" - "最低价(元)") DESC LIMIT 1;"
"请帮我查询下，在20210907，申万行业分类里一级行业为钢铁行业的所有股票里, 成交金额(元)最多的股票的代码是什么？成交金额是多少？":"SELECT "股票代码" ,"成交金额(元)" FROM "A股票日行情表" WHERE "交易日"='20210907' AND "股票代码" IN (SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "行业划分标准" = '申万行业分类' AND "一级行业名称" = '钢铁') ORDER BY "成交金额(元)" DESC LIMIT 1;",
"20210618日，一级行业为基础化工的股票的成交量合计是多少？取整。":"SELECT FLOOR(SUM("成交量(股)")) FROM "A股票日行情表" WHERE "交易日" = '20210618' AND "股票代码" IN (SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "一级行业名称" = '基础化工');",
"20200101日，一级行业为电子的股票的成交金额合计是多少？取整":"SELECT FLOOR(SUM("成交金额(元)")) FROM A股票日行情表 WHERE 交易日 = '20200101' AND  股票代码 IN (SELECT 股票代码 FROM A股公司行业划分表 WHERE 一级行业名称 = '电子' );",
"请查询：在20190118，属于申万二级银行行业的A股股票，它们的平均成交金额是多少？小数点后保留不超过5位。":"SELECT ROUND(AVG("成交金额(元)"),5)  FROM "A股票日行情表" WHERE "交易日" = '20190118' AND "股票代码" IN (SELECT DISTINCT "股票代码" FROM "A股公司行业划分表" WHERE "二级行业名称" = '银行' AND "行业划分标准" = '申万行业分类');"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.

"""


PROMPT_SQL_GENERATE_JJ="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"请帮我查询在2019年,博时基金管理有限公司成立哪种类型的基金个数最多?":"SELECT 基金类型 FROM 基金基本信息 WHERE 管理人 LIKE '%博时基金管理有限公司%' AND 成立日期 LIKE '2019%' GROUP BY 基金类型 ORDER BY (COUNT(DISTINCT 基金代码)) DESC LIMIT 1;",
"我想了解一下西部利得基金管理有限公司2020年成立的债券型基金,其管理费率的平均值是多少?请四舍五入保留小数点两位":"SELECT ROUND(AVG("管理费率"),2) as 平均管理费率 FROM 基金基本信息 WHERE 管理人 = '西部利得基金管理有限公司' AND 基金类型 = '债券型' AND 成立日期 LIKE '2020%';",
"我想知道德邦基金管理有限公司在2019年成立了多少只管理费率小于0.8%的基金？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金基本信息 WHERE 管理人 = '德邦基金管理有限公司' AND 成立日期 LIKE '2019%' AND 管理费率 < '0.8%';",
"请列出国泰基金管理有限公司在2019年成立并且托管人为中国工商银行股份有限公司的所有基金的基金托管费率的平均数。":"SELECT AVG (托管费率) FROM 基金基本信息 WHERE 管理人 LIKE '%国泰基金管理有限公司%' AND 托管人 = '中国工商银行股份有限公司' AND 成立日期 LIKE '2019%'",
"请帮我查询在截止2019-12-31的报告期间，基金总份额降低的基金数量是多少？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金规模变动表 WHERE 报告期期末基金总份额 < 报告期期初基金总份额 AND 截止日期 = '2019-12-31 00:00:00';",
"我想知道在2019年，广发基金管理有限公司已发行的基金中，有多少只基金报告期期初基金总份额小于报告期期末基金总份额(使用每只基金当年最晚的定期报告数据计算)？":"SELECT COUNT(DISTINCT A.基金代码) FROM (SELECT 基金代码,MAX(截止日期) AS 截止日期 FROM 基金规模变动表 WHERE 基金代码 IN (SELECT 基金代码 FROM 基金基本信息 WHERE 管理人='广发基金管理有限公司' ) AND 定期报告所属年度 = '2019'  AND 报告类型 = '基金定期报告'  GROUP BY "基金代码" ) AS A, 基金规模变动表 AS B WHERE A.基金代码=B.基金代码 AND A.截止日期=B.截止日期 AND B.报告期期初基金总份额< B.报告期期末基金总份额;"


请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_JJ_GM="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"请问2020年四季度有多少家基金是净申购?它们的净申购份额加起来是多少?请四舍五入保留小数点两位。":"SELECT COUNT(DISTINCT 基金代码) AS 家数, ROUND(SUM(报告期基金总申购份额-报告期基金总赎回份额),2) AS 净申购份额 FROM 基金规模变动表 WHERE (报告期基金总赎回份额-报告期基金总申购份额 )<0 AND 定期报告所属年度 = '2020' AND 截止日期='2020-12-31 00:00:00' ;",
"请帮我查询在截止2021-03-31的基金定期报告中，基金总赎回份额为零的基金有几个？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金规模变动表 WHERE 报告期基金总赎回份额 ='0' AND 截止日期 = '2021-03-31 00:00:00';",
"请帮我查询下，在2019年12月的报告中，报告期基金总申购份额和报告期基金总赎回份额差额最大的一只基金的简称是什么？差额有多少？保留两位小数。":" SELECT 基金简称,ROUND((报告期基金总申购份额-报告期基金总赎回份额),2)AS 最大差额 FROM 基金规模变动表 WHERE 定期报告所属年度 = '2019' AND 报告类型 = '基金定期报告' AND 截止日期 LIKE '2019%12%' GROUP BY 基金简称 ORDER BY 最大差额 DESC LIMIT 1;",

请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""
PROMPT_SQL_GENERATE_JJ_CY="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"请查询：在2020的年度报告中，个人投资者持有基金份额大于机构投资者持有基金份额的基金属于混合型类型的有几个。":"SELECT COUNT(DISTINCT 基金基本信息."基金代码") FROM 基金基本信息 JOIN 基金份额持有人结构 ON 基金基本信息."基金代码" = 基金份额持有人结构."基金代码" WHERE 基金份额持有人结构."定期报告所属年度" = '2020' AND 报告类型='年度报告' AND 个人投资者持有的基金份额 > 机构投资者持有的基金份额 AND 基金基本信息."基金类型" = '混合型';",
"在2021年的年度报告里，交银施罗德基金管理有限公司管理的基金中，有多少比例的基金是个人投资者持有的份额超过机构投资者？希望得到一个精确到两位小数的百分比。":"SELECT ROUND((A.单*1.0/B.总*1.0)*100,2) FROM
(SELECT COUNT(DISTINCT 基金基本信息.基金代码) AS 单 FROM 基金份额持有人结构 JOIN 基金基本信息 ON 基金份额持有人结构.基金代码 = 基金基本信息.基金代码 WHERE 基金基本信息.管理人 = '交银施罗德基金管理有限公司' AND 定期报告所属年度 = '2021' AND 报告类型 ='年度报告' AND 个人投资者持有的基金份额 > 机构投资者持有的基金份额) AS A,(SELECT COUNT(DISTINCT 基金基本信息.基金代码) AS 总  FROM 基金份额持有人结构 JOIN 基金基本信息 ON 基金份额持有人结构.基金代码 = 基金基本信息.基金代码 WHERE 基金基本信息.管理人 = '交银施罗德基金管理有限公司' AND 定期报告所属年度 = '2021' ) AS B",
"我想知道2020年的年度报告中，机构投资者持有的份额占比超过30%的基金有多少，并且他们总共持有了多少?记得帮我保留两位小数。":"SELECT COUNT(DISTINCT 基金代码),ROUND(SUM(机构投资者持有的基金份额),2) FROM 基金份额持有人结构 WHERE 定期报告所属年度='2020' AND 报告类型='年度报告' AND 机构投资者持有的基金份额占总份额比例>'30';",
"我想知道2020年的中期报告中，机构投资者持有的份额占比超过66%的基金有多少，并且他们总共持有了多少?记得帮我保留两位小数。":"SELECT COUNT(DISTINCT 基金代码),ROUND(SUM(机构投资者持有的基金份额),2) FROM 基金份额持有人结构 WHERE 定期报告所属年度='2020' AND 报告类型='中期报告' AND 机构投资者持有的基金份额占总份额比例>'66';"
"2019年中期报告里，国融基金管理有限公司管理的基金中，机构投资者持有份额比个人投资者多的基金有多少只?":"SELECT COUNT(DISTINCT 基金代码) FROM 基金份额持有人结构 WHERE 定期报告所属年度 = '2019' AND 报告类型='中期报告'  AND 基金代码 IN (SELECT 基金代码 FROM 基金基本信息 WHERE 管理人='国融基金管理有限公司') AND 机构投资者持有的基金份额 > 个人投资者持有的基金份额;"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""
PROMPT_SQL_GENERATE_JJ_HQ="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"20210106日，请给出汇安宜创量化精选混合C基金的管理人和累计单位净值":"SELECT "管理人", "累计单位净值" FROM "基金基本信息","基金日行情表" WHERE "基金基本信息"."基金代码" ="基金日行情表"."基金代码"  AND "交易日期" = '20210106' AND "基金简称" LIKE '%汇安宜创量化精选混合C%';",
"帮我查一下诺德短债债券C基金在20200331的资产净值和单位净值是多少?":"SELECT 资产净值,单位净值 FROM 基金日行情表 WHERE 基金代码 IN (SELECT 基金代码 FROM 基金基本信息 WHERE 基金简称 LIKE '%诺德短债债券C%') AND 交易日期 = '20200331';"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_JJ_GP="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"帮我查询在2020年12月31日，代码为011131的基金前20大重仓股票中属于中信二级生物医药Ⅱ行业的平均市值是多少？小数点后保留不超过3位。":"SELECT ROUND(AVG(市值),3) FROM 基金股票持仓明细 WHERE 持仓日期='20201231' AND 基金代码='011131' AND 第N大重仓股<='20' AND 股票代码 IN (SELECT 股票代码 FROM A股公司行业划分表 WHERE 行业划分标准='中信行业分类' AND 二级行业名称='生物医药Ⅱ');",
"在2021年12月年报(含半年报)中，博时鑫荣稳健混合C基金持有市值最多的前10只股票中，所在证券市场是上海证券交易所的有几个？":"SELECT COUNT(DISTINCT 股票代码) FROM 基金股票持仓明细 WHERE 所在证券市场='上海证券交易所' AND 股票代码 IN(SELECT 股票代码 FROM 基金股票持仓明细 WHERE 持仓日期 LIKE '202112%'  AND 基金简称 LIKE '%博时鑫荣稳健混合C%' AND 报告类型='年报(含半年报)'  ORDER BY 市值 DESC LIMIT 10);",
"我想知道东方阿尔法优势产业混合C基金，在2021年年度报告中，前10大重仓股中，有多少只股票在报告期内取得正收益。":"SELECT COUNT(DISTINCT 表一.股票代码) FROM 基金股票持仓明细 AS 表一,基金股票持仓明细 AS 表二 WHERE 表一.基金代码=表二.基金代码 AND 表一.股票代码=表二.股票代码 AND 表一.持仓日期='20201231' AND 表二.持仓日期='20211231'  AND 表一.基金简称 LIKE '%东方阿尔法优势产业混合C%' AND 表一.第N大重仓股<=10 AND 表一.市值<表二.市值;",
"我想知道东方红品质优选两年定期开放混合基金，在2021年半年度报告中，前10大重仓股中，有多少只股票在报告期内取得正收益。":"SELECT COUNT(DISTINCT 表一.股票代码) FROM 基金股票持仓明细 AS 表一,基金股票持仓明细 AS 表二 WHERE 表一.基金代码=表二.基金代码 AND 表一.股票代码=表二.股票代码 AND 表一.持仓日期='20201231' AND 表二.持仓日期='20210630'  AND 表一.基金简称 LIKE '%东方红品质优选两年定期开放混合%' AND 表一.第N大重仓股<=10 AND 表一.市值<表二.市值;",
"我想了解汇安信利债券A基金,在2020年四季度的季报第3大重股。该持仓股票当个季度的涨跌幅?请四舍五入保留百分比到小数点两位。":"
SELECT C.股票代码,C.股票名称,ROUND(((A."收盘价(元)" - B."收盘价(元)") / B."收盘价(元)") * 100, 2)||'%' AS 涨跌幅百分比
FROM A股票日行情表 AS A ,(SELECT 股票代码,股票名称
      FROM 基金股票持仓明细 
      WHERE 基金简称 LIKE '%汇安信利债券A%' 
      AND 报告类型 = '季报' 
      AND 持仓日期 = '20201231' 
      AND 第N大重仓股 = 3) AS C
JOIN A股票日行情表 AS B ON A.股票代码 = B.股票代码
WHERE A.股票代码 =C.股票代码
AND A.交易日 = (
    SELECT MAX(交易日) 
    FROM A股票日行情表 
    WHERE 交易日 <= '20201231' 
      AND 股票代码 = A.股票代码
)
AND B.交易日 = (
    SELECT MIN(交易日) 
    FROM A股票日行情表 
    WHERE 交易日 >= '20200930' 
      AND 股票代码 = A.股票代码
);",
"在2021年12月季报中，持有健之佳这一股票且市值占基金资产净值比不小于5%的有几只基金？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金股票持仓明细 WHERE 股票名称='健之佳' AND 报告类型='季报' AND 持仓日期 LIKE '202112%' AND 市值占基金资产净值比 >= 0.05;",
"我想知道国泰金鹿混合在2020年Q1的季报中，该基金的第2大重仓股的代码是什么?":"SELECT DISTINCT 股票代码 FROM 基金股票持仓明细 WHERE  基金简称 LIKE '%国泰金鹿混合%' AND 报告类型 = '季报' AND 持仓日期 ='20200331' AND 第N大重仓股='2';",
"请查询：2020年12月年报(含半年报),持有16华润01且是前10大重仓股的基金有几个？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金债券持仓明细 WHERE  持仓日期 LIKE '202012%' AND 报告类型='年报(含半年报)' AND 债券名称 = '16华润01' AND 第N大重仓股 <= 10;",
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}
问题: {input}
请输出能够直接执行的SQL语句.
"""
PROMPT_SQL_GENERATE_JJ_GP_2="""
你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"在2019年报中，鹏华核心优势混合A基金第四大重仓股的代码和股票名称是什么？":"SELECT "股票代码","股票名称" FROM "基金股票持仓明细" WHERE "持仓日期" LIKE '201912%' AND  "第N大重仓股"='4' AND "基金简称" LIKE '%鹏华核心优势混合A%' AND "报告类型" = '年报(含半年报)';",
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}
问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_JJ_HY="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"我想知道在20211231的季报里，中信保诚红利精选混合C投资的股票分别是哪些申万一级行业？":"SELECT DISTINCT "一级行业名称" FROM "A股公司行业划分表" WHERE 行业划分标准='申万行业分类' AND "股票代码" IN (SELECT "股票代码" FROM "基金股票持仓明细" WHERE "报告类型" ='季报' AND "持仓日期" = '20211231' AND "基金简称" LIKE '%中信保诚红利精选混合C%')"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}
问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_JJ_ZQ="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"平安惠添纯债债券基金在20190930的季报里，前三大持仓占比的债券名称是什么?":"SELECT "债券名称" FROM "基金债券持仓明细" WHERE "基金简称" LIKE '平安惠添纯债债券' AND "持仓日期" = '20190930' AND "报告类型"='季报' ORDER BY "持债市值占基金资产净值比" DESC LIMIT 3;",
"广发景兴中短债债券A基金在20200930且报告类型是季报的持债市值中，哪类债券市值最高？":"SELECT "债券类型" FROM "基金债券持仓明细" WHERE "基金简称" LIKE '广发景兴中短债债券A' AND "持仓日期" = '20200930' AND "报告类型" = '季报' GROUP BY "债券类型" ORDER BY SUM("持债市值") DESC LIMIT 1;",
"请帮我查询下在2019年, 山西证券股份有限公司管理的债券型基金中，持有过公司债券的基金有多少只？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金债券持仓明细 WHERE 持仓日期 LIKE '2019%' AND 债券类型='公司债券' AND 基金代码 IN (SELECT 基金代码 FROM 基金基本信息 WHERE 管理人 ='山西证券股份有限公司');"
"在20201231的年报(含半年报)中，泰康长江经济带债券C基金的债券持仓,其持有最大仓位的债券类型是什么?":"SELECT 债券类型 FROM 基金债券持仓明细 WHERE 基金简称 LIKE '%泰康长江经济带债券C%' AND 持仓日期 LIKE '20201231' AND 报告类型 ='年报(含半年报)' GROUP BY 债券类型 ORDER BY SUM(持债市值) DESC LIMIT 1;"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后):
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_SQL_GENERATE_JJ_KZZ="""你是SQLite专家. 对于给定的问题创建符合语法的SQL语句.
只需要查询相关列. 将每个列名用双引号("")括起来.
只可以用下面表中所给出的列名，不可以使用不存在的列名。注意哪些列在对应的表中。
请注意，你可能需要查询多个表来来创建查询语句.
示例如下：
"我想知道国泰信用互利债券A基金在20211231的季报中，其可转债持仓占比最大的是哪个行业？用申万一级行业来统计。":"SELECT DISTINCT "一级行业名称" FROM "A股公司行业划分表" WHERE "行业划分标准"='申万行业分类' AND "股票代码" IN (SELECT "对应股票代码" FROM "基金可转债持仓明细" WHERE "报告类型"='季报'  AND "持仓日期" = '20211231' AND "基金简称" LIKE '%国泰信用互利债券A%' ORDER BY "市值占基金资产净值比" DESC LIMIT 1);"
"我想知道国泰民福策略价值灵活配置混合A基金在基金在20211231的年报(含半年报)中，其可转债持仓占比最大的是哪个行业？用申万一级行业来统计。":"SELECT DISTINCT "一级行业名称" FROM "A股公司行业划分表" WHERE "行业划分标准"='申万行业分类' AND "股票代码" IN (SELECT "对应股票代码" FROM "基金可转债持仓明细" WHERE "报告类型"='年报(含半年报)' AND "持仓日期" = '20211231' AND "基金简称" LIKE '%国泰民福策略价值灵活配置混合A%' ORDER BY "市值占基金资产净值比" DESC LIMIT 1);"
"请帮我查询下在2019年浙商基金管理有限公司成立的基金中，有多少只基金持仓过可转债债券？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金债券持仓明细 WHERE 持仓日期 LIKE '2019%' AND 债券类型='可转债债券' AND 基金代码 IN (SELECT 基金代码 FROM 基金基本信息 WHERE 管理人 ='浙商基金管理有限公司')",
"请帮我查询下，在2020年Q4季报报告中，008572基金的第一大重仓可转债同期还有多少只基金也进行了持仓？":"SELECT COUNT(DISTINCT 基金代码) FROM 基金可转债持仓明细 WHERE 持仓日期='20201231' AND 对应股票代码 IN(SELECT 对应股票代码 FROM 基金可转债持仓明细 WHERE 基金代码='008572' AND "第N大重仓股" =1 AND 持仓日期='20201231');"
请利用以下表的全部信息(以下表名应该都应出现在FROM字段后),当问题中出现基金的名字,请使用"基金简称"字段:
{table_info}

问题: {input}
请输出能够直接执行的SQL语句.
"""

PROMPT_DB_CHAT="""请结合问题和数据库结果组织答案。
根据问题：
{input}
通过查询数据库查询得到以下结果：
{result}

请注意：无需计算,不能只回答数据库结果中的数字,尽可能利用原问题中的文字。
"""

PROMPT_COMPANY_NAME="""已知部分招股信息：
{info}
请问招股公司的全称是什么，只需回答公司名，使用简体中文。
"""

model_path="/tcdata/models/Tongyi-Finance-14B-Chat"
data_path="/tcdata/bs_challenge_financial_14b_dataset/pdf_txt_file/"
kb_path="/app/db/"
emb_model_path="/app/bge-large-zh-v1.5/"
pdf_path="/tcdata/bs_challenge_financial_14b_dataset/pdf/"
txt_path="/tcdata/bs_challenge_financial_14b_dataset/pdf_txt_file/"