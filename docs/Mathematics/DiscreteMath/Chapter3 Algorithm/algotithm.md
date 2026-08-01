---
title: 3.1 算法
tags:
    - 离散数学
---

**定义1**$\qquad$算法是进行一项计算或解决一个问题的精确指令的有限序列.

**算法1**

$$
\begin{aligned}
&\text{寻找有限序列中的最大值}\\
&\mathbf{procedure}\ max\{a_1,a_2,\cdots,a_n:\text{integers}\}\\
&max:=a_1\\
&\mathbf{for}\ i:= 2\ \mathbf{to}\ n\\
&\qquad\mathbf{if}\ max<a_i\ \mathbf{then}\ max := a_i\\
&\mathbf{return}\ max
\end{aligned}
$$

**算法1的C++实现**
```cpp
int find_max_element(int* arr, int n)
{
	int max = arr[0];
	for (int i = 1;i < n;i++)
	{
		if (max < a[i])
			max = a[i];
	}
	return max;
}
```


!!!note 算法的性质
    - 输入: 算法从一个指定的集合得到输入值
    - 输出: 对每个输入值集合,算法都要从一个指定的集合中产生输出值.输出值就是问题的解
    - 确定性: 算法的步骤必须是准确定义的
    - 正确性: 对每一组输入值,算法都应产生正确的输出值
    - 有限性: 对任何输入算法都应在有限(可能很多)步之后产生期望的输出
    - 有效性: 算法的每一步都应能够准确地在有限时间内完成
    - 通用性: 算法过程应该可以应用于期望形式的所有问题,而不只是用于一组特定的输入值.

# 搜索算法

$$
\begin{aligned}
&\text{线性搜索算法}\\
&\mathbf{procedure}\ linear\ search(x:\text{integers},a_1,a_2,\cdots a_n:\text{distinct integers}\}\\
&i:=1\\
&\mathbf{while}\ (i<n\ \mathbf{and}\ x\ne a_i)\\
&\mathbf{if}\ i\le n\ \mathbf{then}\ location := i\\
&\mathbf{else}\ location := 0\\
&\mathbf{return}\ location
\end{aligned}
$$

**线性搜索算法的C++实现**

```cpp
int linear_search(int* arr, int n, int x)
{
	int i, location = 1;
	while (i <= n && x != arr[i])
	{
		i++;
	}
	if (i <= n)
		location = i;
	else
		location = 0;
	return location;
}
```
