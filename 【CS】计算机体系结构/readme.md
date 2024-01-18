# readme

笔记在 [BLOG-CA](https://ruoxining.github.io/OBvault/CS/CA/)

## 历年卷

历年卷文件夹来源 = CC98 + github - 年龄比较大的题

据说体系课改后刚上了两三年，所以题目不多

最后就剩下了两三份

## 2324回忆卷

老师说是会考计组内容，实际感觉计组内容很少很少，只有一个有关cache计算的题目涉及到了一步cache块数的计算

出题方式据说是五位老师各出一套，最后从五位老师出的题里sample。何老师智云回放里有一份样例卷子可以做一下 [智云回放](https://classroom.zju.edu.cn/livingroom?course_id=56686&sub_id=1027410&tenant_code=112)。我有截图下来但是太懒了，不想往这个文档整理。可能如果本仓库star多了我怕丢人就会整理进来。

选择 25 个，几乎记不起来了，很基础的概念题感觉有40%，有少量有关性能指标的计算

记得一个问 Tomasulo with ROB 的 issue 条件是 ____，且当 ______ 为空时，操作数可以被放入 _____。

A. RS 和 ROB 都为空；ROB；RS

B. RS；FU；register

C. RS 或 ROB；啥啥啥；啥啥啥

D. ROB；啥啥啥；啥啥啥

记得它是因为觉得哪个选项也不对，因为我觉得应该填 RS 和 ROB；FU；FU。如果有知道的同学请告诉我该选啥。

大题六个

- 前三个计算
  - 一个 CPU 5 核，每个核平均多少时间发射一条指令，其中20%是无跳转，80%是有跳转，问 CPI。这道是上面我给的智云链接在 30min ~ 31min 处的一道原题。
 
  - 两个大小不同的 cache，一个 8B，一个忘了几路组关联 64B，分别给了两个 cache 的 miss penalty 为 10ns 和 1000ns，求证在该情景下用小 cache 比较合适。我好像是先分别算出了两个 cache 的块数，得到结论小 cache 的 miss rate 为大 cache 的可能是 8 倍，这样根据那个 cache 性能的公式算出来小 cache 更快，得证。

  - 给了两个 1024 * 1024 矩阵相加循环代码，第一个每次步长 16，第二个步长是 1，然后说矩阵里的 block size 是 32 bit，cache 大小算出来刚好是一个 block 大小。让求两种代码的 miss rate 只比。这道是上面我给的智云链接在 30min ~ 31min 处的一道选择题原题改的。

- 后三个分别是
  - Snooping 协议写流程。在 A4 上抄写 ppt 上那道例题的 FSM 和表格即可会做。
    
  - 正常的 pipeline CPU with speculation 画流水线
    
  - 目录协议写流程。也是在 A4 上抄道例题。
 
## A4

A4必须手写，好像目前我遇到的考试里只有 OS 的 3 页是允许打印的。因为考试后 A4 一起交上去了所以没能给大家共享一下。

讲点抄 A4 的心得，如果把纸分成 16 块，大概 
- 1/16 抄了公式（公式在课本最开头有个汇总，可以照抄）
  
- 1/16 抄了 cache 优化方法那个总结表
  
- 1/16 抄了对每种 cache 优化方法的一句话介绍
  
- 1/16 cache 在计组里一些概念（映射方法，三种 miss 之类的），画了 physically tagged, virtually indexed 那个流程图
  
- 1/16 抄了 scoreborad / Tomasulo / Tomasulo with ROB 的一个对比表格，这个表格在瓜豪直播里看见的，现在找不到了，如果找到我补上
  
- 3/16 分别抄了个 scoreborad / Tomasulo / Tomasulo with ROB 例题，这三个算法我速成用的这套帖子 [计算机体系结构-记分牌ScoreBoard](https://zhuanlan.zhihu.com/p/496078836)， [计算机体系结构-Tomasulo算法](https://zhuanlan.zhihu.com/p/499978902)， [计算机体系结构-重排序缓存ROB](https://zhuanlan.zhihu.com/p/501631371)

- 1/16 抄了有 TOS POS 那五个概念的流程图（对不起仅仅一天我已经忘了这块是讲的啥了），在上面我给的智云链接里有这个图。选择题考到了一个，问哪个消除了 W->R W->W 依赖之类的。
  
- 3/16 分别抄了 snooping 协议的 FSM，UMA 和 NUMA 的基本概念，snooping 和目录协议的各一个例题
  
剩下的抄的啥不记得了。可以参考这个划分方法。基本上都用到了。

还有一点是如果是考前一晚上，我觉得有限的时间里看懂一些算法比抄满 A4 纸更重要。一定要记得 A4 纸抄了看不懂不会用等于没抄。
