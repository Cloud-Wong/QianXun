import requests
from lxml import etree
from py2neo import *

head = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")
node_matcher = NodeMatcher(graph)
r_matcher = RelationshipMatcher(graph)

#爬取角色URL列表
def create_role_list(movie_url):
    html = requests.get(movie_url,headers=head)
    html.encoding="utf-8"
    html = html.text
    selector = etree.HTML(html)
    content = selector.xpath("//html")[0]
    role_list = content.xpath("//div[@class='role-name']//a/@href")
    #name_list = content.xpath("//div[@class='role-name']/span/a/text()")
    role_list = ["https://baike.baidu.com"+i for i in role_list]
    return role_list


# 爬取角色信息
def role_info(url):
    param = {}
    html = requests.get(url, headers=head)
    html.encoding = "utf-8"
    html = html.text
    selector = etree.HTML(html)
    content = selector.xpath("//html")[0]
    img = content.xpath("//div[@class='summary-pic']//img/@src")
    if img:
        param['img'] = img[0]
    info_list = content.xpath("//dt[@class='basicInfo-item name']/text()")
    info_value = content.xpath("//dd[@class='basicInfo-item value']")
    info_len = len(info_list)
    for i in range(0, info_len):
        param[info_list[i].replace('\xa0', '')] = info_value[i].xpath("string(.)").replace('\n', '')

    if param:
        del param['中文名']

    return (param)


# 爬取人际关系表 并结合和角色信息一并存入Neo4j数据库
def create_relationship(role_url):
    graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")
    html = requests.get(role_url, headers=head)
    html.encoding = "utf-8"
    html = html.text
    selector = etree.HTML(html)
    content = selector.xpath("//html")[0]
    n_rel = len(content.xpath("//div/h2[contains(string(),'关系')]/ancestor::div/following-sibling::\
                            table[1]/tr[position()>1]"))
    role_name = content.xpath("//dd[@class='lemmaWgt-lemmaTitle-title']/h1/text()")[0]

    source = node_matcher.match(name=role_name).first()
    if not source:
        param = role_info("https://baike.baidu.com/item/" + role_name)
        source = Node("role", name=role_name, **param)
        graph.create(source)

    for i in range(2, 2 + n_rel):
        target_name = content.xpath("//div/h2[contains(string(),'关系')]/ \
                                    ancestor::div/following-sibling::table/tr[" + str(i) + "]/td[1]//text()")[0]
        rel = content.xpath("//div/h2[contains(string(),'关系')]/ancestor::div/\
                            following-sibling::table/tr[" + str(i) + "]/td[2]//text()")[0]
        desc = content.xpath("//div/h2[contains(string(),'关系')]/ancestor::\
                             div/following-sibling::table/tr[" + str(i) + "]/td[3]//text()")[0]
        target = node_matcher.match(name=target_name).first()
        if not target:
            param = role_info("https://baike.baidu.com/item/" + target_name)
            target = Node("role", name=target_name, **param)
            graph.create(target)
        graph.create(Relationship(source, rel, target, describe=desc))


#执行

graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")

movie_url = "https://baike.baidu.com/item/%E5%8D%83%E4%B8%8E%E5%8D%83%E5%AF%BB"  #《千》百度百科
role_list = create_role_list(movie_url)

for i in role_list:
    create_relationship(i)

node_matcher = NodeMatcher(graph)
r_matcher = RelationshipMatcher(graph)


#手动调整信息
graph = Graph("http://127.0.0.1:7474", username="neo4j", password="123456")

#删除假的“坊”
graph.run("MATCH ()-[r:宝宝]->(n) DELETE r,n")
#添加真的坊关系
tang = node_matcher.match(name='汤婆婆').first()
fang = node_matcher.match(name='坊宝宝').first()
graph.create(Relationship(tang,'宝宝',fang,describe='坊宝宝是汤屋的主管——汤婆婆的独子'))
#添加无脸男关系
lian = node_matcher.match(name='无脸男').first()
qian = node_matcher.match(name='荻野千寻').first()
graph.create(Relationship(lian,'喜欢',qian))

#手动添加小玲信息
ling = node_matcher.match(name='小玲').first()
ling['img'] = "https://gss3.bdstatic.com/-Po3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=a7bc12155bdf8db1bc2e7b623118ba69/7af40ad162d9f2d3acf03762acec8a136227cc5e.jpg"
ling['性别'] = '女'
graph.push(ling)