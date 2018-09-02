#!/usr/bin/env python3
# coding=utf-8

"""
LP II - P1
Author: FelipeCRamos
"""
import pandas as pd
import os

def r_part(raw):
    '''Function to get correct coligation from the split string'''
    raw = raw.split(' - ')
    if len(raw) > 1:
        return raw[1]
    else:
        return raw[0]

# read data from csv file
df = pd.read_csv("data/eleicao.csv", delimiter=";")
df['Partido'] = df['Partido/Coligação'].apply(lambda x: x.split(' - ')[0])
df['Coligação'] = df['Partido/Coligação'].apply(r_part)

# given data
aval_pos = 29
real_qe = 12684

# calculations of useful data
valid_votes = df['Votos'].sum()
local_qe = valid_votes / aval_pos

print("Valid votes:\t{}\nQE:\t\t{}".format(valid_votes, local_qe))

# creation of the partido dataframe
partido_df = df[['Coligação', 'Votos']]

# make the sum of valid_votes for each partido
partido_df = partido_df.groupby('Coligação').sum()

# calculate the QP of each partido
partido_df['QP'] = partido_df['Votos'] // real_qe

# get the number of used positions
used_pos = partido_df['QP'].sum()

# create the 'vagas_recebidas' label
partido_df['vagas_recebidas'] = 0
aval_pos -= used_pos

# distributes the residual positions for each partido
for i in list(range(0, int(aval_pos))):
    partido_df['Media'] = partido_df['Votos'] / (partido_df['QP'] + partido_df['vagas_recebidas'] + 1)
    partido_df.sort_values(by='Media', ascending=False, inplace=True)
    partido_df['vagas_recebidas'][0] += 1

# sort by the available positions
partido_df['Vagas'] = partido_df['QP'] + partido_df['vagas_recebidas']
partido_df.drop(['Media', 'QP', 'vagas_recebidas', 'Votos'], axis=1, inplace=True)
partido_df.sort_values(by=['Vagas'], inplace=True, ascending=False)
partido_df = partido_df[partido_df['Vagas'] > 0].dropna(subset=['Vagas'])

# last process, get the selected politicans
eleitos = []
for index in partido_df.index:
    available_positions = partido_df.loc[index]
    ldf = df[df['Coligação'] == index]
    ldf.sort_values(by='Votos', ascending=False, inplace=True)
    if( int(available_positions) > 0 ):
        eleitos.append(ldf[0:int(available_positions)])

# generate the results
result = pd.concat(eleitos)
result.sort_values(by='Votos', ascending=False, inplace=True)

os.system("mkdir output")
# export to the output file ('eleicao.tsv')
result.to_csv(
    'output/results.csv',
    sep = ';',
    index = False,
    columns = [
        'Número',
        'Nome',
        'Partido/Coligação',
        'Votos'
    ]
)
