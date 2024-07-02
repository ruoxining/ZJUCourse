### HW4：Review of Tang et al., ArnetMiner: extraction and mining of academic social networks. (2020 KDD Test of Time Award for Applied Data Science)

3190105959 宁若汐

#### 文章链接

https://dl.acm.org/doi/pdf/10.1145/1401890.1402008

#### 网站链接

[AMiner (arnetminer.org)](http://www.arnetminer.org/)

#### 本文解决的研究难题是什么？该问题有何实际应用场景？

​		本文阐述了ArnetMiner网站（[AMiner (arnetminer.org)](http://www.arnetminer.org/)），一个学术搜索引擎的技术原理。

​		构建学术网络的难点，一方面在于很难爬取到语义连贯或完整的信息，另一方面是缺少对所有信息统一的建模方法，如果对不同格式的信息建不同的模型，就会导致不同格式的信息之间的关系不明显。之前的研究在这两个问题上关注点比较分散，原有方法也不足以深入挖掘整个学术网络。本文尝试用新的方法解决上述两个问题。

​		我们的模型主要从下面几个步骤解决问题：

1. 如何自动从网络上提取学者信息
2. 如何整合不同来源的信息（比如：学者个人介绍与出版物）
3. 如何用统一的方式对不同类型的数据建模
4. 如何用我们搭建的模型提出搜索建议

​		从而构建出一个实用的学者和学术信息网络，部署成搜索引擎，提供学术搜索建议。

#### 本文解决问题的技术方案

我们的流程主要包含五个部分（如图）：

1. 提取：从互联网提取作者个人信息。首先先从互联网手机作者个人主页，用统一的方法提取一些特征，再从论文库提取相应著作。

   前期调研发现，约85.62%的学者在高校内，主页格式相似，其余在公司的研究所内，主页五花八门。40%个人介绍在表格内，部分使用自然语言描述。提取分三步：用SVM做的二分类模型识别相关网页，做分词和用CRF打标预处理，然后提取。

2. 整合：用学者姓名作为主键整合个人介绍和作品。整合过程中，使用了概率模型消除歧义（重名问题）。整合的数据存进了一个叫RNKB的数据库。

3. 存取：RNKB存储用的是MySQL，索引用的倒排文件索引。

4. 建模：使用生成概率模型自动生成不同类型的信息。

5. 搜索服务：提供学者专长搜索，人物关系搜索等功能。

![截屏2022-05-31 02.00.34](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-05-31 02.00.34.png)



#### 本文的优点和贡献

我们的成果介绍：

1. 我们使用Friend-Of-A-Friend（FOAF）理论作为人物关系框架的基础，提出了一个统一的基于条件随机场的个人主页挖掘方法。我们获得了448470位学者的个人介绍。（We extend the Friend-Of-A-Friend (FOAF) ontology [9] as the profile schema and propose a unified approach based on Conditional Random Fields to extract researcher profiles from the Web.）

​		下表分别是个人信息挖掘中打的标签和提取出的作者关系。

![截屏2022-06-03 00.09.05](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 00.09.05.png)

![截屏2022-06-03 00.09.14](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 00.09.14.png)

2. 我们整合了从网络数据库中提取出的学者信息。我们提出了统一的基于概率的框架，处理信息整合过程中的语义模糊问题。使用了隐马尔可夫模型归一化，后面使用了期望最大算法，具体没有看懂，然后解决了语义模糊问题。（We integrate the extracted researcher profiles and the crawled publication data from the online digital libraries. We propose a uni- fied probabilistic framework for dealing with the name ambiguity problem in the integration.）

   

3. 我们提出了三个基于概率的生成模型，可以自动对文章、作者和出版杂志进行我们关注/搜索的方面的建模。（We propose three generative probabilistic models for simul- taneously modeling topical aspects of papers, authors, and publica- tion venues.）

   第一个模型中（图6(a)），会议信息是一个与论文中每个词都有关的特征。我们认为一篇文章的共同作者决定了文章的主题，主题与每个单词都有关。

   第二个模型中（图6(b)），每个主题与每个作者和会议的自然连接结果对应（不像ACT1中只选择一位作者）。我们认为作者们会先瞄准一个会议，根据会议主题和作者兴趣两个因素来撰写论文。

   第三个模型中（图6(c)），不同会议代表一个不同的数值，每篇文章中的每个单词对不同会议的数值有不同贡献，处理过所有单词后，文章会对应得分最高的会议。这是一种发表论文的自然过程，即作者先写好论文，然后根据论文主题决定在什么会议上发表。

![截屏2022-06-03 00.50.14](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 00.50.14.png)

5. 基于建模结果，我们实现了几种搜索服务，比如搜索专业领域、搜索人物关系等。（Based on the modeling results, we implement several search services such as expertise search and association search.）

   我们对提出的方法进行了实证评估。实验结果表明，我们提出的方法在处理上述问题上明显优于baseline。

   

#### 请总结本文的实验设置(包括实验数据集、对比方法，评测指标等， 不需要进行实验结果分析)

##### 数据集

自制数据集。按照前文所述方法在互联网上爬取学者信息和会议信息，处理后做成了数据库。

##### 本工程含有多个步骤，每个步骤都有对应的检验方法：

1. 测试个人信息挖掘算法：

   随机抽取1000个学者姓名，用我们的模型搜索，最终搜索到的有898个个人主页。实验结果F1是83.37%，明显高于两个baseline。下图还展示了不同类型的信息在挖掘个人主页中起到的作用大小。（好像是）

   ![截屏2022-06-05 22.14.48](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-05 22.14.48.png)

2. 姓名消歧方法：选取了14个真实姓名，使用我们的方法进行消歧。先做了两种baseline方法，一种是使用搜索引擎（？），一种是指只选取所有不重复的键值（Distinct），发现我们的方法明显好于baseline。

   ![截屏2022-06-03 00.10.53](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 00.10.53.png)

3. 专长搜索服务

   分别人工评审和使用指标自动评审。收集了一些文章作为subset（含14134个人，10716篇文章，1434个会议），过下面的P@5, P@10, P@20, R-pre指标，结果分别如表格所示？（此处没有详细了解这些指标）

![截屏2022-06-03 01.01.39](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 01.01.39.png)

![截屏2022-06-03 01.02.02](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 01.02.02.png)

4. 联系搜索服务（感觉意思是搜索跟一个人有关系的其它人）：用了最短路算法和深度优先搜索算法（但是固定深度），提供最近关系、近邻关系等搜索服务。

5. 其它应用

   还提供了作者研究兴趣、学术建议等搜索服务。

![截屏2022-06-03 01.03.13](/Users/minervaning/Library/Application Support/typora-user-images/截屏2022-06-03 01.03.13.png)

#### 请大胆谈谈本文有何不足或者局限性

​		感觉本文是很实用很纪实的一篇文章，作者先是花了很多心思，每一步跑了很多个模型，一步步把这个网站搭出来；又花了十多年修这个网站，不断在加新的服务和下架不好的服务，我觉得我才疏学浅，很难谈出有什么不足，倒是有很多可取之处……

​		首先是对于规模如此庞大、工作量这样巨大的一个流程，能分块分步讲清楚，并每一步有对应的检验准确性方法，我觉得作者事先对实验和文章结构的规划肯定十分清楚。我印象最深刻的是学术网络建模一步提到的ACT三个模型的建模思路很细致入微，对我思索主题模型中题目、会议与作者这三个维度的关系有很大启发。

​		如果硬要我鸡蛋里挑骨头，那我只好不情不愿地觉得，一是本文使用的模型似乎没有详细描述训练方法（所以我猜测大部分是预训练模型，只在本文的数据集上稍稍训练一下即可使用？），这一步对于后人复现工程而言有点模糊；二是本文提出的三个ACT模型，似乎只在后文的搜索服务中使用了ACT1，而我觉得ACT2和ACT3的想法似乎更巧妙，可以一试；三是本文似乎在将理论投入应用和在工作量上的贡献稍大，并不是以创新性取胜的。不过无伤大雅，读完确实给我很大启发……😭。
