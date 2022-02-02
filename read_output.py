import sys
import os
import json
import random
import glob
import re

os.chdir("C:\\Users\\Sébastien\\Documents\\AligNarr-master")

movie_list = ['arbitrage', 'die', 'juno', 'moon', 'one', 'panic', 'breakfast', 'slumdog', 'soldier', 'backup']

movie_code = {'arbitrage': 'Arbitrage',
                'die': 'Die_Hard',
                'juno': 'Juno',
                'moon': 'Moon',
                'one': 'One_Eight_Seven',
                'panic': 'Panic_Room',
                'breakfast': 'Slumdog_Millionaire',
                'slumdog': 'Soldier',
                'soldier': 'The_Back-up_Plan',
                'backup': 'The_Breakfast_Club',
                }
movie_code_invert = {v: k for k, v in movie_code.items()}

def segment_screenplay(m,script_file, new_script_file_align, new_script_file_tripod):
    """
    Find the manual segmentation of the screenplay into scenes and re-write the
    script file with seperation markers. Each scene is separated with a sequence
    of 40 '=' from the previous and next one. Also, before the beginning of each
    scene the scene index (starting from 0) is written between the '=' boundaries.
    :param script_file: Original raw script file for a movie
    :param new_script_file: New segmented script file
    :return: -
    """
    movie_name=m
    scenes = []
    last_scene = ''
    flag = 0

    with open(script_file, 'r',encoding="utf8") as f1:
        for line in f1.readlines():
            line_new = re.sub(' +', ' ', line)
            tmp_line = line_new.split()
            tmp_line = [x for x in tmp_line if x != '']
            if ((('INT.' in tmp_line or 'EXT.' in tmp_line or 'INT/EXT.' in tmp_line or
                             'EXT./INT.' in tmp_line or 'INT./EXT.' in tmp_line))):
                flag = 1
                if last_scene != '':
                    scenes.append(last_scene)
                last_scene = line
            else:
                if flag == 1:
                    last_scene += ('\n' + line)
    scenes.append(last_scene)

    for i in l[movie_code_invert[movie_name]+'.json']:

        scene=scenes[i]


        with open(new_script_file_align, 'a+',encoding="utf8") as f1:
            f1.write('='*20)
            f1.write(str(i))
            f1.write('='*20)
            f1.write('\n')
            f1.write(scene)
            f1.write('\n')
            f1.write('='*40)
            f1.write('\n')

    for i in tripod[movie_name]:

        scene=scenes[i]


        with open(new_script_file_tripod, 'a+',encoding="utf8") as f1:
            f1.write('='*20)
            f1.write(str(i))
            f1.write('='*20)
            f1.write('\n')
            f1.write(scene)
            f1.write('\n')
            f1.write('='*40)
            f1.write('\n')

    return

def difference_score(l1,l2):
    score=0
    for i in l1:
        score+=(i-min(l2,key=lambda j:abs(j-i)))**2
    score/=len(l1)
    return score

if __name__ == '__main__':

    l={}
    for filename in os.listdir("C:\\Users\\Sébastien\\Documents\\AligNarr-master\\output_files\\auto_alignment_bm25.w2v.sts"):
        l[filename]=[]
        with open(os.path.join("C:\\Users\\Sébastien\\Documents\\AligNarr-master\\output_files\\auto_alignment_bm25.w2v.sts", filename), 'r') as f:
            data=json.load(f)
            for d in data["summary"].values():
                for j in d:
                    if int(j[5:])-1 not in l[filename]: l[filename].append(int(j[5:])-1)
        l[filename].sort()

    tripod={}
    tripod["The_Back-up_Plan"]=[9, 10,40, 41,82,106, 107, 111,131]
    tripod["Juno"]=[3,31, 32,39, 40, 41,86, 87, 89,7]
    tripod["Soldier"]=[35,51,109,210,223]
    tripod["Panic_Room"]=[17, 18, 20,56, 58,135,148,159, 160]
    tripod["Arbitrage"]=[35, 36, 37,57, 62,67, 87, 88,105,109]
    tripod["The_Breakfast_Club"]=[5,20,31,31,34, 39]
    tripod["Slumdog_Millionaire"]=[32,108,139,150, 157,188, 191]
    tripod["Die_Hard"]=[11, 12,26, 28, 30,99, 100,114, 115,116, 117]
    tripod["Moon"]=[44, 45,68, 69,83, 84,94,143, 144]
    tripod["One_Eight_Seven"]=[30, 31,39,86, 87, 88, 89,142,142]

    dict_score={}
    dict_random_score={}

    for code in l:
        movie_name=movie_code[code[:-5]]
        alig_list=l[code]

        tripod_list=tripod[movie_name]

        tl=[]
        for i,x in enumerate(alig_list):
            if x>=2 and x-1!=alig_list[i-1]: tl.append(x-1)
            tl.append(x)
            if x+1<=max(tripod_list) and i<len(alig_list)-1 and x+1!=alig_list[i+1]: tl.append(x+1)
        alig_list=tl

        print("\n{}\nThe scenes selected by Alignarr are :{}\nThe scenes selected by TRIPOD are :{}\nThe intersection is : {}".format(movie_name,alig_list,tripod_list,list(set(alig_list)&set(tripod_list))))
        score=difference_score(tripod_list,alig_list)
        print("The difference score between the alignarr list and the tripod list is:",score)
        dict_score[movie_name]=score
        rand_score=0
        for i in range(100):
            randlist=random.sample(range(1,max(max(tripod_list),max(alig_list))),len(tripod_list))
            rand_score+=difference_score(tripod_list,randlist)/100
        print("Over 100 random samples, the difference score between the random list and the tripod list is:",rand_score)
        dict_random_score[movie_name]=rand_score




"""
    screenplays_folder = 'test_movies/10_movies'
    new_segmented_screenplays = 'Segmented_screenplays'

    if not os.path.exists(new_segmented_screenplays):
        os.makedirs(new_segmented_screenplays)

    movie_folder_list = [x[0] for x in os.walk(screenplays_folder)]
    movie_folder_list = glob.glob(screenplays_folder + "/*/")

    for movie in movie_folder_list:
        movie_name = movie.split('\\')[-2]
        print(movie_name)
        script_file = os.path.join(movie, 'script_clean.txt')
        new_script_file_align = os.path.join(new_segmented_screenplays,
                                       movie_name + '_align.txt')

        new_script_file_tripod = os.path.join(new_segmented_screenplays,
                                       movie_name + '_tripod.txt')

        segment_screenplay(movie_name,script_file, new_script_file_align,new_script_file_tripod)

"""
print()