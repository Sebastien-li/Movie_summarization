from rouge_score import rouge_scorer
import os

new_segmented_screenplays = 'Segmented_screenplays'
chosen_path= 'selected_scenes'

scorer = rouge_scorer.RougeScorer(['rouge1', 'rougeL'], use_stemmer=True)

for movie in ['Arbitrage', 'Die_Hard','Juno','Moon','One_Eight_Seven','Panic_Room','Slumdog_Millionaire','Soldier','The_Back-up_Plan','The_Breakfast_Club']:

    with open(chosen_path+"\\"+movie+".txt", 'r',encoding="utf8") as f1:
        align=""
        for line in f1.readlines():
            align+=line.replace("\n"," ").replace("=","")

    with open(new_segmented_screenplays+"\\"+movie+"_tripod.txt", 'r',encoding="utf8") as f2:
        tripod=""
        for line in f2.readlines():
            tripod+=line.replace("\n"," ").replace("=","")

    with open(new_segmented_screenplays+"\\"+movie+"_random.txt", 'r',encoding="utf8") as f3:
        random=""
        for line in f3.readlines():
            random+=line.replace("\n"," ").replace("=","")

    scores = scorer.score(align,tripod)
    print("For {},  {}\n".format(movie,scores))

    scores = scorer.score(random,tripod)
    print("For random scenes of {}, {}\n\n".format(movie,scores))