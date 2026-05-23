from typing import *
import pandas as pd
import numpy as np
#import altair as alt
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib as mpl
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes, mark_inset
from simul import simulate_with_liar, simulate_without_liar
from utils import Config
import seaborn as sns


<<<<<<< Updated upstream
def boxplot(fig = None, ax = None, do_lie = False, tactic: Literal["random", "select"] = "random"):
    if do_lie is True:
        benign, cheater, _ = simulate_with_liar(model_acc=0.8, played_match=20, vote_per_match=1, benign_num=2, cheater_num=1, tactic=tactic)
    elif do_lie is False:
        benign, cheater, _ = simulate_without_liar(model_acc=0.8, played_match=20, vote_per_match=1, benign_num=2, cheater_num=1)
=======
# Default values
BENIGN_NUM = 2
CHEATER_NUM = 1

LIE_TYPE: Literal["radom", "select"] = "random"
LIE_FREQ = 0.5

REPORT_CNT = 3

MODEL_ACC = 0.9

################# Non lier ####################
def simulate_without_liar(
    report_cnt=REPORT_CNT,
    test_cnt=1,
    model_acc=MODEL_ACC,
    benign_num=BENIGN_NUM,
    cheater_num=CHEATER_NUM,
):
    """
    report_cnt: Means number of game played. Server is being initalized for each game
    test_cnt: Means number of voting in one game
    """
    # We don't need to check validity because no one lies
    # Therefore, only check "dubious"
    user_lst = [Benign(i, model_acc) for i in range(benign_num)]
    user_lst += [Cheater(i, model_acc, is_lier=False) for i in range(cheater_num)]

    benign, cheater = [], []
    for _ in range(report_cnt):
        # Reset Server and repeat evaluation for REPORT_CNT times
        server = Server(benign_num, cheater_num)
        # Evalute for test_cnt times
        for _ in range(test_cnt):
            server.simul_match(user_lst)
        for user in user_lst:
            dubi = server.dubious[user.name]
            if user.name.startswith("user"):
                benign.append(dubi)
            elif user.name.startswith("cheater"):
                cheater.append(dubi)

    return benign, cheater, server


def boxplot_for_nonlier(fig = None, ax = None):
    benign, cheater, _ = simulate_without_liar(model_acc=0.9, report_cnt=20)
>>>>>>> Stashed changes

    benign_dub = [benign[key][0] for key in benign.keys()]
    cheater_dub = [cheater[key][0] for key in cheater.keys()]
    if ax is None:
        fig, ax = plt.subplots()
        
    ax.boxplot([benign_dub, cheater_dub])
    ax.set_ylim(-4, 4)
    ax.set_ylabel("Dubious", labelpad=0.0)
    ax.set_xticks([1, 2], ["Benign user", "Cheating User"])
    return fig, ax 


def scatter_and_line(fig = None, ax = None,  do_lie = False, tactic: Literal["random", "select"] = "random"):
    model_acc = np.linspace(1.0, 0.5, 100).tolist()

    benign_scat, cheater_scat = {"acc": [], "dub": []}, {"acc": [], "dub": []}
    benign_line, cheater_line = [], []

    for acc in model_acc:
        # function call below assume
        # played 10 games and 2 votes per each game
        if do_lie is True:
            benign, cheater, _ = simulate_with_liar(model_acc=acc, played_match=10, vote_per_match=2, benign_num=2, cheater_num=1, tactic=tactic)
        elif do_lie is False:
            benign, cheater, _ = simulate_without_liar(model_acc=acc, played_match=10, vote_per_match=2, benign_num=2, cheater_num=1)
        benign_dub = [benign[key][0] for key in benign.keys()]
        cheater_dub = [cheater[key][0] for key in cheater.keys()]
        # scatter
        benign_scat["acc"] += [acc for _ in benign_dub]
        benign_scat["dub"] += benign_dub
        cheater_scat["acc"] += [acc for _ in cheater_dub]
        cheater_scat["dub"] += cheater_dub
        # line
        benign_line.append(sum(benign_dub) / len(benign_dub))
        cheater_line.append(sum(cheater_dub) / len(cheater_dub))

    if fig is None and ax is None:  
        fig, ax = plt.subplots()
    ax.set_ylim(-7, 7)
    ax.set_xlim(0.5, 1.0)
    ax.set_ylabel("Dubious", labelpad=0.0)
    ax.set_xlabel("Model Acc")

    # plot
    ax.plot(model_acc, benign_line, label="Benign user")
    ax.plot(model_acc, cheater_line, label="Cheating user")
    ax.legend(loc='upper left')

    # scatter
    # ax.scatter('acc', 'dub', data=benign_scat)
    # ax.scatter('acc', 'dub', data=cheater_scat)

    # trendline
    z = np.polyfit(benign_scat["acc"], benign_scat["dub"], 1)
    p = np.poly1d(z)
    ax.plot(benign_scat["acc"], p(benign_scat["acc"]), "b--")
    z = np.polyfit(cheater_scat["acc"], cheater_scat["dub"], 1)
    p = np.poly1d(z)
    ax.plot(cheater_scat["dub"], p(cheater_scat["dub"]), "r--")

    return ax


def contour(fig = None, ax = None, do_lie = False, tactic: Literal["random", "select"] = "random"):
    TOTAL_USER = 100
    vote_cnt = 2
    match_cnt = 1
    model_acc = np.linspace(1.0, 0.5, TOTAL_USER // 2).tolist()
    cheat_rate = []
    sim_acc = []
    
    for cheat_num in range(TOTAL_USER // 2):
        cheat_rate.append(cheat_num / TOTAL_USER)
        sim_ret = []
        for acc in model_acc:
            if do_lie is True:
                benign, cheater, _ = simulate_with_liar(model_acc=acc, played_match=match_cnt, vote_per_match=vote_cnt, benign_num=TOTAL_USER - cheat_num, cheater_num=cheat_num, tactic=tactic)
            elif do_lie is False:
                benign, cheater, _ = simulate_without_liar(model_acc=acc, played_match=match_cnt, vote_per_match=vote_cnt, benign_num=TOTAL_USER - cheat_num, cheater_num=cheat_num)
            
            benign_dub = [benign[key][0] for key in benign.keys()]
            cheater_dub = [cheater[key][0] for key in cheater.keys()]
            correct = len(list(filter(lambda x: x < 0, benign_dub))) + len(
                list(filter(lambda x: x > 0, cheater_dub))
            )
            sim_ret.append(correct / (TOTAL_USER * match_cnt))
        sim_acc.append(sim_ret)

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    ax.set_ylabel("Cheater Rate")
    ax.set_xlabel("Model Acc")
    X, Y = np.meshgrid(model_acc, cheat_rate)
    co = ax.contourf(X, Y, sim_acc, levels=np.linspace(0.5, 1.0, 11), extend='min')
    fig.colorbar(co, ax=ax)
    
    return fig, ax


def plot_one_third_cheater(fig = None, ax = None, do_lie = False, tactic: Literal["random", "select"] = "random"):

    TOTAL_USER = 100
    cheat_user = 33
    vote_cnt = 1
    match_cnt = 10
    model_acc = np.linspace(1.0, 0.5, TOTAL_USER // 2).tolist()

    sim_ret = []
    for acc in model_acc:
        if do_lie is True:
            benign, cheater, _ = simulate_with_liar(model_acc=acc, played_match=match_cnt, vote_per_match=vote_cnt, benign_num=TOTAL_USER - cheat_user, cheater_num=cheat_user, tactic=tactic)
        elif do_lie is False:
            benign, cheater, _ = simulate_without_liar(model_acc=acc, played_match=match_cnt, vote_per_match=vote_cnt, benign_num=TOTAL_USER - cheat_user, cheater_num=cheat_user)
        
        benign_dub = [benign[key][0] for key in benign.keys()]
        cheater_dub = [cheater[key][0] for key in cheater.keys()]
        correct = len(list(filter(lambda x: x < 0, benign_dub))) + len(
            list(filter(lambda x: x > 0, cheater_dub))
        )
        sim_ret.append(correct / (TOTAL_USER * match_cnt))

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    ax.plot(model_acc, sim_ret, 'o-')
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Model Acc")

    return fig, ax

<<<<<<< Updated upstream
=======
##############################################

#################### Lier ####################


def simulate_with_liar(
    report_cnt=REPORT_CNT,
    test_cnt=1,
    model_acc=MODEL_ACC,
    benign_num=BENIGN_NUM,
    cheater_num=CHEATER_NUM,
):
    """
    report_cnt: Counting for send-recv - EX) battle for 5 times
    test_cnt: Test count per 1 report - EX) there was 2 report at first battle
    """
    # We don't need to check validity because no one lies
    # Therefore, only check "dubious"
    user_lst = [Benign(i, model_acc) for i in range(benign_num)]
    user_lst += [
        Cheater(i, model_acc, is_lier=True, lier_type=LIE_TYPE, lie_freq=LIE_FREQ)
        for i in range(cheater_num)
    ]

    benign, cheater = [], []
    for _ in range(report_cnt):
        # Reset Server and repeat evaluation for REPORT_CNT times
        server = Server(benign_num, cheater_num)
        # Evalute for test_cnt times
        for _ in range(test_cnt):
            server.simul_match(user_lst)
        for user in user_lst:
            dubi = server.dubious[user.name]
            if user.name.startswith("user"):
                benign.append(dubi)
            elif user.name.startswith("cheater"):
                cheater.append(dubi)

    return benign, cheater, server # TODO server 리팩토링


def boxplot_for_lier(fig = None, ax = None):
    benign, cheater = simulate_with_liar(model_acc=0.9, report_cnt=20)

    if ax is None:
        fig, ax = plt.subplots()
    ax.boxplot([benign, cheater])
    ax.set_ylim(-1.0, 1.0)
    ax.set_ylabel("Dubious")
    ax.set_xticks([1, 2], ["Benign user", "Cheating User"])
    return fig, ax

# 그래프 의미: 모델 정확성이 증가할 수록
# 일반 유저와 치터를 잘 구분할 수 있다
def scatter_and_line_for_lier(fig = None, ax = None):
    model_acc = np.linspace(1.0, 0.5, 100).tolist()

    benign_scat, cheater_scat = {"acc": [], "val": []}, {"acc": [], "val": []}
    benign_line, cheater_line = [], []

    for acc in model_acc:
        # function call below assume
        # total 3 battles and 2 reports per 1 battle
        benign, cheater = simulate_with_liar(report_cnt=10, test_cnt=2, model_acc=acc)
        # scatter
        benign_scat["acc"] += [acc for _ in benign]
        benign_scat["val"] += benign
        cheater_scat["acc"] += [acc for _ in cheater]
        cheater_scat["val"] += cheater
        # line
        benign_line.append(sum(benign) / len(benign))
        cheater_line.append(sum(cheater) / len(cheater))

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    ax.set_ylim(-1.2, 1.2)
    ax.set_ylabel("Dubious")
    ax.set_xlabel("Model Acc")

    # plot
    ax.plot(model_acc, benign_line, label="Benign user")
    ax.plot(model_acc, cheater_line, label="Cheating user")
    ax.legend(loc='upper left')

    # scatter
    # ax.scatter('acc', 'val', data=benign_scat)
    # ax.scatter('acc', 'val', data=cheater_scat)

    # trendline
    z = np.polyfit(benign_scat["acc"], benign_scat["val"], 1)
    p = np.poly1d(z)
    ax.plot(benign_scat["acc"], p(benign_scat["acc"]), "b--")
    z = np.polyfit(cheater_scat["acc"], cheater_scat["val"], 1)
    p = np.poly1d(z)
    ax.plot(cheater_scat["acc"], p(cheater_scat["acc"]), "r--")

    return fig, ax


def contour_for_lier(fig = None, ax = None):
    """
    input: (치팅 사용자 비율, 모델 정확성, 거짓말쟁이 비율)
        치팅 사용자 비율: 전체 사용자 500명으로 설정 최대 50% 까지 - 사용자가 5000인 이유는 세세한 평가치를 만들기위해
        모델 정확성: 1.0에서 0.5까지
        거짓말쟁이 비율: 1.0에서 0.5까지 --> 현재 글로벌 변수로 관리하고 있음 고처야함(TODO)
    output: 시뮬레이션 정확성
        정확성: 정답 판정의 경우 Non cheater의 경우 의심도 양, Cheater의 경우 음일 경우를 옳바른 경우로 따진다

    -- 그래프 결과: 거짓말 하는 유저가 존재하지 않느다면, 모델 정확성이 0.8 이상을 만족할 경우 치터/비치터를 구분할 수 있다
    ++ 그래프 결과: 거짓말 하는 유저가 한다면, 치팅 사용자 비율에 따라서 모델 정확성인 0.9 이상을 만족해야지 치터/비치터를 구분할 수 있다
    """
    TOTAL_USER = 50
    model_acc = np.linspace(1.0, 0.5, TOTAL_USER // 2).tolist()
    cheat_rate = []
    sim_acc = []

    for cheat in range(TOTAL_USER // 2):
        cheat_rate.append(cheat / TOTAL_USER)
        sim_ret = []
        for acc in model_acc:
            benign, cheater = simulate_with_liar(
                REPORT_CNT, 2, acc, TOTAL_USER - cheat, cheat
            )
            correct = len(list(filter(lambda x: x < 0, benign))) + len(
                list(filter(lambda x: x > 0, cheater))
            )
            sim_ret.append(correct / (TOTAL_USER * REPORT_CNT))
        sim_acc.append(sim_ret)

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    ax.set_ylabel("Cheater Rate")
    ax.set_xlabel("Model Acc")
    X, Y = np.meshgrid(model_acc, cheat_rate)
    co = ax.contourf(X, Y, sim_acc, levels=np.linspace(0.5, 1.0, 11), extend='min')
    fig.colorbar(co, ax=ax)
    
    return fig, ax

def plot_for_liar(fig = None, ax = None):
    """
    input: (치팅 사용자 비율, 모델 정확성, 거짓말쟁이 비율)
        치팅 사용자 비율: 전체 사용자 500명으로 설정 최대 50% 까지 - 사용자가 5000인 이유는 세세한 평가치를 만들기위해
        모델 정확성: 1.0에서 0.5까지
        거짓말쟁이 비율: 1.0에서 0.5까지 --> 현재 글로벌 변수로 관리하고 있음 고처야함(TODO)
    output: 시뮬레이션 정확성
        정확성: 정답 판정의 경우 Non cheater의 경우 의심도 양, Cheater의 경우 음일 경우를 옳바른 경우로 따진다

    -- 그래프 결과: 거짓말 하는 유저가 존재하지 않느다면, 모델 정확성이 0.8 이상을 만족할 경우 치터/비치터를 구분할 수 있다
    ++ 그래프 결과: 거짓말 하는 유저가 한다면, 치팅 사용자 비율에 따라서 모델 정확성인 0.9 이상을 만족해야지 치터/비치터를 구분할 수 있다
    """
    TOTAL_USER = 100
    cheater_num = 33
    model_acc = np.linspace(1.0, 0.5, TOTAL_USER // 2).tolist()

    sim_ret = []
    for acc in model_acc:
        benign, cheater = simulate_with_liar(
            REPORT_CNT, 2, acc, TOTAL_USER - cheater_num, cheater_num
        )
        correct = len(list(filter(lambda x: x < 0, benign))) + len(
            list(filter(lambda x: x > 0, cheater))
        )
        sim_ret.append(correct / (TOTAL_USER * REPORT_CNT))

    if fig is None and ax is None:
        fig, ax = plt.subplots()
    ax.plot(model_acc, sim_ret, 'o-')
    ax.set_ylabel("Accuracy")
    ax.set_xlabel("Model Acc")

    return fig, ax


def __contour_for_lier(fig, ax):
    """
    input: (치팅 사용자 비율, 모델 정확성, 거짓말쟁이 비율)
        치팅 사용자 비율: 전체 사용자 500명으로 설정 최대 50% 까지 - 사용자가 5000인 이유는 세세한 평가치를 만들기위해
        모델 정확성: 1.0에서 0.5까지
        거짓말쟁이 비율: 1.0에서 0.5까지 --> 현재 글로벌 변수로 관리하고 있음 고처야함(TODO)
    output: 시뮬레이션 정확성
        정확성: 정답 판정의 경우 Non cheater의 경우 의심도 양, Cheater의 경우 음일 경우를 옳바른 경우로 따진다

    -- 그래프 결과: 거짓말 하는 유저가 존재하지 않느다면, 모델 정확성이 0.8 이상을 만족할 경우 치터/비치터를 구분할 수 있다
    ++ 그래프 결과: 거짓말 하는 유저가 한다면, 치팅 사용자 비율에 따라서 모델 정확성인 0.9 이상을 만족해야지 치터/비치터를 구분할 수 있다
    """
    TOTAL_USER = 20
    model_acc = np.linspace(1.0, 0.5, TOTAL_USER // 2).tolist()
    cheat_rate = []
    sim_acc = []

    for cheat in range(TOTAL_USER // 2):
        cheat_rate.append(cheat / TOTAL_USER)
        sim_ret = []
        for acc in model_acc:
            benign, cheater = simulate_with_liar(
                REPORT_CNT, 2, acc, TOTAL_USER - cheat, cheat
            )
            correct = len(list(filter(lambda x: x > 0, benign))) + len(
                list(filter(lambda x: x < 0, cheater))
            )
            sim_ret.append(correct / (TOTAL_USER * REPORT_CNT))
        sim_acc.append(sim_ret)

    ax.set_ylabel("Cheater Rate")
    ax.set_xlabel("Model Acc")
    X, Y = np.meshgrid(model_acc, cheat_rate)
    co = ax.contourf(X, Y, sim_acc, levels=np.linspace(0, 1.0, 11), extend='min')
    ax.set_title(f"FREQ: {LIE_FREQ}")
    fig.colorbar(co, ax=ax)


def plot_how_stubborn_simple_version():
    """
    그래프 결과: 거짓말의 빈도(LIE_FREQ)의 변화와 상관없이 거의 비슷한 그림을 보여준다 = 식이 거짓말에 대해서 stubborn 하다. 즉 거짓말 하는 놈을 잘 걸러준다
    """
    global LIE_FREQ
    fig, axs = plt.subplots(2, 3, layout="constrained")
    for i in range(0, 6):
        LIE_FREQ = 0.5 + 0.1 * i
        __contour_for_lier(fig, axs[i // 3, i % 3])
    plt.show()


>>>>>>> Stashed changes

def figure_1():
    global LIE_TYPE, LIE_FREQ
    LIE_TYPE = 'random'
    
    fig, axs = plt.subplots(2, 3)
    boxplot(fig, axs[0, 0])
    boxplot(fig, axs[0, 1], do_lie=True, tactic="random")
    boxplot(fig, axs[0, 2], do_lie=True, tactic="select")
    
    scatter_and_line(fig, axs[1, 0])
    scatter_and_line(fig, axs[1, 1], do_lie=True, tactic="random")
    scatter_and_line(fig, axs[1, 2], do_lie=True, tactic="select")

    axs[0, 0].set_title('(1) Without liar', fontdict={'fontsize': 'x-large'})
    axs[0, 1].set_title('(2) With random liar', fontdict={'fontsize': 'x-large'})
    axs[0, 2].set_title('(3) With tactical liar', fontdict={'fontsize': 'x-large'})
    axs[1, 0].set_title('(1) Without liar', fontdict={'fontsize': 'x-large'})
    axs[1, 1].set_title('(2) With random liar', fontdict={'fontsize': 'x-large'})
    axs[1, 2].set_title('(3) With tactical liar', fontdict={'fontsize': 'x-large'})
    
    plt.suptitle("(a) Dubious score after simulation with fixed model acc (80%)", fontsize='xx-large', fontweight='bold')
    # Adjust vertical_spacing = 0.5 * axes_height
    plt.subplots_adjust(hspace=0.5)

    # Add text in figure coordinates
    plt.figtext(0.5, 0.485, '(b) Distribution of dubious score', ha='center', va='center', fontdict={'fontsize': 'xx-large', 'fontweight': 'bold'})
    fig.set_figwidth(13)
    fig.set_figheight(7)
    plt.savefig(fname='img/figure1.pdf', bbox_inches='tight', pad_inches=0)
    plt.savefig(fname='img/figure1.png', bbox_inches='tight', pad_inches=0)
    
def figure_2():

    fig, axs = plt.subplots(2, 3)
    plot_one_third_cheater(fig, axs[0, 0])
    plot_one_third_cheater(fig, axs[0, 1], do_lie=True, tactic="random")
    plot_one_third_cheater(fig, axs[0, 2], do_lie=True, tactic="select")
    
    contour(fig, axs[1, 0])
    contour(fig, axs[1, 1], do_lie=True, tactic="random")
    contour(fig, axs[1, 2], do_lie=True, tactic="select")

    axs[0, 0].set_title('(1) Without liar', fontdict={'fontsize': 'x-large'})
    axs[0, 1].set_title('(2) With random liar' , fontdict={'fontsize': 'x-large'})
    axs[0, 2].set_title('(3) With tactical liar' , fontdict={'fontsize': 'x-large'})
    axs[1, 0].set_title('(1) Without liar' , fontdict={'fontsize': 'x-large'})
    axs[1, 1].set_title('(2) With random liar' , fontdict={'fontsize': 'x-large'})
    axs[1, 2].set_title('(3) With tactical liar' , fontdict={'fontsize': 'x-large'})
    
    plt.suptitle("(a) Accuracy with fixed cheater rate (33%)", fontsize='xx-large', fontweight='bold')
    # Adjust vertical_spacing = 0.5 * axes_height
    plt.subplots_adjust(hspace=0.5)

    # Add text in figure coordinates
    plt.figtext(0.5, 0.485, '(b) Contour of accuracy', ha='center', va='center', fontdict={'fontsize': 'xx-large', 'fontweight': 'bold'})
    
    fig.set_figwidth(13)
    fig.set_figheight(7)
    plt.savefig(fname='img/figure2.png', bbox_inches='tight', pad_inches=0)  
    plt.savefig(fname='img/figure2.pdf', bbox_inches='tight', pad_inches=0)  
    
'''
def figure_appendix(playdata, e, cheater):
    for bat in playdata['battle']:
        bat['parti'] = str(bat['parti'])
        
    source = pd.DataFrame([bat for bat in playdata['battle']])
    chart = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='parti'
    )
    
    chart.save(f'img/battle/{playdata["game"]}-battle.png')
    
    if len(playdata['votes']) == 0:
        return
    source = pd.DataFrame([vote for vote in playdata['votes']])
    chart = alt.Chart(source).mark_bar().encode(
        x='start',
        x2='end',
        y='target'
    )
    
    chart.save(f'img/battle/{playdata["game"]}-vote.png')
    return
'''
def boxplot_figure_3(fig = None, ax = None, normal_score = (), cheater_score = ()):
    
    if ax is None:
        fig, ax = plt.subplots()
    

<<<<<<< Updated upstream
    ax.boxplot([normal_score[0], cheater_score[0]], labels=["Benign user", "Cheating User"])
    ax.set_ylabel("Dubious score", labelpad=0.0)
    
    ax.axhline(y=0, color='lightgray', linestyle='-', linewidth=16, label='Zoomed', alpha=0.4)
    
    FN_cases = np.where(normal_score[0] > 0, True, False)
    TP_cases = np.where(normal_score[0] < 0, True, False)
    FN = np.where(FN_cases, normal_score[0], None)
    TP = np.where(TP_cases, normal_score[0], None)
    ax.scatter([1 for _ in range(len(TP[TP != None]))], TP[TP != None],alpha=0.4, color='g', label="True Positive/Negative")
    ax.scatter([1 for _ in range(len(FN[FN != None]))], FN[FN != None], alpha=0.4, color='r', label="False Negative")

    FP_cases = np.where(cheater_score[0] < 0, True, False)
    TN_cases = np.where(cheater_score[0] > 0, True, False)
    FP = np.where(FP_cases, cheater_score[0], None)
    TN = np.where(TN_cases, cheater_score[0], None)
    ax.scatter([2 for _ in range(len(FP[FP != None]))], FP[FP != None], alpha=0.4, color='y', label="False Positive")
    ax.scatter([2 for _ in range(len(TN[TN != None]))], TN[TN != None],alpha=0.4, color='g')

    ax.axhline(y=0, color='#ff3300', linestyle='--', linewidth=1, label='Threshold')
    ax.set_ylim(-0.5, 4.5)
    
    # Zooming
    axins = zoomed_inset_axes(ax, 4, loc='upper left', axes_kwargs={'facecolor': 'lightgray'})
    # for labeling
    axins.axhline(y=0, color='lightgray', linestyle='-', linewidth=7, label='Zoomed', alpha=0.4)
    axins.axhline(y=0, color='#ff3300', linestyle='--', linewidth=1, label='Threshold')
    
    axins.scatter([0.05 for _ in range(len(TP[TP != None]))], TP[TP != None],alpha=0.8, color='g', vmin=0.2, vmax=0.2, label="True Positive/Negative")
    axins.scatter([0.05 for _ in range(len(FN[FN != None]))], FN[FN != None], alpha=0.8, color='r', vmin=0.2, vmax=0.2, label="False Negative")
    axins.scatter([0.15 for _ in range(len(FP[FP != None]))], FP[FP != None], alpha=0.8, color='y', vmin=0.2, vmax=0.2, label="False Positive")
    axins.scatter([0.15 for _ in range(len(TN[TN != None]))], TN[TN != None],alpha=0.8, color='g', vmin=0.2, vmax=0.2)
    

    
    axins.set_ylim(-0.2, 0.2)
    axins.set_xlim(0, 0.2)
    # ticks invisible
    axins.set_xticks([])
    axins.set_yticks([])
    axins.grid()
    
    
    return fig, ax 

def figure_3():
    from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

    from eval.eval import res as eval_res
    from eval.lie import res as lie_res

    fig = plt.figure()
    gs = fig.add_gridspec(3,3)
    sns.set_palette('bright')

    # Confusion matrix
    from matplotlib.colors import ListedColormap
    # Red, Orange, Green
    cmap = ListedColormap([[0.973,0.796,0.678],[1,0.91,0.592],[0.765,0.882,0.698]] + [[0.765,0.882,0.698]]*35)
    display_labels = ["N", "Ch"]
    tn, tp, fn, fp = np.sum(eval_res[:,4:8], axis=0, dtype=int)
    ax = fig.add_subplot(gs[1, 2])
    ConfusionMatrixDisplay(confusion_matrix=np.array([[tp,fn], [fp, tn]]), display_labels=display_labels).plot(
    include_values=True, cmap=cmap, ax=ax, colorbar=False, text_kw={'fontsize': 'xx-large', 'color':'black'})
    ax.set_title("Without liar")
    ax.xaxis.set_ticklabels(['','',])
    ax.set_xlabel('')
    ax.tick_params(axis='x', which='both',bottom=False)
    
    ax = fig.add_subplot(gs[2, 2])
    tn, tp, fn, fp = np.sum(lie_res[:,4:8], axis=0, dtype=int)
    ConfusionMatrixDisplay(confusion_matrix=np.array([[tp,fn], [fp, tn]]), display_labels=display_labels).plot(
    include_values=True, cmap=cmap, ax=ax, colorbar=False, text_kw={'fontsize': 'xx-large', 'color':'black'})
    ax.set_title("With liar")

    n_dubs, c_dubs = np.array([]), np.array([])
    n_vals, c_vals = np.array([]), np.array([])
    # Boxplot
    # result of eval/eval.py
    for i, r in enumerate(eval_res):
        s_agg, t_agg, _, thresh_acc = r[8:]
        
        normal_dub = np.where(np.invert(t_agg), s_agg, None)
        normal_dub = normal_dub[normal_dub != None] - thresh_acc

        n_dubs = np.append(n_dubs, normal_dub)
        
        cheater_score = np.where(t_agg, s_agg, None)
        cheater_score = cheater_score[cheater_score != None] - thresh_acc

        
        c_dubs = np.append(c_dubs, cheater_score)
        
    ax = fig.add_subplot(gs[:, 0])
    boxplot_figure_3(fig, ax, (n_dubs, n_vals), (c_dubs, c_vals))
    ax.set_title("Without liar", fontdict={'fontsize': 'x-large'})

    n_dubs, c_dubs = np.array([]), np.array([])
    n_vals, c_vals = np.array([]), np.array([])
    # result of eval/eval.py
    for i, r in enumerate(lie_res):
        s_agg, t_agg, _, thresh_acc = r[8:]
        
        normal_dub = np.where(np.invert(t_agg), s_agg, None)
        normal_dub = normal_dub[normal_dub != None] - thresh_acc

        n_dubs = np.append(n_dubs, normal_dub)
        
        cheater_score = np.where(t_agg, s_agg, None)
        cheater_score = cheater_score[cheater_score != None] - thresh_acc

        c_dubs = np.append(c_dubs, cheater_score)
    ax = fig.add_subplot(gs[:, 1])
    boxplot_figure_3(fig, ax, (n_dubs, n_vals), (c_dubs, c_vals))
    ax.set_title("With liar", fontdict={'fontsize': 'x-large'})
    # Title and legend
    plt.legend(bbox_to_anchor=(4.9, .8), loc='right', borderaxespad=0., framealpha=1, facecolor ='white', frameon=True)
    
    def set_title(rect_left = (0.13, -0.05, 0.5, 0.0), rect_right = (0.68, -0.05, 0.2, 0.0)):
        #rect_left = 0, 0, 0.5, 0.8  # x, y, width, height
        #rect_right = 0.5, 0, 0.5, 0.8
        ax_left = fig.add_axes(rect_left)
        ax_right = fig.add_axes(rect_right)
        ax_left.set_xticks([])
        ax_left.set_yticks([])
        ax_left.spines['right'].set_visible(False)
        ax_left.spines['top'].set_visible(False)
        ax_left.spines['bottom'].set_visible(False)
        ax_left.spines['left'].set_visible(False)
        ax_left.set_axis_off()
        ax_right.set_xticks([])
        ax_right.set_yticks([])
        ax_right.spines['right'].set_visible(False)
        ax_right.spines['top'].set_visible(False)
        ax_right.spines['bottom'].set_visible(False)
        ax_right.spines['left'].set_visible(False)
        ax_right.set_axis_off()
        ax_left.set_title('(a) Standardized dubious scores', fontdict={'fontsize': 'xx-large', 'fontweight': 'bold'})
        ax_right.set_title('(b) Results', fontdict={'fontsize': 'xx-large', 'fontweight': 'bold'})
    set_title()
    
    #axs[0].set_title("Without liar", fontdict={'fontsize': 'x-large'})
    #axs[1].set_title("With liar", fontdict={'fontsize': 'x-large'})

    fig.set_figwidth(9.6)
    fig.set_figheight(6)
    fig.savefig('img/figure3.pdf', bbox_inches='tight', pad_inches=0.1)
    fig.savefig('img/figure3.png', bbox_inches='tight', pad_inches=0.1)
    fig.savefig('img/figure3.eps', bbox_inches='tight', pad_inches=0.1)
    fig.savefig('img/figure3.svg', bbox_inches='tight', pad_inches=0.1)
    plt.show()
    
if __name__ == '__main__':
    figure_1()
    figure_2()
    figure_3()
=======
    #contour_for_lier(fig, axs[0, 2])
    figure_1()
>>>>>>> Stashed changes
