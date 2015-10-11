# Conference Track Management

**核心思路：**
有多个talks要根据条件分配到多个session，session又要分配到多个tracks，
所以建立三个类Talk、Session和Track一一对应，并根据具体条件实现相应的类方法与属性。

题目类似背包问题，但并无要求尽可能使track数量少（即每个track包含talks尽量多）。我的核心思路是把talk按时间由大到小排序，然后从大的talk开始分配给session，当session不能再包含大talk时在从最小的talk开始尝试继续分配给session直到session包含talk最大化。

在具体解答问题过程中出现对题目条件的一些疑问但因不能提问故按本人理解有几个约定：

 1. 题目条件没有说是否可以出现下午不安排talk。根据题目条件下午的working event不早于4点推测下午必须安排talk，否则working event时间必早于4点。
 2. 题目条件没有说明极端情况下是否可以出现早上不安排talk。根据*约定1*中下午必须安排talk，则有可能出现上午没有talk的极端情况。

PS:根据题目条件，问题中的示例输出有一个错误：

> 04:00PM Rails for Python Developers lightning
> 05:00PM Networking Event

应该是：
04:00PM Rails for Python Developers lightning  
04:05PM Networking Event

**运行代码:**

 1. 将talk数据写入SampleInput.txt
 2. 进入src/ctm/
 3. 运行`python main.py`
 4. 或者运行`python main.py --f your_input.txt`来输入你的数据文件

**测试代码:**

请使用第三方测试库nose：

    pip install nose
    pip install coverage

测试代码请直接在src目录下运行：

    nosetests --with-coverage -v

*解答者：*
*张建奇 rapospectre@163.com*
