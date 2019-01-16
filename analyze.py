from collections import deque
import numpy as np
import json


def get_graph(filename):
    class node:
        str=""
        begin=0
        end=0
        def __init__(self,str,begin,end):
            self.str=str
            self.end=end
            self.begin=begin


    # container = deque()
    # container.append(["function",0,0])
    # print(container)
    box=[]# 存放关键字
    box.append(node("main",-1,-1))
    next_type = 1 #1:正确条件下运行 0：错误条件下运行

    symbol=["{","}"]
    s_keywords=["else","if","while","for"]
    j_keywords=["break","continue"]
    r_keywords=["return"]

    file = open(filename)
    file_str=[]
    cnt=0
    kuohao=[]
    kuohao2=[]
    for line in file:
        #print(line)
        cnt = len(file_str)
        file_str.append([line,0])#string if_is_a_folder
        if line.find("{")!=-1:
            kuohao.append(cnt)
            kuohao2.append(len(box)-1)
        if line.find("}")!=-1:
            k=kuohao2[-1]
            kk=kuohao[-1]
            box[k].begin=kk
            box[k].end=cnt
            kuohao2.pop()
            kuohao.pop()
        for substr in s_keywords:
            pos=line.find(substr)
            if pos!=-1:
                box.append(node(line[pos:line.rfind('\n')],-1,-1))
                file_str[-1][1]=len(box)-1
                break
            # print(container)
        if line.find("//")!=-1:
            div=line[line.find("//")+2:line.rfind('\n')]
            #print(div)
    print(file_str)
    stack=[]
    visited=[0 for i in range(0,len(box))]
    # interval_begin=0
    # interval_end=0
    '''
    def dfs(pos,depth):
        visited[pos] = 1
        print("    ", box[pos].str, "depth=", depth)
    
        for p in range(pos+1,len(box)):
            if box[p].end<box[pos].end and visited[p]==0:
                dfs(p,depth+1)
        return
    '''


    class graph_node:
        content=""
        type=0# 0:container 1:矩形 2:菱形 3:圆角矩形 4:平行四边形 5:fork
        linker=0 #container的连接
        yes=-1
        no=-1
        last=-1
        def __init__(self,str,i,j,yes,no,last):
            self.content=str
            self.type=i
            self.linker=j
            self.yes=yes
            self.no=no
            self.last=last

        def to_json(self):
            x={"content":self.content,"type":self.type,"linker":self.linker,"yes":self.yes,"no":self.no,"last":self.last}
            return json.dumps(x)



    graph=[]
    if_stack=[]#保存if位置，用于给else
    graph.append(graph_node("开始",3,0,-1,-1,-1))
    graph.append(graph_node("结束",3,0,-1,-1,-1))
    def bfs(pos,before,after):
        print("bfs ",pos,before,after)
        queue = deque()
        bfe=before
        aftr=after
        from_=box[pos].begin
        to_=box[pos].end
        i=from_
        while i!=to_:
            #print(if_stack)
            if file_str[i][1] != 0:# 两个括号之间
                line = file_str[i][0]
                if line.find("else") != -1 and line.find("if")==-1:#else
                    bf=if_stack[-1]
                    nxt=graph[graph[bf].yes].yes
                    pos = len(graph)  # pos pos+1 是新建的节点
                    if_stack.pop()
                    queue.append(pos + 1)
                    graph[bf].no = pos
                    graph.append(graph_node("else", 5, 0, pos + 1, -1, bf))
                    graph.append(graph_node("container", 0, file_str[i][1], nxt, -1, pos))
                    pass
                if line.find("else")!=-1 and line.find("if")!=-1:   #else if
                    bf = if_stack[-1]
                    nxt = graph[graph[bf].yes].yes
                    str = line[line.find("//") + 2:line.rfind('\n')] if line.find("//") != -1 else line[line.find(
                        "(") + 1:line.rfind(')')]
                    pos = len(graph)  # pos pos+1 是新建的节点
                    if_stack.pop()
                    if_stack.append(pos)
                    queue.append(pos + 1)
                    graph[bf].no = pos
                    graph.append(graph_node(str, 2, 0, pos + 1, -1, bf))
                    graph.append(graph_node("container", 0, file_str[i][1], nxt, -1, pos))
                    pass
                if line.find("if")!=-1 and line.find("else")==-1:       # if
                    str = line[line.find("//") + 2:line.rfind('\n')] if line.find("//") != -1 else line[line.find(
                        "(") + 1:line.rfind(')')]
                    pos = len(graph)  # pos pos+1 pos+2 是新建的节点
                    if_stack.append(pos)
                    queue.append(pos+1)
                    graph[bfe].yes = pos
                    graph[aftr].last = pos + 2
                    graph.append(graph_node(str, 2, 0, pos + 1, pos+2,bfe))
                    graph.append(graph_node("container", 0, file_str[i][1], pos+2, -1,pos))
                    graph.append(graph_node("fork", 5, 0, aftr, -1,pos+1))
                    bfe = pos + 2

                if line.find("for")!=-1:
                    str=line[line.find("(") + 1:line.rfind(')')]
                    str=str.split(";")
                    pos=len(graph)#pos pos+1 pos+2 pos+3是新建的四个节点
                    queue.append(pos + 2)
                    graph[bfe].yes = pos
                    graph[aftr].last = pos+4
                    #print("for",bfe)
                    graph.append(graph_node(str[0], 1, 0, pos+1, -1,bfe))
                    graph.append(graph_node(str[1], 2, 0, pos+2, pos+4,pos))
                    graph.append(graph_node("container", 0, file_str[i][1], pos+3,-1,pos+1))
                    graph.append(graph_node(str[2], 1, 0, pos + 1, -1,pos+2))
                    graph.append(graph_node("fork", 5, 0, aftr, -1, pos+1))
                    bfe=pos+4

                if line.find("while")!=-1:
                    str = line[line.find("//") + 2:line.rfind('\n')] if line.find("//") != -1 else line[line.find(
                        "(") + 1:line.rfind(')')]
                    pos = len(graph)  # pos pos+1 pos+2是新建的节点
                    queue.append(pos + 1)
                    graph[bfe].yes = pos
                    graph[aftr].last = pos+2
                    graph.append(graph_node(str, 2, 0, pos + 1, pos+2, bfe))
                    graph.append(graph_node("container", 0, file_str[i][1], pos, -1, pos))
                    graph.append(graph_node("fork", 5, 0, aftr, -1, pos))
                    bfe = pos+2
            elif file_str[i][0].find("//")!=-1:#一般有注释代码

                line = file_str[i][0]
                #print(line[line.find("//") + 2:line.rfind('\n')], aftr, bfe)
                pos = len(graph)
                graph.append(graph_node(line[line.find("//") + 2:line.rfind('\n')], 1, 0,aftr,-1,bfe))#建立节点
                graph[bfe].yes=pos #将该节点连在前一个节点的yes上，表明顺序进行
                bfe=pos #修改before

            if file_str[i][1]!=0:
                i=box[file_str[i][1]].end+1
            else:
                i=i+1
        while len(queue)!=0:
            i=queue[0]
            bfs(graph[i].linker,graph[i].last,graph[i].yes)# TODO 不应该用i-1
            queue.popleft()
        return

    bfs(0,0,1)

    cnt = 0
    for item in graph:
        if graph[item.no].type == 5:  # 处理第五类节点
            item.no = graph[item.no].yes
        if graph[item.yes].type == 5:  # 处理第五类节点
            item.yes = graph[item.yes].yes
        cnt = cnt + 1
    cnt = 0
    for item in graph:
        if graph[item.no].type == 5:  # 处理第五类节点
            item.no = graph[item.no].yes
        if graph[item.yes].type == 5:  # 处理第五类节点
            item.yes = graph[item.yes].yes
        cnt = cnt + 1

    queue = deque()
    queue.append(0)
    visited = [0 for i in range(0, len(graph))]
    visited[0] = 1
    while len(queue) != 0:
        pos = queue[0]
        #print(graph[pos].content, end="")
        if graph[pos].yes != -1 and visited[graph[pos].yes] == 0:
            if graph[graph[pos].yes].type == 0:
                graph[pos].yes = -1
                continue
            queue.append(graph[pos].yes)
            visited[graph[pos].yes] = 1
            # print("\tyes:",G[G[pos].yes].content,end="")
        if graph[pos].no != -1 and visited[graph[pos].no] == 0:
            if graph[graph[pos].no].type == 0:
                graph[pos].no = -1
                continue
            queue.append(graph[pos].no)
            visited[graph[pos].no] = 1
            # print("\tno:", G[G[pos].no].content,end="")
        queue.popleft()


    return graph