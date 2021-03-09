## 简介

用户可以上传zip文件和config.json文件。
其中zip中的文件内容为yaml和json文件。config.json文件中描述了zip的哪个文件要解压到哪个路径去。


#### 要求
1. 上传zip文件后，要检查config.json中的文件，是否都在zip中出现过了。如果没有出现过，要提示前端
2. 下载是，zip中的文件，就是config.json中的文件
3. 要考虑配置文件不存在的情况，如果某个文件不存在，需要返回错误码到前端，提示哪些文件确实了。
4. 结合graphql
5. 导入导出功能的开发
6. 数组模式和单个dict对象模式：监听模式和数据库模式； 还是直接将单个dict的形式转换为list？
7. 将所有中文翻译一遍
8. 现在区分相同元素的唯一方法是index，后期考虑加上_id字段

#### notice

1. 我似乎搞混了queryset, filter_set, filter之间的关系： 似乎filterSet里边的next_batch才是我的filterSet的本意，现在的filterSet跟querySet的区别差不多了
2. filter中的mvc做得不够到位
# TODO:
1. 提高程序可读性
2. 增加程序的效率
3. 增加graphql后台
4. 增加可视化的接口自由配置
5. 自动对接到mysql， mongo， redis等
