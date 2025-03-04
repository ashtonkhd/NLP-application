import matplotlib.pyplot as plt

def createPlot(amount_with, total, path):
    _with = amount_with
    _total = total
    _without = _total - _with
    
    _with_procent = round((_with/_total)*100)
    _without_procent = round((_without/_total)*100)
    
    labels = 'Results', 'Rest'
    sizes = [_with_procent, _without_procent]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels)
    plt.savefig(path)


if __name__ == "__main__":
    createPlot(25, 200, '../static/term_plot.png')
