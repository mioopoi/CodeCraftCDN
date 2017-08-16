
这是我参加[CodeCraft2017华为软件精英挑战赛](http://codecraft.huawei.com/)时用[Gurobi](http://www.gurobi.com/)求解赛题的整数规划
模型时所写的建模代码。至于`既然比赛不允许用任何第三方ILP Solver，还要线下求最优解`的原因，在于**求最优解可以
为启发式算法的设计提供方向**。

工具版本：
- Python: 2.7.11 (Anaconda2)
- Gurobi: 7.0.2

ps. 这里的代码主要是针对初赛赛题的。

官方提供的用例在文件夹`low`, `mid`和`high`中，分别对应初级、中级和高级用例。

主要源文件和功能是:
- `read_graph.py`: 读文件，建图(使用`NetworkX`库)
- `solver.py`: 用`Gurobi`进行整数规划建模并求解
- `autorun.py`: 批量求解

其他几个文件说明如下：
`test_network_simplex.py`是我测试networkx中提供的网络单纯形性能写的脚本，和整数规划无关，大家看看就好

作者：Huafan Li
邮箱：huafan@seu.edu.cn