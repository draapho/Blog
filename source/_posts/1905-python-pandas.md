---
title: Pandas Dataframe 入门
date: 2019-05-20
categories: python
tags: [python, pandas]
description: 如题.
---

# 1 创建DataFrame
对于一个用python做数据处理的人来说，pandas是必须要了解的。
对于一个数据处理工具来说，读写是最基本的，
下面是我最近整理的关于pandas一些基本本操作，主要包括以下内容：
- 如何创建DataFrame
- 如何读取DataFrame的值，读一行/列、读多行/列
- 如何对DataFrame赋值
- 如何对DataFrame插入一（多）行/列
- 如何删除DataFrame的一（多）行/列


开始前先引入两个库
``` python
import pandas as pd
import numpy as np
```

## 1.1 利用字典创建

利用字典创建DataFrame:
``` python
data={"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":['zhangsan','李四',999,0.1]}
df=pd.DataFrame(data,index=[1,2,3,4])

# 结果演示
>>> df
        one  two     three
1 -1.183802  1.0  zhangsan
2  1.426724  2.0        李四
3 -1.530958  3.0       999
4 -0.939147  4.0       0.1
```

- 如果创建df时不指定索引，默认索引将是从0开时，步长为1的数组。
- df的行、列可以是不同的数据类型，同行也可以有多种数据类型。
- df创建完成好可以重新设置索引，通常用到3个函数：`set_index`、`reset_index`、`reindex`


### 1.1.1 `set_index`

`set_index`用于将df中的一行或多行设置为索引. 用法:
``` python
df.set_index('one')
df.set_index(['one'],drop=False)
# 参数drop默认为True，意为将该列设置为索引后从数据中删除，如果设为False，将继续在数据中保留该行。

# 结果演示
>>> df.set_index('one')
           two     three
one
-1.183802  1.0  zhangsan
 1.426724  2.0        李四
-1.530958  3.0       999
-0.939147  4.0       0.1

>>> df.set_index(['one'],drop=False)
                one  two     three
one
-1.183802 -1.183802  1.0  zhangsan
 1.426724  1.426724  2.0        李四
-1.530958 -1.530958  3.0       999
-0.939147 -0.939147  4.0       0.1
```

``` python
df.set_index(['one','two'])
df.index=['a','b','c','d']
# 如果要设置的索引不在数据中, 可以用index直接设置

# 结果演示
>>> df
        one  two     three
a -1.183802  1.0  zhangsan
b  1.426724  2.0        李四
c -1.530958  3.0       999
d -0.939147  4.0       0.1

>>> df.set_index(['one','two'])
                  three
one       two
-1.183802 1.0  zhangsan
 1.426724 2.0        李四
-1.530958 3.0       999
-0.939147 4.0       0.1
```


### 1.1.2 `reset_index`

`reset_index`用于将索引还原成默认值，即从0开始步长为1的数组。
``` python
df.reset_index(drop=True)
df.set_index(['one'],drop=False)
# 参数drop默认值为False，意为将原来的索引做为数据列保留，如果设为True，原来的索引会直接删除。

# 结果演示
>>> df.reset_index()
  index       one  two     three
0     a -1.183802  1.0  zhangsan
1     b  1.426724  2.0        李四
2     c -1.530958  3.0       999
3     d -0.939147  4.0       0.1

>>> df.reset_index(drop=True)
        one  two     three
0 -1.183802  1.0  zhangsan
1  1.426724  2.0        李四
2 -1.530958  3.0       999
3 -0.939147  4.0       0.1
```

### 1.1.3 `reindex`

`reindex`比较复杂，也不常用到，这里是基础篇，不做大量说明，感兴趣的朋友可以看 [官方文档](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reindex.html)


## 1.2 利用数组创建
``` python
data=np.random.randn(6,4)       #创建一个6行4列的数组
df=pd.DataFrame(data,columns=list('ABCD'),index=[1,2,'a','b','2006-10-1','第六行'])

# 结果演示
>>> df
                  A         B         C         D
1         -0.173690  0.004300 -0.896126  0.360287
2          1.493732  0.784469 -0.799769 -1.828341
a         -0.678492  0.613644  1.835787  0.252200
b         -1.347327  0.134869 -0.595432 -0.533671
2006-10-1  0.178216 -0.690090 -0.625436  1.377065
第六行    -1.534302 -0.147462  0.703847  0.221454
```

## 1.3 创建一个空DataFrame
``` python
pd.DataFrame(columns=('id','name','grade','class'))

# 结果演示
>>> pd.DataFrame(columns=('id','name','grade','class'))
Empty DataFrame
Columns: [id, name, grade, class]
Index: []
```


# 2 读DataFrame
为了便于理解，以下面DataFrame为例，对其读写操作展开说明：
``` python
>>> data=np.random.randn(6,4)
>>> df=pd.DataFrame(data,columns=list('ABCD'),index=[1,2,'a','b','2006-10-1','第六行'])
>>> df
                  A         B         C         D
1         -0.173690  0.004300 -0.896126  0.360287
2          1.493732  0.784469 -0.799769 -1.828341
a         -0.678492  0.613644  1.835787  0.252200
b         -1.347327  0.134869 -0.595432 -0.533671
2006-10-1  0.178216 -0.690090 -0.625436  1.377065
第六行    -1.534302 -0.147462  0.703847  0.221454
```

## 2.1 按列读取

### 2.1.1 `df.列名`

``` python
# 该方法每次只能读取一列。
df.A

# 结果演示
>>> df.A
1            1.787797
2            0.098504
a           -0.361166
b            0.337533
2006-10-1   -0.628970
第六行          3.356526
Name: A, dtype: float64
```

### 2.1.2 `df['列名']` `df[['列名']]` `df[['列名1','列名2','列名n']]`

``` python
# 该方法每次只能读取一列。
df['A']
df[['A','C','D']]

# df['A']和 df[['A']] 返回结果的值相同，但数据结构有差异,
# 用 type(df['A']),type(df[['A']]) 查看。 前者为series, 后者为DataFrame.

# 结果演示
>>> df['A']
1            1.787797
2            0.098504
a           -0.361166
b            0.337533
2006-10-1   -0.628970
第六行       3.356526
Name: A, dtype: float64

>>> df[['A','C','D']]
                  A         C         D
1          1.787797 -0.668013  0.554594
2          0.098504 -0.420558  0.508395
a         -0.361166  0.423340 -2.039099
b          0.337533  0.378315  0.485731
2006-10-1 -0.628970  1.152818 -0.671454
第六行     3.356526  0.854735 -0.768296

>>> type(df['A']),type(df[['A']])
(<class 'pandas.core.series.Series'>, <class 'pandas.core.frame.DataFrame'>)
```

### 2.1.3 `.iloc[:,colNo]` `.iloc[:,colNo1:colNo2]`

按列号读取，有时候我们可能更希望通过列号（1，2，3…）读取数据而不是列名，
又或着我们要读取多行的时候一个一个输入列名是很麻烦的，
我们希望有最简单的代码读取我们最想要的内容，
`.iloc` 方法可以让我们通过列号索引数据，具体如下：

``` python
df.iloc[:1]         # 读取第一列
df.iloc[:,1:3]      # 读取第1列到第3列
df.iloc[:,2:]       # 读取第2列之后的数据
df.iloc[:,:3]       # 读取前3列数据

# 这其实是按单元格读取数据的特殊写法，如果有疑问请看 2.3 按单元格读取数据。
```


## 2.2 按行读取

### 2.2.1 `.loc['行标签']` `.loc[['行标签']]` `.loc[['行标签1','行标签2','行标签n']]`

`.loc`根据行标签索引数据，这里的行标签可以理解为索引（没有深入研究，但是在这里，行标签=索引）,
比如我们要分别读取第1行和第3行就是`df[[1]]`、`df[['a']]`，
如果该df的索引变为`['a', 'b', 'c', 'd', 'e', 'f']`，分别读取第1行和第3行的操作将变成`df[['a']]`,`df[['c']]`，
也就是说.loc后面的'行标签'必须在索引中。

``` python
df.loc[[1]]
df.loc[[1,'a','2006-10-1']]
# df.loc[1] 和 df.loc[[1]] 返回结果的值相同，但数据结构有差异
# 用 type(df.loc[1]),type(df.loc[[1]]) 查看。 前者为series, 后者为DataFrame.

# 结果演示
>>> df.loc[[1]]
          A         B         C         D
1  1.787797  0.366138 -0.668013  0.554594

>>> df.loc[[1,'a','2006-10-1']]
                  A         B         C         D
1          1.787797  0.366138 -0.668013  0.554594
a         -0.361166 -0.427358  0.423340 -2.039099
2006-10-1 -0.628970 -1.219419  1.152818 -0.671454

>>> type(df.loc[1]),type(df.loc[[1]])
(<class 'pandas.core.series.Series'>, <class 'pandas.core.frame.DataFrame'>)
```

### 2.2.2 `.iloc['行号']` `.iloc[['行号']]` `.iloc[['行号1','行号2','行号n']]`
`.iloc`根据行号索引数据，行号是固定不变的，不受索引变化的影响，
如果df的索引是默认值，则.loc和.iloc的用法没有区别，因为此时行号和行标签相同。


`.iloc`还可以通过切片的方式读取数据，所谓切片就是给出要读数据的首尾位置，
然后读取首尾中间这“一片”数据（个人理解，可能理解的不对或比较片面，对此有疑惑的朋友请自行查阅相关资料）
比如我们要读取第1行到第4行的数据，利用切片的方法就是 `df.iloc[1:5]`

``` python
df.iloc[[1]]
df.iloc[[1,2,5]]
df.iloc[1:5]        # 切片形式
df.iloc[:5]         # 读取第0行到第4行的数据；
df.iloc[8:]         # 读取第8行后所有数据，包括第8行；
df.iloc[3,6]        # 读取第3行到第6行的数据，包括第3行但不包括第6行。

# 结果演示
>>> df.iloc[[1]]
          A         B         C         D
2  0.098504 -1.332709 -0.420558  0.508395

# 可以看到 df.loc[1] 和 df.iloc[1] 读到的内容是不一样的，
# df.loc[1] 读取的是索引号为1的那一行，df.iloc[1] 读取的是第1行。

>>> df.iloc[[1,2,5]]
            A         B         C         D
2    0.098504 -1.332709 -0.420558  0.508395
a   -0.361166 -0.427358  0.423340 -2.039099
第六行  3.356526 -0.945234  0.854735 -0.768296

>>> df.iloc[1:5]
                  A         B         C         D
2          0.098504 -1.332709 -0.420558  0.508395
a         -0.361166 -0.427358  0.423340 -2.039099
b          0.337533  1.770279  0.378315  0.485731
2006-10-1 -0.628970 -1.219419  1.152818 -0.671454
```

### 2.2.3 ~~`.ix`~~
`.ix` 已经不推荐使用, 所以就不举例分析了.

``` python
# 结果演示
>>> df.ix[[1]]
__main__:1: DeprecationWarning:
.ix is deprecated. Please use
.loc for label based indexing or
.iloc for positional indexing
```

### 2.2.4 `at` `iat`
`at`、`iat` 这里就不做介绍了，因为上面的方法完全够用了，感兴趣的话可以看 [官方文档](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.at.html)
`.loc` `.iloc` 完全可以满足DataFrame的读取操作，所以`ix`,`at`,`iat`并不推荐使用。


## 2.3 按单元格读取

### 2.3.1 `df[col][row]`
读取一个单元格的数据时推荐使用，也可以写成 `df.col[row]`
``` python
df['A'][1]
df.A[1]

# 结果演示
>>> df['A'][1]
1.7877970995354475
>>> df.A[1]
1.7877970995354475
```

### 2.3.2 `.loc`
``` python
# 读取一个单元格：
df.loc[row][col]
df.loc[row,col]
```

``` python
# 读取一行多列：
df.loc[row][[col1,col2]]
df.loc[row,[col1,col2]]
df.loc[row][firstCol:endCol]
df.loc[row,firstCol:endCol]

# 结果演示
>>> df.loc[1][['A','B']]
A    1.787797
B    0.366138
Name: 1, dtype: float64
>>> df.loc[1,['A','B']]
A    1.787797
B    0.366138
Name: 1, dtype: float64
>>> df.loc[1]['A':'C']
A    1.787797
B    0.366138
C   -0.668013
Name: 1, dtype: float64
>>> df.loc[1,'A':'C']
A    1.787797
B    0.366138
C   -0.668013
Name: 1, dtype: float64
```

``` python
# 读取多行一列：
df.loc[[row1,row2]][col]
df.loc[[row1,row2]].col
df.loc[[row1,row2],col]
# 行号不能用切片!

# 结果演示
>>> df.loc[[1,2]]['A']
1    1.787797
2    0.098504
Name: A, dtype: float64
>>> df.loc[[1,2,'b']].B
1    0.366138
2   -1.332709
b    1.770279
Name: B, dtype: float64
>>> df.loc[[1,'a'],'A']
1    1.787797
a   -0.361166
Name: A, dtype: float64
```

``` python
# 读取多行多列:
df.loc[[row1,row2],[col1,col2]]
df.loc[[row1,row2]][[col1,col2]]
df.loc[[row1,row3],firstCol:endCol]
# 行号不能用切片!

# 结果演示
>>> df.loc[[1,2]][['A','C']]
          A         C
1  1.787797 -0.668013
2  0.098504 -0.420558
>>> df.loc[[1,'b'],['A','B']]
          A         B
1  1.787797  0.366138
b  0.337533  1.770279
>>> df.loc[[1,'b'],'A':'C']
          A         B         C
1  1.787797  0.366138 -0.668013
b  0.337533  1.770279  0.378315
```

### 2.3.3 `.iloc`
``` python
# 读取一个单元格：
df.iloc[rowNo].col
df.iloc[rowNo][col]
df.iloc[rowNo,colNo]
# 不支持 df.iloc[rowNo,col]
```

``` python
# 读取一行多列：
df.iloc[rowNo,firestColNo,endColNo]
df.iloc[rowNo][[col1,col2]]
df.iloc[rowNo][firesCol:endCol]
# 不支持 df.iloc[rowNo,[col1,col2]]
# 不支持 df.iloc[rowNo,firstColNo:endColNo]

# 结果演示
>>> df.iloc[0,1:3]
B    0.366138
C   -0.668013
Name: 1, dtype: float64
>>> df.iloc[0][['A','B']]
A    1.787797
B    0.366138
Name: 1, dtype: float64
>>> df.iloc[0]['A':'C']
A    1.787797
B    0.366138
C   -0.668013
Name: 1, dtype: float64
```

``` python
# 读取多行一列：
df.iloc[[rowNo1,rowNo2],colNo]
df.iloc[firstRowNo:endRowNo,colNo]
df.iloc[[rowNo1,rowNo2]][col]
df.iloc[firstRowNo,endRowNo][col]

# 结果演示
>>> df.iloc[0:3,1]
1    0.366138
2   -1.332709
a   -0.427358
Name: B, dtype: float64
>>> df.iloc[1:3]['A']
2    0.098504
a   -0.361166
Name: A, dtype: float64
>>> df.iloc[[1,2,4]]['A']
2            0.098504
a           -0.361166
2006-10-1   -0.628970
Name: A, dtype: float64
```

``` python
# 读取多行多列：
df.iloc[firstRowNo:endRowNo,firstColNo:endColNo]
df.iloc[[RowNo1,RowNo2],[ColNo1,ColNo2]]
df.iloc[firstRowNo:endRowNo][[col1,col2]]

# 结果演示
>>> df.iloc[0:3,1:4]
          B         C         D
1  0.366138 -0.668013  0.554594
2 -1.332709 -0.420558  0.508395
a -0.427358  0.423340 -2.039099
>>> df.iloc[0:3, [1,2,3]]
          B         C         D
1  0.366138 -0.668013  0.554594
2 -1.332709 -0.420558  0.508395
a -0.427358  0.423340 -2.039099
>>> df.iloc[1:3][['A','B','C']]
          A         B         C
2  0.098504 -1.332709 -0.420558
a -0.361166 -0.427358  0.423340
```

### 2.3.4 ~~`.ix` `at` `iat`~~
`ix`,`at`,`iat`不推荐使用


# 3 写DataFrame/DataFrame赋值
## 3.1 按列赋值
``` python
df.col=colList/colValue
df[col]=colList/colValue
# 如果用一个列表或数组赋值，其长度必须和df的行数相同。

# 结果演示
>>> df.A=[1,2,3,4,5,6]
>>> df['A']=0
```

## 3.2 按行赋值
``` python
df.loc[row]=rowList
df.loc[row]=rowValue
```

## 3.3 给多行多列赋值

DataFrame的读写操作是多变的，这里也仅仅列出了几种常用的方法，熟练一种方式即可。
``` python
df.loc[[row1,row2],[col1,col2]]=value/valueList
df.iloc[[rowNo1,rowNo2],[colNo1,colNo2]]=value/valueList
df.iloc[[rowNo1,rowNo2]][[col1,col2]]=value/valueList
df.ix[firstRow:endRow,firstCol:endCol]=value/valueList
```

# 4 DataFrame的插入
初始化 DataFrame, 以下面DataFrame为例展开说明
``` python
data={"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":['zhangsan','李四',999,0.1]}
df=pd.DataFrame(data,index=[1,2,3,4])

# 获得如下DataFrame
        one  two     three
1 -1.183802  1.0  zhangsan
2  1.426724  2.0        李四
3 -1.530958  3.0       999
4 -0.939147  4.0       0.1
```

## 4.1 在任意位置插入
``` python
# 插入一列
insert(ioc,column,value)
# ioc:要插入的位置
# colunm:列名
# value:值

# 结果演示
>>> df.insert(2,'four',[11,22,33,44])
>>> df
        one  two  four     three
1 -1.417222  1.0    11  zhangsan
2  1.251673  2.0    22        李四
3 -0.103710  3.0    33       999
4 -1.237722  4.0    44       0.1
```

``` python
# 插入一行
row={'one':111,'two':222,'three':333}
df.loc[1]=row       # or
df.iloc[1]=row      # or
df.ix[1]=row
```

## 4.2 在末尾插入
如果插入一行或一列，用上面的方法把插入位置改为末尾即可，下面给出插入多行多列的方法。

``` python
# 按列合并, 插入多行
df.append(df2)
# 效果等同于 pd.concat([df,df2],axis=0)

# 结果演示
# 初始化列表df, df2, 用于列合并
>>> data={"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":['zhangsan','李四',999,0.1]}
>>> df=pd.DataFrame(data,index=[1,2,3,4])
>>> data={"one":[222,214],"two":np.linspace(11,22,2), "three":['AAA', 'BBB']}
>>> df2=pd.DataFrame(data)

>>> df.append(df2)
          one   two     three
1    0.168605   1.0  zhangsan
2    0.466244   2.0        李四
3   -0.176716   3.0       999
4    1.066139   4.0       0.1
0  222.000000  11.0       AAA
1  214.000000  22.0       BBB
```

``` python
# 插入多行多列
pandas.concat(objs, axis=0, join_axes=None, ignore_index=False)
# objs:合并对象
# axis:合并方式，默认0表示按列合并，1表示按行合并
# ignore_index:是否忽略索引


# 结果演示

# 按行合并
初始化列表df, df1, 用于行合并
>>> data={"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":['zhangsan','李四',999,0.1]}
>>> df=pd.DataFrame(data,index=[1,2,3,4])
>>> data={"four":np.random.randn(4),"five":np.linspace(1,100,4)}
>>> df1=pd.DataFrame(data,index=[1,2,3,4])
>>> df1
       four   five
1 -0.119780    1.0
2 -0.290202   34.0
3  1.209032   67.0
4  0.997500  100.0

>>> pd.concat([df,df1],axis=1)
        one  two  four     three      four   five
1 -1.417222  1.0    11  zhangsan -0.119780    1.0
2  1.251673  2.0    22      李四 -0.290202   34.0
3 -0.103710  3.0    33       999  1.209032   67.0
4 -1.237722  4.0    44       0.1  0.997500  100.0
# 若 df2 和 df 的列数不相同, 空缺的行内容会别填充为 NaN


# 按列合并
# 初始化列表df, df2, 用于列合并
>>> data={"one":np.random.randn(4),"two":np.linspace(1,4,4),"three":['zhangsan','李四',999,0.1]}
>>> df=pd.DataFrame(data,index=[1,2,3,4])
>>> data={"one":[222,214],"two":np.linspace(11,22,2), "three":['AAA', 'BBB']}
>>> df2=pd.DataFrame(data)
>>> df2
   one   two three
0  222  11.0   AAA
1  214  22.0   BBB

>>> pd.concat([df,df2],axis=0)                                                                 }
          one   two     three
1    0.034967   1.0  zhangsan
2   -1.888495   2.0        李四
3    1.045013   3.0       999
4   -0.313027   4.0       0.1
0  222.000000  11.0       AAA
1  214.000000  22.0       BBB
# 若 df2 和 df 的列数不相同, 空缺的列内容会别填充为 NaN
```

# 5 DataFrame的删除操作
``` python
drop(labels, axis=0, level=None, inplace=False)
# lables：要删除数据的标签
# axis：0表示删除行，1表示删除列，默认0
# inplace:是否在当前df中执行此操作

# 结果演示
# 下述操作不会影响 df 本身, 因为没有被重新赋值.
>>> df.drop(['one','two'],axis=1)
      three
1  zhangsan
2        李四
3       999
4       0.1
>>> df.drop([1,3],axis=0)
        one  two three
2  0.466244  2.0    李四
4  1.066139  4.0   0.1
```

# 6 DataFrame的高级操作
## 6.1 `drop_duplicates` 删除重复行
``` python
df.drop_duplicates()                    # 删除重复行
df.drop_duplicates(['A','B','C'])       # 指定要判断的列, 删除重复内容的行.
```

## 6.2 `fillnan` 填充无效值
``` python
df.fillna('我是无效值')                  # 将 NaN 替换为 '我是无效值'
```

----------

***转载自 [pandas 入门：DataFrame的创建，读写，插入和删除](https://blog.csdn.net/xtfge0915/article/details/52938740#) 和 [pandas进阶：DataFrame高级操作](https://blog.csdn.net/xtfge0915/article/details/83477062)有删改***