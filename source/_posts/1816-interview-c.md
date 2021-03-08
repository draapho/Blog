---
title: 面试之嵌入式C语言
date: 2018-05-07
categories: interview
tags: [interview]
description: 面试题集.
---

# 总览
- [逻辑|这样表达，事半功倍](https://draapho.github.io/2017/05/04/1714-expression/)
- [面试之常规问题](https://draapho.github.io/2018/01/10/1805-interview-general/)
- [面试之嵌入式C语言](https://draapho.github.io/2018/05/07/1816-interview-c/)
- [C语言知识巩固](https://draapho.github.io/2017/05/17/1715-c/)
- [面试之嵌入式Linux](https://draapho.github.io/2018/05/08/1817-interview-linux/)

我个人面试经验极少, 但这种能力都是需要培养的.
此系列总结一下面试中常见的技能要点. 侧重于技术面的准备.



# Q1: #define
Using the #define statement, how would you declare a manifest constant that returns the number of seconds in a year? Disregard leap years in your answer.

A1:
`#define SECONDS_PER_YEAR (60UL * 60UL * 24UL * 365UL)`

I'm looking for several things here:
- Basic knowledge of the #define syntax (i.e. no semi-colon at the end, the need to parenthesize etc.).
- A good choice of name, with capitalization and underscores.
- An understanding that the pre-processor will evaluate constant expressions for you. Thus, it is clearer, and penalty free to spell out how you are calculating the number of seconds in a year, rather than actually doing the calculation yourself.
- A realization that the expression will oveflow an integer argument on a 16 bit machine hence the need for the L, telling the compiler to treat the expression as a Long.
- As a bonus, if you modified the expression with a UL (indicating unsigned long), then you are off to a great start because you are showing that you are mindful of the perils of signed and unsigned types and remember, first impressions count!

# Q2: #define
Write the "standard" MIN macro. That is, a macro that takes two arguments and returns the smaller of the two arguments.

A2:
`#define MIN(A,B) ( (A) <= (B) ? (A) : (B) )`

The purpose of this question is to test the following:
- Basic knowledge of the #define directive as used in macros. This is important, because until the inline operator becomes part of standard C, macros are the only portable way of generating inline code. Inline code is often necessary in embedded systems in order to achieve the required performance level.
- Knowledge of the ternary conditional operator. This exists in C because it allows the compiler to potentially produce more optimal code than an ifthen-else sequence. Given that performance is normally an issue in embedded systems, knowledge and use of this construct is important.
- Understanding of the need to very carefully parenthesize arguments to macros.
- I also use this question to start a discussion on the side effects of macros, e.g. what happens when you write code such as : `least = MIN(*p++, b);`

# Q3: #error
What is the purpose of the preprocessor directive #error?

A3:
Either you know the answer to this, or you don't. If you don't, then see reference.
This question is very useful for dierentiating between normal folks and the nerds. It's only the nerds that actually read the appendices of C textbooks that find out about such things. Of course, if you aren't looking for a nerd, the candidate better hope she doesn't know the answer.

# Q4: Infinite loops
Infinite loops often arise in embedded systems. How does one code an infinite loop in C?

A4:
There are several solutions to this question. My preferred solution is:
``` c
while ( 1 ) {
    ...
}
```

Another common construct is:
``` c
for ( ; ; ) {
    ...
}
```
Personally, I dislike this construct because the syntax doesn't exactly spell out what is going on. Thus, if a candidate gives this as a solution, I'll use it as an opportunity to explore their rationale for doing so. If their answer is basically "I was taught to do it this way and I have never thought about it since" then it tells me something (bad) about them. Conversely, if they state that it's the K&R preferred method and the only way to get an infinite loop passed Lint, then they score bonus points.

A third solution is to use a goto:
``` c
Loop :
. . .
goto Loop ;
```
Candidates that propose this are either assembly language programmers (which is probably good), or else they are closet BASIC / FORTRAN programmers looking to get into a new field.

# Q5: Data declarations
Using the variable a, write down definitions for the following:
a) An integer
b) A pointer to an integer
c) A pointer to a pointer to an integer
d) An array of ten integers
e) An array of ten pointers to integers
f) A pointer to an array of ten integers
g) A pointer to a function that takes an integer as an argument and returns an integer
h) An array of ten pointers to functions that take an integer argument and return an integer

A5:
The answers are:
``` c
int a;          // An integer
int *a;         // A pointer to an integer
int **a;        // A pointer to a pointer to an integer
int a[10];      // An array of ten integers
int *a[10];     // An array of ten pointers to integers
int (*a)[10];   // A pointer to an array of ten integers
int (*a)(int);  // A pointer to a function that takes an integer as an argument and returns an integer
int (*a[10])(int); // An array of ten pointers to functions that take an integer argument and return an integer
```
People often claim that a couple of these are the sorts of thing that one looks up in textbooks and I agree. While writing this article, I consulted textbooks to ensure the syntax was correct. However, I expect to be asked this question (or something close to it) when in an interview situation. Consequently, I make sure I know the answers at least for the few hours of the interview. Candidates that don't know the answers (or at least most of them) are simply unprepared for the interview. If they can't be prepared for the interview, what will they be prepared for?

# Q6: Static
What are the uses of the keyword static?

A6:
This simple question is rarely answered completely. Static has three distinct uses in C:
- A variable declared static within the body of a function maintains its value between function invocations.
- A variable declared static within a module1, (but outside the body of a function) is accessible by all functions within that module. It is not accessible by functions within any other module. That is, it is a localized global.
- Functions declared static within a module may only be called by otherfunctions within that module. That is, the scope of the function is localized to the module within which it is declared.

Most candidates get the first part correct. A reasonable number get the second part correct, while a pitiful number understand the third answer. This is a serious weakness in a candidate, since they obviously do not understand the importance and benefits of localizing the scope of both data and code.

# Q7: Const
What does the keyword const mean?

A7:
As soon as the interviewee says "const means constant", I know I'm dealing with an amateur. Dan Saks has exhaustively covered const in the last year, such that every reader of ESP should be extremely familiar with what const can and cannot do for you. If you haven't been reading that column, suffice it to say that const means "read-only". Although this answer doesn't really do the subject justice, I'd accept it as a correct answer. (If you want the detailed answer, then read Saks' columns carefully!).

If the candidate gets the answer correct, then I'll ask him these supplemental questions:

# Q7.1: Const
What do the following incomplete declarations mean?
```
const int a ;
int const a ;
const int *a ;
int * const a ;
int const *a const ;
```

A7.1:
The first two mean the same thing, namely a is a const (read-only) integer.
The third means a is a pointer to a const integer (i.e., the integer isn't modifiable, but the pointer is).
The fourth declares a to be a const pointer to an integer (i.e., the integer pointed to by a is modifiable, but the pointer is not).
The final declaration declares a to be a const pointer to a const integer (i.e., neither the integer pointed to by a, nor the pointer itself may be modified).

If the candidate correctly answers these questions, I'll be impressed. Incidentally, one might wonder why I put so much emphasis on const, since it is very easy to write a correctly functioning program without ever using it. There are several reasons:
- The use of const conveys some very useful information to someone reading your code. In effect, declaring a parameter const tells the user about its intended usage. If you spend a lot of time cleaning up the mess left by other people, then you'll quickly learn to appreciate this extra piece of information. (Of course, programmers that use const, rarely leave a mess for others to clean up...)
- const has the potential for generating tighter code by giving the optimizer some additional information.
- Code that uses const liberally is inherently protected by the compiler against inadvertent coding constructs that result in parameters being changed that should not be. In short, they tend to have fewer bugs.

# Q8: Volatile
What does the keyword volatile mean? Give three different examples of its use.

A8:
A volatile variable is one that can change unexpectedly. Consequently, the compiler can make no assumptions about the value of the variable. In particular, the optimizer must be careful to reload the variable every time it is used instead of holding a copy in a register. Examples of volatile variables are:
- Hardware registers in peripherals (e.g., status registers)
- Non-stack variables referenced within an interrupt service routine.
- Variables shared by multiple tasks in a multi-threaded application.

If a candidate does not know the answer to this question, they aren't hired. I consider this the most fundamental question that distinguishes between a 'C programmer' and an 'embedded systems programmer'. Embedded folks deal with hardware, interrupts, RTOSes, and the like. All of these require volatile variables. Failure to understand the concept of volatile will lead to disaster. On the (dubious) assumption that the interviewee gets this question correct, I like to probe a little deeper, to see if they really understand the full significance of volatile. In particular, I'll ask them the following:

# Q8.1: Volatile
- Can a parameter be both const and volatile? Explain your answer.
- Can a pointer be volatile? Explain your answer.
- What is wrong with the following function?:

``` c
int square (volatile int *ptr) {
    return *ptr * *ptr;
}
```

A8.1:
The answers are as follows:
- Yes. An example is a read only status register. It is volatile because it can change unexpectedly. It is const because the program should not attempt to modify it.
- Yes. Although this is not very common. An example is when an interrupt service routine modifses a pointer to a buffer.
- This one is wicked. The intent of the code is to return the square of the value pointed to by `*ptr`. However, since `*ptr`points to a volatile parameter, the compiler will generate code that looks something like this:

``` c
int square ( volatile int *ptr ) {
    int a, b;
    a = *ptr ;
    b = *ptr ;
    return a * b ;
}
```

Since it is possible for the value of `*ptr` to change unexpectedly, it is possible for a and b to be different. Consequently, this code could return a number that is not a square! The correct way to code this is:

``` c
long square ( volatile int *ptr ) {
    int a;
    a = *ptr;
    return a * a;
}
```

# Q9: Bit Manipulation
Embedded systems always require the user to manipulate bits in registers or variables. Given an integer variable a, write two code fragments. The first should set bit 3 of a. The second should clear bit 3 of a. In both cases, the remaining
bits should be unmodified.

A9:
These are the three basic responses to this question:
- No idea. The interviewee cannot have done any embedded systems work.
- Use bit fields. Bit fields are right up there with trigraphs as the most braindead portion of C. Bit fields are inherently non-portable across compilers, and as such guarantee that your code is not reusable. I recently had the misfortune to look at a driver written by Infineon for one of their more complex communications chip. It used bit fields, and was completely useless because my compiler implemented the bit fields the other way around. The moral never let a non-embedded person anywhere near a real piece of hardware!
- Use #defines and bit masks. This is a highly portable method, and is the one that should be used. My optimal solution to this problem would be:

``` c
#define BIT3 (0x1<<3)

static int a;
void set_bit3(void) {
    a |= BIT3 ;
}

void clear_bit3(void) {
    a &= ~BIT3;
}
```

Some people prefer to define a mask, together with manifest constants for the set and clear values. This is also acceptable. The important elements that I'm looking for are the use of manifest constants, together with the `|=` and `&=` constructs.

# Q10: Accessing fixed memory locations
Embedded systems are often characterized by requiring the programmer to access a specific memory location. On a certain project it is required to set an integer variable at the absolute address 0x67a9 to the value 0xaa55. The compiler is a pure ANSI compiler. Write code to accomplish this task.

A10:
This problem tests whether you know that it is legal to typecast an integer to a pointer in order to access an absolute location. The exact syntax varies depending upon one's style. However, I would typically be looking
``` c
// for something like this:
int *ptr;
ptr = (int *)0x67a9 ;
*ptr = 0xaa55 ;

// A more obfuscated approach is:
*(int * const)(0x67a9) = 0xaa55;
```
Even if your taste runs more to the second solution, I suggest the first solution when you are in an interview situation.

# Q11: Interrupts
Interrupts are an important part of embedded systems. Consequently, many compiler vendors offer an extension to standard C to support interrupts. Typically, this new key word is `__interrupt`. The following code uses `__interrupt` to define an interrupt service routine. Comment on the code.

``` c
__interrupt double compute_area(double radius) {
    double ar ea = PI * radius * radius;
    print ("\nArea = %f", area ) ;
    return area ;
}
```

A11:
This function has so much wrong with it, it's almost tough to know where to start.
- Interrupt service routines cannot return a value. If you don't understand this, then you aren't hired.
- ISR's cannot be passed parameters. See first item for your employment prospects if you missed this.
- On many processors/compilers, floating point operations are not necessarily re-entrant. In some cases one needs to stack additional registers, in other cases, one simply cannot do floating point in an ISR. Furthermore, given that a general rule of thumb is that ISRs should be short and sweet, one wonders about the wisdom of doing floating point math here.
- In a similar vein to third point, printf() often has problems with reentrancy and performance.
If you missed last two points then I wouldn't be too hard on you. Needless to say, if you got these two points, then your employment prospects are looking better and better.

# Q12: Code Examples
What does the following code output and why?
```
void foo (void) {
    unsigned int a = 6;
    int b = -20;
    (a+b > 6) ? puts (">6") : puts("<=6");
}
```

A12:
This question tests whether you understand the integer promotion rules in C an area that I find is very poorly understood by many developers. Anyway, the answer is that this outputs `>6`. The reason for this is that expressions involving signed and unsigned types have all operands promoted to unsigned types. Thus `-20` becomes a very large positive integer and the expression evaluates to greater than 6. This is a very important point in embedded systems where unsigned data types should be used frequently. If you get this one wrong, then you are perilously close to not being hired.


# Q13: Code Examples
Comment on the following code fragment?
```
unsigned int zero = 0;
unsigned int compzero = 0xFFFF; /* 1's complement of zero */
```

A13:
On machines where an int is not 16 bits, this will be incorrect. It should be coded:
`unsigned int compzero = ~0;`

This question really gets to whether the candidate understands the importance of word length on a computer. In my experience, good embedded programmers are critically aware of the underlying hardware and its limitations, whereas computer programmers tend to dismiss the hardware as a necessary annoyance.

By this stage, candidates are either completely demoralized or they are on a roll and having a good time. If it is obvious that the candidate isn't very good, then the test is terminated at this point. However, if the candidate is doing well, then I throw in these supplemental questions. These questions are hard, and I expect that only the very best candidates will do well on them. In posing these questions, I'm looking more at the way the candidate tackles the problems, rather than the answers. Anyway, have fun...

# Q14: Dynamic memory allocation
Although not as common as in non-embedded computers, embedded systems still do dynamically allocate memory from the heap. What are the problems with dynamic memory allocation in embedded systems?

A14:
Here, I expect the user to mention memory fragmentation, problems with garbage collection, variable execution time, etc. This topic has been covered extensively in ESP, mainly by Plauger. His explanations are far more insightful than anything I could offer here, so go and read those back issues! Having lulled the candidate into a sense of false security, I then offer up this tidbit: What does the following code fragment output and why?

``` c
char *ptr;
if (( ptr=(char *)malloc(0)) == NULL) {
    puts("Got a null pointer");
} else {
    puts("Got a valid pointer");
}
```

This is a fun question. I stumbled across this only recently, when a colleague of mine inadvertently passed a value of 0 to malloc, and got back a valid pointer! After doing some digging, I discovered that the result of malloc(0) is implementation defined, so that the correct answer is "it depends". I use this to start a discussion on what the interviewee thinks is the correct thing for malloc to do. Getting the right answer here is nowhere near as important as the way you approach the problem and the rationale for your decision.

# Q15: Typedef
Typedef is frequently used in C to declare synonyms for pre-existing data types.
It is also possible to use the preprocessor to do something similar. For instance,
consider the following code fragment:

``` c
#define dPS struct s *
typedef struct s * tPS;
```
The intent in both cases is to define dPS and tPS to be pointers to structure s. Which method (if any) is preferred and why?

A15:
This is a very subtle question, and anyone that gets it right (for the right reason) is to be congratulated or condemned ("get a life" springs to mind). The answer is the typedef is preferred. Consider the declarations:

``` c
dPS p1, p2;
tPS p3, p4;
```

The first expands to `struct s *p1 , p2` which defines p1 to be a pointer to the structure and p2 to be an actual structure, which is probably not what you wanted. The second example correctly defines p3 and p4 to be pointers.

# Q16: Obfuscated syntax
C allows some appalling constructs. Is this construct legal, and if so what does this code do?

``` c
int a=5, b=7, c;
c = a+++b ;
```

A16:
This question is intended to be a lighthearted end to the quiz, as, believe it or not, this is perfectly legal syntax. The question is how does the compiler treat it? Those poor compiler writers actually debated this issue, and came up with the "maximum munch" rule, which stipulates that the compiler should bite off as big a (legal) chunk as it can. Hence, this code is treated as:
    `c = a++ + b;`

Thus, after this code is executed, a = 6, b = 7 and c = 12; If you knew the answer, or guessed correctly then well done. If you didn't know the answer then I would not consider this to be a problem. I find the biggest benefit of this question is that it is very good for stimulating questions on coding styles, the value of code reviews and the benefits of using lint.

Well folks, there you have it. That was my version of the C test. I hope you had as much fun doing it as I had writing it. If you think the test is a good test, then by all means use it in your recruitment. Who knows, I may get lucky in a year or two and end up being on the receiving end of my own work.

# Q: What is NULL pointer and what is its use?
The NULL is a macro de¡ned in C. Null pointer actually means a pointer that does not point to any valid location. We de¡ne a pointer to be null when we want to make sure that the pointer does not point to any valid location and not to use that pointer to change anything. If we don't use null pointer, then we can't verify whether this pointer points to any valid location or not.

# Q: What is void pointer and what is its use?
The void pointer means that it points to a variable that can be of any type. Other pointers points to a speci¡c type of variable while void pointer is a somewhat generic pointer and can be pointed to any data type, be it standard data type(int, char etc) or user de¡ne data type (structure, union etc.). We can pass any kind of pointer and reference it as a void pointer. But to dereference it, we have to type the void pointer to correct data type.

# Q: What is ISR?
An ISR(Interrupt Service Routine) is an interrupt handler, a callback subroutine which is called when a interrupt is encountered Interrupt latency is the time required for an ISR responds to an interrupt.

# Q: What is interrupt latency? How to reduce interrupt latency?
Interrupt latency is the time required for an ISR responds to an interrupt.
Interrupt latency can be minimized by writing short ISR routine and by not delaying interrupts for more time.

20) What is Top half & bottom half of a kernel?

Sometimes to handle an interrupt, a substantial amount of work has to be done. But it conflicts with the speed need for an interrupt handler. To handle this situation, Linux splits the handler into two parts – Top half and Bottom half. The top half is the routine that actually responds to the interrupt. The bottom half on the other hand is a routine that is scheduled by the upper half to be executed later at a safer time.

All interrupts are enabled during execution of the bottom half. The top half saves the device data into the specific buffer, schedules bottom half and exits. The bottom half does the rest. This way the top half can service a new interrupt while the bottom half is working on the previous.

# Q: Can static variables be declared in a header file?
A static variable cannot be declared without defining it. A static variable can be defined in the header file. But doing so, the result will be having a private copy of that variable in each source file which includes the header file. So it will be wise not to declare a static variable in header file, unless you are dealing with a different scenario.

# Q: Is Count Down_to_Zero Loop better than Count_Up_Loops?
Count down to zero loops are better. Reason behind this is that at loop termination, comparison to zero can be optimized by the compiler. Most processors have instruction for comparing to zero. So they don't need to load the loop variable and the maximum value, subtract them and then compare to zero. That is why count down to zero loop is better.

# Q: What are inline functions? Advantages and disadvantages of using macro and inline functions?
The ARM compilers support inline functions with the keyword __inline. These functions have a small definition and the function body is substituted in each call to the inline function. The argument passing and stack maintenance is skipped and it results in faster code execution, but it increases code size, particularly if the inline function is large or one inline function is used often.

The advantage of the macro and inline function is that the overhead for argument passing and stuff is reduced as the function are in-lined. The advantage of macro function is that we can write type insensitive functions. It is also the disadvantage of macro function as macro functions can't do validation check. The macro and inline function also increases the size of the executable.

# Q: What happens when recursive functions are declared inline?
Inlining an recursive function reduces the overhead of saving context on stack. But, inline is merely a suggestion to the compiler and it does not guarantee that a function will be inlined. Obviously, the compiler won't be able to inline a recursive function infinitely. It may not inline it at all or it may inline it, just a few levels deep.


# Q: Can structures be passed to the functions by value?
Passing structure by its value to a function is possible, but not a good programming practice. First of all, if we pass the structure by value and the function changes some of those values, then the value change is not reflected in caller function. Also, if the structure is big, then passing the structure by value means copying the whole structure to the function argument stack which can slow the program by a significant amount.

# Q: Why cannot arrays be passed by values to functions?
In C, the array name itself represents the address of the first element. So, even if we pass the array name as argument, it will be passed as reference and not its address.


# Q: What is the concatenation operator?

The Concatenation operator (##) in macro is used to concatenate two arguments. Literally, we can say that the arguments are concatenated, but actually their value are not concatenated. Think it this way, if we pass A and B to a macro which uses ## to concatenate those two, then the result will be AB. Consider the example to clear the confusion-
``` c
#define SOME_MACRO(a, b) a##b
main()
{
  int var = 15;
  printf(“%d”, SOME_MACRO(v, ar));
}
```
Output of the above program will be 15.

# Q: `#define cat(x,y) x##y` concatenates x to y. But `cat(cat(1,2),3)` does not expand but gives preprocessor warning. Why?
The cat(x, y) expands to x##y. It just pastes x and y. But in case of cat(cat(1,2),3), it expands to cat(1,2)##3 instead of 1##2##3. That is why it is giving preprocessor warning.

# Q: How to decide whether given processor is using little endian format or big endian format ?
``` c
#include <stdio.h>

int check_for_endianness()
{
  unsigned int x = 1;
  char *c = (char*) &x;
  return (int)*c;
}
```

# Q: What is forward reference w.r.t. pointers in c?
Forward Referencing with respect to pointers is used when a pointer is declared and compiler reserves the memory for the pointer, but the variable or data type is not defined to which the pointer points to. For example
``` c
struct A *p;
struct A
{
 // members
};
```

# Q: How can you define a structure with bit field members?
Not command use bit field in embedded system! because bit fields are inherently non-portable across compilers, and as such guarantee that your code is not reusable.
Bit field members can be declared as shown below
```
struct A
{
 char c1 : 3;
 char c2 : 4;
 char c3 : 1;
};
```
Here c1, c2 and c3 are members of a structure with width 3, 4, and 1 bit respectively. The ':' indicates that they are bit fields and the following numbers indicates the width in bits.

# Q: How do you write a function which takes 2 arguments - a byte and a field in the byte and returns the value of the field in that byte?
The function will look like this -
``` c
int GetFieldValue(int byte, int field ) {
    return (byte >> field) & 0x01;
}
```
The byte is right shifted exactly n times where n is same as the field value. That way, our intended value ends up in the 0th bit position. "Bitwise And" with 1 can get the intended value. The function then returns the intended value.

# Q: What is job of preprocessor, compiler, assembler and linker ?
The preprocessor commands are processed and expanded by the preprocessor before actual compilation. After preprocessing, the compiler takes the output of the preprocessor and the source code, and generates assembly code. Once compiler completes its work, the assembler takes the assembly code and produces an assembly listing with offsets and generate object files.

The linker combines object files or libraries and produces a single executable file. It also resolves references to external symbols, assigns final addresses to functions and variables, and revises code and data to reflect new addresses.

# Q: Significance of watchdog timer in Embedded Systems.

The watchdog timer is a timing device with a predefined time interval. During that interval, some event may occur or else the device generates a time out signal. It is used to reset to the original state whenever some inappropriate events take place which can result in system malfunction. It is usually operated by counter devices.

# Q: Why ++n executes faster than n+1?

The expression ++n requires a single machine instruction such as INR to carry out the increment operation. In case of n+1, apart from INR, other instructions are required to load the value of n. That is why ++n is faster.

# Q: What is wild pointer?

A pointer that is not initialized to any valid address or NULL is considered as wild pointer. Consider the following code fragment -

``` c
int *p;
*p = 20;
```
Here p is not initialized to any valid address and still we are trying to access the address. The p will get any garbage location and the next statement will corrupt that memory location.


# Q: What is dangling pointer?
迷途指针, 指向的buffer已经被释放了, 但是指向它的指针依旧
If the memory of a pointer is de-allocated or freed and the pointer is not assigned to NULL, then it may still contain that address and accessing the pointer means that we are trying to access that location and it will give an error. This type of pointer is called dangling pointer.

# Q: Write down the equivalent pointer expression for referring the same element `a[i][j][k][l]` ?
We know that `a[i]` can be written as `*(a+i)`. Same way, the array elements can be written like pointer expression as follows -
``` c
a[i][j] == *(*(a+i)+j)
a[i][j][k] == *(*(*(a+i)+j)+k)
a[i][j][k][l] == *(*(*(*(a+i)+j)+k)+l)
```

# Q: When should we use register modifier?
The register modifier is used when a variable is expected to be heavily used and keeping it in the CPU’s registers will make the access faster.

# Q: Explain what are the different storage classes in C
- `auto` for local variables in RAM
- `register` for local variables in register
- `static` for local variable, keeping the value during the life-time of the program
- `static` for global variable only shared on its own file scope
- `extern` to give a reference of a global variable that is visible to ALL the program files


----------

***转载自 [The 0x10 Best Questions for Would-be Embedded Programmers](http://www.emb-linux.narod.ru/interview/0x10_questions.pdf)***
***转载自 [Embedded C Interview Questions and Answers](http://a4academics.com/interview-questions/57-c-plus-plus/722-embedded-c-interview-questions?showall=&limitstart=)***
