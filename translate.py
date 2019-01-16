from collections import deque
import analyze as az
import operator
G=az.get_graph("sample2.cpp")
queue = deque()
queue.append(0)
visited=[]
vis={}
cnt=0
while len(queue)!=0:
    pos = queue[0]
    queue.popleft()
    if pos in visited:
        continue
    if pos==0:
        cnt=0
    else:
        cnt=cnt+1
        vis[pos]=cnt
    visited.append(pos)
    if G[pos].yes!=-1:
        queue.append(G[pos].yes)
    if G[pos].no!=-1:
        queue.append(G[pos].no)

print(vis)
tail=vis[1]
for i in vis:
    if vis[i]>tail:
        vis[i]=vis[i]-1
vis[1]=len(vis)
print(vis)
v=sorted(vis.items(),key = operator.itemgetter(1))
print(v)
print("STEP%-2d:  开始" % 0)
for (pos,i) in v:
    print("STEP%-2d:  " % (i), end="")
    if G[pos].type == 2:
        if G[pos].yes != -1 and G[pos].no != -1:
            print("判断%s 如果条件为真，跳转到STEP%d；否则，跳转到STEP%d" % (G[pos].content, vis[G[pos].yes], vis[G[pos].no]))
        if G[pos].yes != -1 and G[pos].no == -1:
            print("判断%s 如果条件为真，跳转到STEP%d" % (G[pos].content, vis[G[pos].yes]))
        if G[pos].yes == -1 and G[pos].no != -1:
            print("判断%s 如果条件为假，跳转到STEP%d" % (G[pos].content, vis[G[pos].no]))
    else:
        print(G[pos].content)
'''
queue = deque()
queue.append(0)
visited=[]
cnt=0
while len(queue)!=0:
    pos = queue[0]
    queue.popleft()
    if pos in visited:
        continue
    if pos==0:
        cnt=0
        print("STEP%-2d:  开始" % (cnt))
    else:
        cnt=cnt+1
        print("STEP%-2d:  "%(cnt),end="")
        if G[pos].type==2:
            if G[pos].yes!=-1 and G[pos].no!=-1:
                print("判断%s 如果条件为真，跳转到STEP%d；否则，跳转到STEP%d" % (G[pos].content,vis[G[pos].yes],vis[G[pos].no]))
            if G[pos].yes!=-1 and G[pos].no==-1:
                print("判断%s 如果条件为真，跳转到STEP%d" % (G[pos].content,vis[G[pos].yes]))
            if G[pos].yes==-1 and G[pos].no!=-1:
                print("判断%s 如果条件为假，跳转到STEP%d" % (G[pos].content,vis[G[pos].no]))
        else:
            print(G[pos].content)
    visited.append(pos)
    if G[pos].yes!=-1:
        queue.append(G[pos].yes)
    if G[pos].no!=-1:
        queue.append(G[pos].no)'''