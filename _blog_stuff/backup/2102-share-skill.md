---
title: 交易市场思路
date: 2021-02-03
categories: market
tags: [market]
---

# 总览
- [交易市场思考](https://draapho.github.io/2019/03/26/1902-trading-rule/)
- [波浪理论简述](https://draapho.github.io/2019/04/26/1903-wave-principle/)
- [你将不会成为一个伟大的投资人](https://draapho.github.io/2019/06/25/1907-investor/)
- [交易市场阶段性探索心得](https://draapho.github.io/2020/02/09/2001-exploration/)
- [波浪理论口诀](https://draapho.github.io/2020/08/06/2005-wave-mnemonic/)
- [波浪理论感悟](https://draapho.github.io/2020/08/07/2006-wave-thinking/)
- [交易市场思路](https://draapho.github.io/2021/02/03/2102-share-skill/)


# 股市波动与电子学
- 股市为什么总是之字形前行, 闪电为什么总是呈现之字形?
    - 闪电呈现之字形是因为空气有电容的作用, 即对电子的储能作用.
    - 股市呈现之字形是因为人能容忍一定时间和程度的亏损或者盈利而持仓不动. 具有类似的储能作用.
- 股市的K线图, 本质是什么?
    - K线图是股价图, 本质的话, 对应的是电子学中的电压.
    - 电子学中, 决定电压的是电流和阻抗(电阻, 电容, 电感). 进一步讲, 是电压造成电势能差促使大量电子流动, 而路径则阻碍电子流动, 形成最终的电流.
    - 股市中, 情况较为复杂. 因为有些纯价值派的存在, 人家的参考依据是企业和行业的业绩而非K线图, 但无论如何, 这些人的行为也是反应到K线图上的, 即K线图对他们而言不是因, 只是无关紧要的果. 对于纯技术派而言, K线图即是因又是果.
    - 大差不差的: **金钱对应于电子. 股价对应于电压. K线图对应于历史电压波形. 阻抗大小对应于预期值.**
    - 金钱供应量决定了股价的可持续性. 这很好理解, 若电压很高, 但电子不足, 只能是脉冲式的波动. 因而, 大资金的态度尤为重要.
    - 股市有明显的自激振荡模式, 并且自激振荡往往呈现黄金比例的递增; 也有震荡衰减模式.
    - 套用电子学时, 麻烦的是:
        - 参数的不确定性. 譬如, 对应于阻抗的预期值, 必然与K线图呈现某种关系的波动, 较难测量.
        - 人类的相互博弈性质, 这些参数随时都在变, 就算有测量公式, 偷偷测量是一个值, 公开测量立刻是另外一个值.
        - 数学工具的不完善. 由于K线图的非平滑连续特性, 微积分是无法直接使用的.
- 短线, 中线和长线.
    - 短线看情绪, 情绪就是预期值的变化.
    - 中线看资金, 主力资金的态度决定行情的可持续性.
    - 长线看业绩, 由于主力资金只能慢进慢出, 必须追求稳定性, 而业绩是这几个要素里面, 确定性和稳定性最高的.
    - 更顶尖的资金, 看的是行业发展和社会发展趋势. 毕竟级别越大, 变化就越缓慢, 确定性越高, 也就能容纳更多的资金.
    - 进入交易市场的人, 全部是以盈利为目的的. 投机与投资, 无所谓好坏和高低.


# 彩虹均线
彩虹均线, 黄金比例均线.
核心思路: 均线即持仓成本, 只有所有均线都顺次排列好了, 才是大概率的见底或见顶.

内含双均线交叉, 60/250均线交叉.
金叉: 短均线上叉上升趋势中的长均线
死叉: 短均线下叉下降趋势中的长均线
买点: 短均线下叉上升趋势中的长均线
卖点: 短均线上叉下降趋势中的长均线

``` C
#MAINCHART
INPUT:
  赤(13, 5, 21),
  橙(21, 21, 34),
  黄(34, 34, 89),
  青(89, 55, 143),
  蓝(144, 144, 250);

// 显示所属板块
PE:=DynaInfo(Q_PE),NoDraw;
VL:=DynaInfo(Q_MARKETVAL)/100000000,NoDraw;
DRAWTEXTEX(1, 1, 2, 0, STKNAME+' '+STKLABEL+'   市盈:'+NumToStr(PE,2)+' 市值:'+NumToStr(VL,2)+'亿'+'   '+IndustryName),
    IIF(PE>0 and PE<100 and VL>100,ColorCyan,ColorYellow);


M5:MA(C,5), ColorWhite, LineDot;
PartLine(M5/REF(M5,1)>1.01,M5),ColorWhite, LineThick2;
PartLine(M5/REF(M5,1)<0.99,M5),ColorWhite, LineThick2;

// 赤橙黄绿青蓝紫
M13:MA(C,赤), ColorLightRed;
M21:MA(C,橙), Color00A5FF;
M34:MA(C,黄), ColorYellow;
M60:MA(C,60), ColorGreen;
M89:MA(C,青), ColorCyan;
M144:MA(C,蓝), ColorBlue;
M250:MA(C,250), ColorRed;

// 单K线测顶底
单阳测顶:=C*C/REF(C,1)/0.9, NoDraw;
单阴测低:=C*C/REF(C,1)/1.1, NoDraw;
单K顶底:IF(C>O, 单阳测顶, 单阴测低), NoDraw, ColorWhite;
```


# 均线交叉
倍数移中均线, 短均线右移与长均线交叉点具有强烈的变盘提示作用.
适用与N字形调整, 标准的五浪顶底预测. 但无效交叉点也不少.
核心思路: 移中均线交叉点的对称性. 通过右移移中均线达到预测效果.


``` C
#MAINCHART
#RUN_BY_BAR

#Template "
均线M Param#1, 0不显示短均线,
均线N Param#2, -1显示长均线,
"

INPUT:
    M(64,0,999),
    N(0,-1,999);


// 显示所属板块
PE:=DynaInfo(Q_PE),NoDraw;
VL:=DynaInfo(Q_MARKETVAL)/100000000,NoDraw;
DRAWTEXTEX(1, 1, 2, 0, STKNAME+' '+STKLABEL+'   市盈:'+NumToStr(PE,2)+' 市值:'+NumToStr(VL,2)+'亿'+'   '+IndustryName),
    IIF(PE>0 and PE<100 and VL>100,ColorCyan,ColorYellow);



// 中长均线交叉
IF (N==-1 or N>M) Then Begin
P:=IIF(N==-1, M*4, N);                  // 默认长均线为4倍短均线

// 中期均线右移
T2:=P/4;
M20:=ma(C,P/2)*(2-MOD(P,2));
M21:=ma(C,1+P/2)*(MOD(P,2));
M2:=(M20+M21)/2;
M24:=M2*(4-MOD(P,4));
M25:=Ref(M2,1)*(MOD(P,4));
M26:=(M24+M25)/4;
M2_:=Ref(M26,T2),ColorBrown;
Plot[-T2](M26, 'M2_', ColorBrown);

// 长期均线
M4:ma(C,P),ColorRed,LineThick2;
D4:=EMA(M4-ref(M4,1),5);            // 速率
DL:=SwingLow(1,D4,9,M*4);           // 前速率波谷
DH:=SwingHIGH(1,D4,9,M*4);          // 前速率波峰
DLD4:=BarsLast(Cross(DL,D4),1);     // 速率跌破前低
D4DH:=BarsLast(Cross(D4,DH),1);     // 速率突破前高

////IsSummer:=D4>=0 and DLD4>=D4DH;
//IsAutumn:=D4>=0 and D4DH>DLD4 and ref(D4,DLD4)>0; // 速率跌破前低后再没有突破前高.
//IsWinter:=D4<=0 and D4DH>=DLD4;                       // 速率跌破前低后再没有突破前高.
//IsSpring:=D4<=0 and DLD4>D4DH and ref(D4,D4DH)<0; // 速率突破前高后再没有跌破前低.
//PARTLINE(IsWinter, M4),ColorMagenta,LineThick2;
//PARTLINE(IsAutumn or IsSpring, M4),Color20A4FF,LineThick2;    // 橙色

// 交叉点
D2:=M2_-M4;
W2:=D2+D2-ref(D2,1);                                // 用于预测过零轴
BARCROSS:=BarsLast(D2*W2<=0 and abs(D2)<=abs(W2));  // 过零轴
VERTLINE(BARCROSS==0 or (D2*ref(D2,1)<=0 and BARCROSS > 1)), ColorBrown, LineDashDot;
IF M=0 Then Begin
    D2_4:-D2, NoAxis, ColorGray;
End

// 计算中长均线包围面积
DSUM2:=SUM(D2, 0); // 累加差值
DCROSS2:=BarsLast(D2*ref(D2,1)<=0, 1);
DAREA2:=DSUM2-REF(DSUM2,1+DCROSS2),NoAxis;
DrawNumber(DCROSS2=0 or ISLASTBAR, M4*0.997, REF(DAREA2,1), 1), ColorBrown;
End


// 短中均线交叉
IF M>0 Then Begin
// 短期均线右移
Q:=IIF(N>M/5 and N<M, N, M/2);
T0:=(M-Q)/2;
M00:=ma(C,Q)*(2-MOD(M,2));
M01:=ma(C,1+Q)*(MOD(M,2));
M0:=(M00+M01)/2;            // 忽略误差可直接 M0:=ma(C,M/2)
//  M02:=Ref(M0,T0)*(4-MOD(M,4));
//  M03:=Ref(M0,1+T0)*(MOD(M,4));
//  M0_:(M02+M03)/4,ColorLightGreen;    // 忽略误差可直接 M0_:Ref(M0,T0), 无法显示右移的部分
M04:=M0*(4-MOD(M,4));
M05:=Ref(M0,1)*(MOD(M,4));
M06:=(M04+M05)/4;
M0_:=Ref(M06,T0),ColorLightGreen;
Plot[-T0](M06, 'M0_', ColorLightGreen);

// 中期均线
M1:ma(C,M),ColorGreen, LineThick2;

// 交叉点
D0:M0_-M1,NoDraw, ColorCyan;
//  W00:C-M1, NoAxis, COlorGray, LineDot;
//  VERTLINE(D0*ref(D0,1)<=0), ColorBrown, LineDot; // 交叉最简单的写法
W0:=D0+D0-ref(D0,1);                                // 用于预测过零轴
BARCROSS:=BarsLast(D0*W0<=0 and abs(D0)<=abs(W0));  // 过零轴
VERTLINE(BARCROSS==0 or (D0*ref(D0,1)<=0 and BARCROSS > 1)), ColorBrown, LineDot;
IF (N>=0 and N<M) Then Begin
    D0_1:-D0,NoAxis, ColorBrown;
End

// 计算短中均线包围面积
DSUM:=SUM(D0, 0); // 累加差值
DCROSS:=BarsLast(D0*ref(D0,1)<=0, 1);
DAREA:=DSUM-REF(DSUM,1+DCROSS),NoAxis;
DrawNumber(DCROSS=0, M1*0.997, REF(DAREA,1), 1), ColorGreen;
DrawNumber(ISLASTBAR, M1*0.997, DAREA, 1), ColorGreen;

DPOS:=BarsLast(D0>0 and D0*ref(D0,1)<=0, 1);    // 前一个正面积
DNEG:=BarsLast(D0<0 and D0*ref(D0,1)<=0, 1);    // 前一个负面积
DPOS1:=BarsLast(D0>0 and D0*ref(D0,1)<=0, 2);   // 前二个正面积
DNEG1:=BarsLast(D0<0 and D0*ref(D0,1)<=0, 2);   // 前二个负面积

DrawNumber(DPOS=0 and ABS(REF(DAREA,1))>ABS(REF(DAREA,1+DNEG)) and ABS(REF(DAREA,1))>ABS(REF(DAREA,1+DPOS1)), M1*0.997, REF(DAREA,1), 1), ColorYellow;  // 向上的力
DrawNumber(DNEG=0 and ABS(REF(DAREA,1))<ABS(REF(DAREA,1+DPOS)) and ABS(REF(DAREA,1))<ABS(REF(DAREA,1+DNEG1)), M1*0.997, REF(DAREA,1), 1), ColorYellow;  // 向上的力
DrawNumber(DPOS=0 and ABS(REF(DAREA,1))<ABS(REF(DAREA,1+DNEG)) and ABS(REF(DAREA,1))<ABS(REF(DAREA,1+DPOS1)), M1*0.997, REF(DAREA,1), 1), ColorCyan;    // 向下的力
DrawNumber(DNEG=0 and ABS(REF(DAREA,1))>ABS(REF(DAREA,1+DPOS)) and ABS(REF(DAREA,1))>ABS(REF(DAREA,1+DNEG1)), M1*0.997, REF(DAREA,1), 1), ColorCyan;    // 向下的力

DrawNumber(ISLASTBAR and DAREA<0 and ABS(DAREA)>ABS(REF(DAREA,1+DNEG)) and ABS(DAREA)>ABS(REF(DAREA,1+DPOS1)), M1*0.997, DAREA, 1), ColorYellow;        // 向上的力
DrawNumber(ISLASTBAR and DAREA>0 and ABS(DAREA)<ABS(REF(DAREA,1+DPOS)) and ABS(DAREA)<ABS(REF(DAREA,1+DNEG1)), M1*0.997, DAREA, 1), ColorYellow;        // 向上的力
DrawNumber(ISLASTBAR and DAREA<0 and ABS(DAREA)<ABS(REF(DAREA,1+DNEG)) and ABS(DAREA)<ABS(REF(DAREA,1+DPOS1)), M1*0.997, DAREA, 1), ColorCyan;          // 向下的力
DrawNumber(ISLASTBAR and DAREA>0 and ABS(DAREA)>ABS(REF(DAREA,1+DPOS)) and ABS(DAREA)>ABS(REF(DAREA,1+DNEG1)), M1*0.997, DAREA, 1), ColorCyan;          // 向下的力

End

// 其它
// 5日均线.
M5:ma(C,5), ColorWhite, LineDot;
PartLine(M5/REF(M5,1)>1.01,M5),ColorWhite, LineThick2;
PartLine(M5/REF(M5,1)<0.99,M5),ColorWhite, LineThick2;

// 单K线测顶底
单阳测顶:=C*C/REF(C,1)/0.9, NoDraw;
单阴测低:=C*C/REF(C,1)/1.1, NoDraw;
单K顶底:IF(C>O, 单阳测顶, 单阴测低), NoDraw, ColorWhite;
```


# 慢速KD
通过均线速率的变化和慢速KD, 确定买点, 卖点供参考
多用于大周期, 如周线, 月线的买点提示
由于买点和止损点很容易设置, 比较实用.

``` C
PE:=DYNAINFO(Q_PE),NODRAW;
VL:=DYNAINFO(Q_MARKETVAL)/100000000,NODRAW;
// 显示个股基本信息
PE:=DYNAINFO(Q_PE),NODRAW;
VL:=DYNAINFO(Q_MARKETVAL)/100000000,NODRAW;
DRAWTEXTEX(1, 1, 2, 0, STKNAME+' '+STKLABEL+'   市盈:'+NUMTOSTR(PE,2)+' 市值:'+NUMTOSTR(VL,2)+'亿'+'   '+INDUSTRYNAME),
    IF(PE>0 AND PE<100 AND VL>100,ColorCyan,ColorYellow);
//DRAWTEXTEX(1, 1, 2, 10, BLKNAME),COLORCYAN;

// 成交量强弱对比
RVOL:=EMA(V,5)/SMA(V,20,1);
VBase:="SH000001$Volume";
RBase:=EMA(VBase,5)/SMA(VBase,20,1), NODRAW;
亿元:AMOUNT/100000000, ColorWhite, NODRAW;
换手率:(V/CAPITAL), ColorMagenta, NODRAW;
量强弱:RVOL/RBase, NODRAW, ColorCyan;
O1:=IIF(C<REF(C,1), V, 0);
C1:=IIF(C<REF(C,1), 0, V);
KLINE(O1,0,量强弱*V,C1,1), ColorGray;

// 慢速KD
//N:=9;
//RSV:= (C-LLV(L,N))/(HHV(H,N)-LLV(L,N))*100;
//FASTK:=SMA(RSV,3,1);
//K:SMA(FASTK,3,1),ColorYellow;
N:=34;
RSV:=(C-LLV(L,N))/(HHV(H,N)-LLV(L,N))*100;
K:SMA(RSV,5,1);
D:=SMA(K,5,1),ColorWhite;

KUP:=IF(K/REF(K,1)>1.00, 1, 0);
KDN:=IF(K/REF(K,1)<0.97, 1, 0);
PARTLINE(KUP, K),ColorMagenta;
PARTLINE(KDN, K),ColorCyan;

// 基于均线, 判断背离, 仅供参考!
M:=3;
MC:=SMA(C,M,1),NOAXIS;

DC:=IF(MC<=REF(MC,1) AND MC<=REF(MC,M/2) AND MC<=REF(MC,M), 1, 0);  // 均线下降
UC:=IF(MC>=REF(MC,1) AND MC>=REF(MC,M/2) AND MC>=REF(MC,M), 1, 0);  // 均线上升
DD:=IF(D<=REF(D,1) AND D<=REF(D,M/2) AND D<=REF(D,M), 1, 0);
UD:=IF(D>=REF(D,1) AND D>=REF(D,M/2) AND D>=REF(D,M), 1, 0);
//DRAWNUMBER(DC AND UD, K, 7, 0), ColorMagenta;  // 跌势中, 背离, 准备买入
//DRAWNUMBER(UC AND DD, K, 8, 0), ColorCyan;     // 升势中, 背离, 准备卖出
D1:=ANY(DC AND UD,9);
D2:=ANY(UC AND DD,9);
// 9周期内有过买入信号, K值40以下的转折点提示买入
DRAWNUMBER(DC AND UD, K, 0, 0), ColorGray;
//// DRAWNUMBER(D1 AND REF(K,1)/REF(K,2)<=1 AND K/REF(K,1)>=1 AND K<50, K, 0, 0), ColorRed; ////
// 9周期内有过卖出信号, K值60以上的减速点提示卖出
DRAWNUMBER(D2 AND REF(K,1)/REF(K,2)>=1.01 AND K/REF(K,1)<1.01 AND K>60, K, 1, 0), ColorGreen;

80, ColorWhite, LINEDOT;
20, ColorWhite, LINEDOT;



// 根据均线提示买卖点.
// 对数化. 必须先均线, 再对数. 否则某些个股会出错(历史除权导致股价为负, 无法对数化)
N:=16;
LNN:=LN(MA(C,N));
LN2N:=LN(MA(C,N*2));
LN4N:=LN(MA(C,N*4));

// 用速度变化判断顶底
DN:=(LNN-REF(LNN,1)), ColorWhite;
D2N:=(LN2N-REF(LN2N,1)), ColorYellow;
D4N:=(LN4N-REF(LN4N,1)), ColorGreen;

// 交叉
CROSS11:=BARSLAST(CROSS(DN,D2N),1),NODRAW;
CROSS12:=BARSLAST(CROSS(D2N,DN),1),NODRAW;
CROSS21:=BARSLAST(CROSS(DN,D2N),2),NODRAW;
CROSS22:=BARSLAST(CROSS(D2N,DN),2),NODRAW;

// 均线序列及变化速度
LNUP:=IF(D2N/LN2N>-0.001 AND LN2N>LN4N, 1, 0);  // 长均线上升中, 适当放宽卖的条件.
LNDN:=IF(D2N/LN2N<0.001 AND D4N/LN4N<0.001 AND LNN<LN2N AND LN2N<LN4N, 1, 0);   // 长均线下降中
D1UP:=IF(DN/LNN>-0.001 AND DN<=D2N, 1, 0);  // 短均线上升减速中
D1DN:=IF(DN/LNN< 0.001 AND DN>=D2N, 1, 0);  // 短均线下降减速中

// 底部变盘: 加速度相等 且 均线下降趋势排列 且 长均线下降趋势减缓
BUY1:=IF(CROSS11=0 AND LNDN AND D2N>REF(D2N,CROSS21),1,0), NODRAW;
BUY2:=IF(CROSS12=0 AND LNDN AND D2N>REF(D2N,CROSS22),1,0), NODRAW;
// 顶部变盘: 加速度相等 且 均线上升趋势排列 且 长均线上升趋势减缓
SELL1:=IF(CROSS11=0 AND LNUP AND D2N<REF(D2N,CROSS21),1,0), NODRAW;
SELL2:=IF(CROSS12=0 AND LNUP AND D2N<REF(D2N,CROSS22),1,0), NODRAW;

// 底部写0, 顶部写1
DRAWNUMBER(BUY1 OR BUY2, 0, 0,0), ColorBrown;
//DRAWNUMBER(SELL1, 100, 1,0), ColorGray;

//ADL
IF StrFind(BlkName, '指数.', 1) Then Begin
    ADL:SUM(ADVANCE-DECLINE,0), NOAXIS, ColorBrown;
End
```


# 能量波
用了高通滤波, 来体现本级别K线的波动情况
重要的点: 前低, 前高, 零轴!
同时整合了MACD.

``` C
#NOTE "
能量波, 使用了高通滤波概念.
N=9,  大致相当于MACD的红绿柱(MACD).
D=24, 大致相当于MACD的白线(DIFF).
D=36, 大一级别的N=9.

使用的级别思路:D表示大级别波动情况, N表示小级别波动情况.
一般而言, 大级别一波需要小级别走一次三波或五波.
D在0轴之上, 没有背离, 那么N回踩零轴或前低是买点.
D在0轴之上, 股价背离, 那么N拉到前高或背离是卖点.
D在0轴之下的情况, 同理.
"
N:=9;
//D:=18;
A:=0.1111;

// 高通滤波. y[i] = α * y[i-1] + α * (x[i] - x[i-1])
//HPO:=(A/10)*(O-Ref(C,N));
//HPO:=A*(O/Ref(C,N)-1);        // 改用除法, 波动价格归一化
//HPO:=A*ref(HPO,1)+HPO;
//HPC:=(A/10)*(C-Ref(C,N));
//HPC:=A*(C/Ref(C,N)-1);
//HPC:=A*ref(HPC,1)+HPC;

CC:=REFX(MA(C,3),1);
HPO:=A*(O/Ref(CC,N)-1);
HPO:=A*ref(HPO,1)+HPO;
HPC:=A*(C/Ref(CC,N)-1);
HPC:=A*ref(HPC,1)+HPC;

// 能量波K线
PO:=100*HPO, NoDraw;
PC: 100*HPC, NoDraw, ColorWhite;

//PN:=EMA(PC,5), NoDraw;
//PartLine(PN>=REF(PN,1), PN), ColorRed;
//PartLine(PN<REF(PN,1), PN), ColorCyan;

// 长周期能量波
//HPD:=A*(C/Ref(C,D)-1);
//HPD:=A*ref(HPD,1)+HPD;

//PD: MA(100*HPD,5), NoDraw, ColorLightRed;
//PartLine(PD>=REF(PD,1), PD), ColorLightRed, LineThick2;
//PartLine(PD<REF(PD,1), PD), ColorLightGreen, LineThick2;

KLine(PO,PC,PC,PC,0), ColorYellow;
//0, ColorGray, LineDot;

// MACD
DIFF:=EMA(CLOSE,12)/EMA(CLOSE,26)-1;
DEA:=EMA(DIFF,9);
MACD:100*(DIFF-DEA), Stick, ColorBrown;
StickLine(ABS(MACD)>ABS(REF(MACD,1)) and ABS(MACD)>ABS(REFX(MACD,1)), 0, MACD, 1, 1), ColorGray;



// 低通滤波(即SMA). y[i] = α * x[i] + (1-α) * y[i-1]
//LPO:=(A/10)*O;
//LPO:(1-A/10)*ref(LPO,N)+LPO, NoDraw;
//LPC:=(A/10)*C;
//LPC:(1-A/10)*ref(LPC,N)+LPC, NoDraw;
//KLine(LPO,LPC,LPC,LPC,0);


//INPUT:
//  M(0,0,999);
//
//// 短中均线交叉
//IF M>0 Then Begin
//// 短期均线右移
//Q:=M/2;
//T0:=(M-Q)/2;
//M00:=ma(PC,Q)*(2-MOD(M,2));
//M01:=ma(PC,1+Q)*(MOD(M,2));
//M0:=(M00+M01)/2;          // 忽略误差可直接 M0:=ma(PC,M/2)
//M02:=Ref(M0,T0)*(4-MOD(M,4));
//M03:=Ref(M0,1+T0)*(MOD(M,4));
//M0_:(M02+M03)/4,ColorBrown;   // 忽略误差可直接 M0_:Ref(M0,T0), 无法显示右移的部分
//
//// 中期均线
//M1:ma(PC,M),ColorWhite;
//
//// 交叉点
//D0:=M0_-M1;
////    VERTLINE(D0*ref(D0,1)<=0), ColorGray, LineDot;  // 交叉最简单的写法
//W0:=D0+D0-ref(D0,1);                              // 用于预测过零轴
//BARCROSS:=BarsLast(D0*W0<=0 and abs(D0)<=abs(W0));    // 过零轴
//VERTLINE(BARCROSS==0 or (D0*ref(D0,1)<=0 and BARCROSS > 1)), ColorBrown, LineDot;
//End
```


# 强弱系统
核心思路: 横向对比, 找出最强/最弱的指数/板块/个股.
要点: 最强的最弱, 见顶. 最弱的走强, 见底.
额外的思路: 港股相比于A股会由提前量. 同一股票将H股对比A股, 如果之前一直弱势, 突然走强, 很可能就是逻辑反转走牛.

``` C
// 如果属于自定义的 '指数.' 板块, 显示市场强弱. 否则显示个股强弱.
#NOTE "
市场强弱, 用于对比大小票的强弱转换. 中证500和沪深300建议用IC/IF替代.
    白色, 真实走势, 中证500(SH000905), IC仓指(IC98), 中证指数(IC8888).
    绿色, 风格因子, 中证500(SH000905)/沪深300(SH000300), 代表小盘题材
    红色, 趋势因子, 沪深300(SH000300)/上证50(SH000016), 代表绩优权重

个股强弱, 用于判断个股的强弱
    洋红, 个股趋势, 个股/沪深300,  代表个股的整体趋势
    青色, 个股风格, 个股/创业板指, 代表个股的强弱情况
    黄色, 个股板块, 个股/板块,     代表个股的强弱情况
    上证50是最强的代表, 沪深300是市场最具代表性的指数.
    中证500是弱的代表, 创业板指是最弱但最具创新的代表.
    为便于观察, 选取沪深300和创业板指, 以及所在版块来评估个股趋势和强弱.

使用理念: 横向比较强弱(上上, 上下, 下上, 下下), 纵向比较强弱变化.
    顶底判断:
            见顶,强者转弱;
            见底,弱者转强.
    强者恒强:
            个股涨, 大盘跌, 个股强弱创新高. 等到大盘走强时, 个股将形成强者恒强!
    回归平衡:
            个股相对大盘先强后弱, 回归平衡后再转强!
            风格因子回归平衡判断, 底部看前低区域, 顶部看前高区域.
            趋势因子回归平衡判断, 底部看前高区域, 顶部看前低区域.
    波浪判断:
            1浪金融权重. 金融权重打头阵, 风格因子二次探底, .
            2浪回归平衡. 趋势因子见顶, 风格因子见底, 为同步上涨打下基础.
            3浪同步大涨. 绩优白马是强者恒强的涨, 小盘题材是由弱转强的涨.
            4浪普涨结束. 需要仔细甄别强弱, 选强去弱, 调仓换股, 降低仓位.
            5浪分化. 通常是题材轮动, 最后用权重拉指数冲顶.(见顶:强者转弱)
            A浪普跌. 对大级别A浪末期, 可仔细甄别强弱, 弱中选强, 为B浪反弹做准备.
            B浪赝品. 有限的参与资金决定了个股分化的命运. 通常是快速的题材轮动.
            C浪大跌. 最后砸权重, 制造恐慌中见底. (见底:弱者转强, 强者补跌)
"

// 显示参数精灵设置
#Template "归一化底价日期 Param#1"

INPUT:
  D1(1190104,0,1341231);

// 上证50
C50:="SH000016$Close";
O50:="SH000016$Open";
L50:="SH000016$Low";

// 沪深300
C300:="SH000300$Close";
O300:="SH000300$Open";
L300:="SH000300$Low";

// 中证500
C500:="SH000905$Close";
O500:="SH000905$Open";
H500:="SH000905$High";
L500:="SH000905$Low";

// 创业板指;
CCY:="SZ399006$Close";
OCY:="SZ399006$Open";
LCY:="SZ399006$Low";

// 上证指数
CSH:="SH000001$Close";
OSH:="SH000001$Open";
HSH:="SH000001$High";
LSH:="SH000001$Low";


IF StrFind(BlkName, '指数.', 1) Then Begin
// 属于系统指数的, 直接显示强弱系统.

// 真实走势
真实走势:C500, NoDraw, ColorGray;
KLine(O500,H500,L500,C500,1),ColorGray;

// 风格因子
OFG:=O500/O300;
CFG:=C500/C300;
风格因子:CFG, NoDraw, ColorLightGreen;
KLine(OFG,CFG,CFG,CFG,0),ColorLightGreen;

// 趋势因子
OQS:=O300/O50;
CQS:=C300/C50;
趋势因子:CQS, NoDraw, ColorLightRed;
KLine(OQS,CQS,CQS,CQS,0),ColorLightRed;

// 基于均线, 判断背离, 仅供参考!
N:=9;
MZS:=SMA(C500,N,1),NoAxis;
MFG:=EMA(CFG,N);
MQS:=EMA(CQS,N);

DZS:=IF(MZS<REF(MZS,1) and MZS<REF(MZS,1+N/2), 1, 0);
UZS:=IF(MZS>REF(MZS,1) and MZS>REF(MZS,1+N/2), 1, 0);
DFG:=IF(MFG<REF(MFG,1) and MFG<REF(MFG,N/2) and MFG<REF(MFG,N), 1, 0);
UFG:=IF(MFG>REF(MFG,1) and MFG>REF(MFG,N/2) and MFG>REF(MFG,N), 1, 0);
DQS:=IF(MQS<REF(MQS,1) and MQS<REF(MQS,N/2) and MQS<REF(MQS,N), 1, 0);
UQS:=IF(MQS>REF(MQS,1) and MQS>REF(MQS,N/2) and MQS>REF(MQS,N), 1, 0);

FGMIN:=Min(OFG, CFG);
QSMIN:=Min(OQS, CQS);
//// DrawNumber(DZS and UFG and UQS, FGMIN, 0, 0), ColorRed;   ////
//// DrawNumber(UZS and DFG and DQS, QSMIN, 1, 0), ColorGreen; ////


End Else Begin

// 上证指数
上证指数:CSH, NoDraw, ColorGray;
KLine(OSH,HSH,LSH,CSH,1),ColorGray;

// 个股
LGG:=RefData(StkLabel, D_Low, DataPeriod);

// 指定日期归一化, 建议选取历史低点.
// BarStatus必须放在前面, 可自适应新股. 使用<=可自动适应多周期.
B1:=BarsLast(BarStatus==1 or (Date<=D1 and Time<=093000),1);

// 个股/沪深300
R300:=L300[B1]/LGG[B1];
CV300:=R300*C/C300;
OV300:=R300*O/O300;
V沪深:CV300, NoDraw, ColorMagenta;
//KLine(OV300,CV300,CV300,CV300,0),ColorMagenta;

// 个股/创业板指
RCY:=LCY[B1]/LGG[B1];
CVCY:=RCY*C/CCY;
OVCY:=RCY*O/OCY;
v创业:CVCY, NoDraw, ColorCyan;
KLine(OVCY,CVCY,CVCY,CVCY,0),ColorCyan;

// 个股板块, 个股/行业板块
If (IndustryName != '') Then Begin
    // 显示个股基本信息
    PE:=DynaInfo(Q_PE),NoDraw;
    VL:=DynaInfo(Q_MARKETVAL)/100000000,NoDraw;
    DRAWTEXTEX(1, 1, 2, 0, STKNAME+' '+STKLABEL+'   市盈:'+NumToStr(PE,2)+' 市值:'+NumToStr(VL,2)+'亿'+'   '+IndustryName),
        IIF(PE>0 and PE<100 and VL>100,ColorCyan,ColorYellow);

    // 板块指数
    CodeBK:=StkLabelN(IndustryName);
    CBK:=RefData(CodeBK, D_Close, DataPeriod);
    OBK:=RefData(CodeBK, D_Open, DataPeriod);
    LBK:=RefData(CodeBK, D_Low, DataPeriod);

    //板块/上证指数
    RBKSH:=LSH[B1]/LBK[B1];
    CBKSH:=RBKSH*CBK/CSH;
    OBKSH:=RBKSH*OBK/OSH;
    KLine(OBKSH,CBKSH,CBKSH,CBKSH,0),ColorBrown;

    //个股/板块
    RBK:=LBK[B1]/LGG[B1];
    CVBK:=RBK*C/CBK;
    OVBK:=RBK*O/OBK;
    v板块:CVBK, NoDraw, ColorYellow;
    KLine(OVBK,CVBK,CVBK,CVBK,0),ColorYellow;

    //板块强弱
    板块强弱:CBKSH, NoDraw, ColorBrown;
End Else Begin
    CVBK:=CV300;
    OVBK:=OV300;
End

// V沪深显示在最顶层
KLine(OV300,CV300,CV300,CV300,0),ColorMagenta;

// 平台突破
M:=4;
RR:=1.005; // 设置有效突破阀值
HH1:=HHV(REF(CV300,1),M);
HH2:=HHV(REF(CVCY,1),M);
HH3:=HHV(REF(CVBK,1),M);
TP1:=CV300/HH1>RR;
TP2:=CVCY/HH2>RR;
TP3:=CVBK/HH3>RR;
TP:=TP1 and TP2 and TP3,NoDraw;
平台突破:=TP and BARSLASTCOUNT(REF(TP,1)==0)>M,NoDraw;
VMIN:=MinList(OV300, OVCY, OVBK, CV300, CVCY, CVBK);
DrawNumber(TP, VMIN, 0, 0), ColorBrown;
DrawNumber(平台突破, VMIN, 0, 0), ColorRed;

End
```

# 板块轮动
强弱系统, 用于板块选择判断.

``` C
#NOTE "
板块强弱, 选用最具代表性的板块, 和上证指数做比较:
    淡红, 券商.     券商. 金融代表. 牛熊指示器.
    白色, 中证消费. 家电食品. 高收益, 绩优白马.
    黄色, 中证医药. 医疗医药. 高收益, 绩优白马.
    淡绿, 中证信息. 信息科技. 高波动, 未来成长.
    青色, 创业板指. 小票创新. 高波动, 未来成长.

板块特点:
    上证50券商是一组,  代表核心资产, 特点是低波动, 即跌的少涨的慢;
    消费和医药是一组,   代表绩优白马, 特点是高收益, 即跌的少涨的多;
    创业和信息是一组,   代表未来成长, 特点是高波动, 即跌的多涨的多;
    其它行业只看龙头,   代表传统行业, 如地产, 化工, 有色, 基建等等.

使用理念: 可用于辅助判断大盘顶底和板块轮动.
    顶底判断:
            见顶,强者转弱;
            见底,弱者转强.
    强者恒强:
            板块强弱创新高, 然后回踩不破前高, 将形成强者恒强!
            如果板块强弱创新低无法立刻收回, 则该板块将长期走弱!
    回归平衡:
            板块相对大盘先强后弱, 回归平衡后再转强!
    波浪判断:
            1浪金融权重. 金融权重打头阵, 创业信息二次探底, .
            2浪回归平衡. 金融权重见顶, 创业信息见底, 为同步上涨打下基础.
            3浪同步大涨. 消费医药是强者恒强的涨, 创业信息是由弱转强的涨.
            4浪普涨结束. 需要仔细甄别强弱, 选强去弱, 调仓换股, 降低仓位.
            5浪分化. 通常是题材轮动, 最后用权重拉指数冲顶.(见顶:强者转弱)
            A浪普跌. 对大级别A浪末期, 可仔细甄别强弱, 弱中选强, 为B浪反弹做准备.
            B浪赝品. 有限的参与资金决定了个股分化的命运. 通常是快速的题材轮动.
            C浪大跌. 最后砸权重, 制造恐慌中见底. (见底:弱者转强, 强者补跌)
"

// 显示参数精灵设置
#Template "是否显示以及偏移量:
券商  Param#1,淡红
消费  Param#2,白色
医药  Param#3,黄色
信息  Param#4,淡绿
创业  Param#5,青色
归一化底价日期 Param#6
"

input:
    证券K(0,-1,50),
    消费K(0,-1,50),
    医药K(0,-1,50),
    信息K(0,-1,50),
    创业K(0,-1,50),
    D1(1190104,0,1341231);

CSH:="SH000001$Close";  // 上证指数
OSH:="SH000001$Open";
HSH:="SH000001$High";
LSH:="SH000001$Low";
//CSH:="SH000300$Close";    // 沪深300
//OSH:="SH000300$Open";
//HSH:="SH000300$High";
//LSH:="SH000300$Low";

LCY:="SZ399006$Low";    // 创业板
LXF:="SH000932$Low";    // 消费
LYY:="SH000933$Low";    // 医药
LZQ:="J141$Low";        // 证券
LXX:="SH000935$Low";    // 信息

// 指定日期归一化, 建议选取历史低点.
// BarStatus必须放在前面, 可自适应新股. 使用<=可自动适应多周期.
B1:=BarsLast(BarStatus==1 or (Date<=D1 and Time<=093000),1);
MINSH:=LSH[B1];
MINCY:=LCY[B1];
MINXF:=LXF[B1];
MINYY:=LYY[B1];
MINZQ:=LZQ[B1];
MINXX:=LXX[B1];

// 归一化比率
RSH:=MINSH/MINSH;
RCY:=MINSH/MINCY;
RXF:=MINSH/MINXF;
RYY:=MINSH/MINYY;
RZQ:=MINSH/MINZQ;
RXX:=MINSH/MINXX;

KLine(OSH,HSH,LSH,CSH,1),ColorGray;

// 中证医药
CYY:=RYY*"SH000933$Close"/CSH + 医药K/10;
OYY:=RYY*"SH000933$Open" /OSH + 医药K/10;
医药:CYY, NODRAW, ColorYellow;
IF (医药K>=0) Then KLine(OYY,CYY,CYY,CYY,0),ColorYellow;

// 中证消费
CXF:=RXF*"SH000932$Close"/CSH + 消费K/10;
OXF:=RXF*"SH000932$Open" /OSH + 消费K/10;
消费:CXF, NODRAW, ColorWhite;
IF (消费K>=0) Then KLine(OXF,CXF,CXF,CXF,0),ColorWhite;

// 证券
CZQ:=RZQ*"J141$Close"/CSH + 证券K/10;
OZQ:=RZQ*"J141$Open" /OSH + 证券K/10;
证券:CZQ, NODRAW, ColorLightRed;
IF (证券K>=0) Then KLine(OZQ,CZQ,CZQ,CZQ,0),ColorLightRed;

// 中证信息
CXX:=RXX*"SH000935$Close"/CSH + 信息K/10;
OXX:=RXX*"SH000935$Open" /OSH + 信息K/10;
信息:CXX, NODRAW, ColorLightGreen;
IF (信息K>=0) Then KLine(OXX,CXX,CXX,CXX,0),ColorLightGreen;

// 创业板
CCY:=RCY*"SZ399006$Close"/CSH + 创业K/10;
OCY:=RCY*"SZ399006$Open" /OSH + 创业K/10;
创业:CCY, NODRAW, ColorCyan;
IF (创业K>=0) Then KLine(OCY,CCY,CCY,CCY,0),ColorCyan;
```

# 期权加油线
机构代表主力和大资金. 因而可以通过期权的认沽或认购持仓变动来预判主力对后市的看法.
首先在期权市场上, 散户往往是直线思维, 看涨买认购, 看跌了买认沽; 而机构是绝对主力, 往往提前布局了仓位, 从而反向操作, 即看涨卖认沽, 看跌卖认购.
这样, 就有这样一个推论: 期权市场, 买方的主要是散户, 卖方的主要是机构.
因而, 当认沽期权持仓量变大时, 说明散户看跌, 但主力资金不怕跌, 敢于把大量认沽的筹码卖给直线思维的散户, 主力资金对后市是看涨的!
反之, 当认购期权持仓量变大时, 说明散户看涨, 但主力资金不看涨, 才肯把大量认购的筹码丢给直线思维的散户, 主力资金对后市是看跌的!
综上, 观察`认沽期权持仓量/认购期权持仓量`的变化, 结合K线图相对位置, 可以预判底部和顶部, 特别是顶部区域.
由于这条线往往优先于K线价格, 因而取名为期权加油线. 期权加油线也有趋势线, 前低的支撑作用, 前高的阻力作用, 可作为参考, 但最有用的还是背离.

![期权加油线](https://draapho.github.io/images/2102/option.png)


# 股债收益率模型
股债收益率模型（EYBY）是一个经典的股市估值模型，其基本思想是将“股票收益率”（EY）与“债券收益率”（BY）进行对比，计算出(EY-BY)，当该数值为正数，股票收益率更高，当该数值为负数，债券收益率更高.
其中EY取10年国债的到期收益率, BY取全A指数中位市盈率(TTM)的倒数, 有些网站也成为等权PE.

此模型本质上, 是一个跨市场的强弱指标.
另建议用BY-EY, 和股价走势图叠加显示, 视觉上会更直观.


# 股价增长模式
股市波动有两种主要的博弈模式, 增量博弈和存量博弈. 其中增量博弈有明显的生命形式的自增长特征.
波浪理论里面提到了黄金比例, 但没有将黄金比例应用到高点到高点的预测. 下图例示范:

![等比增长](https://draapho.github.io/images/2102/ratio.png)