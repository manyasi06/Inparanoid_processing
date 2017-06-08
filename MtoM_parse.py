import pandas as pd
import numpy as np
import argparse


#read in file from options

parser = argparse.ArgumentParser()
parser.add_argument('-f' ,'--filename', type=argparse.FileType('r'))
parser.add_argument('-o' , '--outfile', type=argparse.FileType('w'))
args = parser.parse_args()


df = pd.read_table(args.filename)

# now we can use the same technique as in: http://stackoverflow.com/a/40449726/5741205
def split_list_in_cols_to_rows(df, lst_cols):
    # make sure `lst_cols` is a list
    if lst_cols and not isinstance(lst_cols, list):
        lst_cols = [lst_cols]
    # all columns except `lst_cols`
    idx_cols = df.columns.difference(lst_cols)

    # calculate lengths of lists
    lens = df[lst_cols[0]].str.len()

    return pd.DataFrame({
        col:np.repeat(df[col].values, df[lst_cols[0]].str.len())
        for col in idx_cols
    }).assign(**{col:np.concatenate(df[col].values) for col in lst_cols}) \
      .append(df.loc[lens==0, idx_cols]).fillna('') \
      .loc[:, df.columns]


#the only thing that I did to modify the string all was change the string regular expression to allow
#for a String that has a captial letter A-Z and repiptive digits for the first part of the regular expression
# This is good because I sometimes have to modify the fasta headers because of duplicates in Ensembl
df['OrtoB'] = df['OrtoB'].str.findall(r'([A-Za-z.:\d+]{1,}\s[\d\.]+)')
new = split_list_in_cols_to_rows(df, 'OrtoB')

#this is to do the first column of values as well just in case
#1st store column for the data by splitting on the space
orto = new['OrtoA'].str.split()
#remove all empty lists
orto = orto[orto.astype(bool)]
#get lengths of lists, but floor divide by 2 because pairs
lens = orto.str.len() // 2
#explode nested lists to array
orto2 = np.concatenate(orto.values)
#repeat index to explode
idx = new.index.repeat(lens)
#create DataFrame and join both column together
s = pd.DataFrame(orto2.reshape(-1,2), index=idx).apply(' '.join, axis=1).rename('OrtoA')
#remove original column and join s
new = new.drop('OrtoA', axis=1).join(s).reset_index(drop=True)

#write output to a csv file
new.to_csv(args.outfile)
