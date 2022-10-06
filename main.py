import psutil, wordcloud, os, random
from collections import Counter
#import matplotlib.pyplot as plt

fileName = "wordcloud.png"

processes = {}

def sortedByValue(d):
    sortedList = sorted(d.items(), key=lambda x:x[1])
    return dict(reversed(sortedList))

def mergeWithSubstring(target, substring):
    values = [v for k, v in processes.items() if substring in k or target in k]
    names = [k for k, v in processes.items() if substring in k]
    for name in names:
        processes.pop(name)
    if target in processes.keys():
        processes[target] += sum(values)
    else:
        processes[target] = sum(values)

def main():
    # get values 
    for process in psutil.process_iter():
        try:
            if process.name() in processes.keys():
                processes[process.name()] += process.memory_full_info().uss
            else:
                processes[process.name()] = process.memory_full_info().uss

        except: #psutil.AccessDenied
            continue
    
    # merge related values
    mergeWithSubstring("firefox", "Isolated")
    mergeWithSubstring("chrome", "chrome")
    mergeWithSubstring("steam", "steam")

    #biggestProcesses = dict(itertools.islice(sortedByValue(processes).items(), 80)) 
    word_could_dict=Counter(sortedByValue(processes).keys())

    colors = ['BuGn', 'GnBu', 'PuBu', 'PuBuGn', 'YlGnBu']
    
    cloud = wordcloud.WordCloud(width=1920, height=1200, margin=5, min_font_size = 6, font_step=2,
        stopwords=None, colormap=random.choice(colors)).generate_from_frequencies(word_could_dict)
    # Blues
    
    cloud.to_file(fileName)
    os.system(f"gsettings set org.gnome.desktop.background picture-uri '{os.getcwd()}/{fileName}'")

if __name__ == "__main__":
    main()