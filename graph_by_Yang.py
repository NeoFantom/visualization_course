import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import read_csv_by_Xue as xue

if __name__ == '__main__':
    df = xue.x_get_all_data('data', 'login.csv')

    email = nx.MultiGraph()
    rd = nx.MultiGraph()  # Research and development department
    hr = nx.MultiGraph()  # Human resource department
    fi = nx.MultiGraph()  # Finance department
    email.clear(); rd.clear(); hr.clear(); fi.clear();

    spam_key = ['新葡京', '釦', '扣', 'QQ:']
    rd_key = ['ALARM', 'RECOVER', 'Emerg', '警', '文档', '项目', '崩', '系统', '设计', '台', '需', '端', '测', '置', '技术', '汇', '段']
    hr_key = ['简历', '资料', '通知', '总结', 'Offer', '岗位', '考勤', '员', '候', '内', '迟', '旷', '早', '福']
    fi_key = ['财务', '资金', '报销', '会计', '税']


    def add_node_edge(graph: nx.MultiGraph, from_node, to_nodes, c):
        graph.add_node(from_node)
        for i in to_nodes.split(';'):
            graph.add_node(i)
            graph.add_edge(from_node, i, viz={'color':{'r':c[0], 'g':c[1], 'b':c[2], 'a': 1.0}})
            graph.add_edge()
            # graph.add_edge(frm, i)
        return graph


    for i in range(1917):
        # Filter garbage
        if any(j in df['subject'][i] for j in spam_key):
            pass
        # Add to RD
        elif any(j in df['subject'][i] for j in rd_key):
            rd = add_node_edge(rd, df['from'][i], df['to'][i], (255, 0, 0))
            email = add_node_edge(email, df['from'][i], df['to'][i], (255, 0, 0))
        # Add to HR
        elif any(j in df['subject'][i] for j in hr_key):
            hr = add_node_edge(hr, df['from'][i], df['to'][i], (0, 128, 0))
            email = add_node_edge(email, df['from'][i], df['to'][i], (0, 128, 0))
        # Add to Fi
        elif any(j in df['subject'][i] for j in fi_key):
            fi = add_node_edge(fi, df['from'][i], df['to'][i], (65, 105, 225))
            email = add_node_edge(email, df['from'][i], df['to'][i], (65, 105, 225))
        else:
            email = add_node_edge(email, df['from'][i], df['to'][i], (250, 128, 114))

    nx.write_gexf(email, 'C:/Users/Mio/workspace/Vis/data/email.gexf')
    nx.write_gexf(rd, 'C:/Users/Mio/workspace/Vis/data/rd.gexf')
    nx.write_gexf(hr, 'C:/Users/Mio/workspace/Vis/data/hr.gexf')
    nx.write_gexf(fi, 'C:/Users/Mio/workspace/Vis/data/fi.gexf')
