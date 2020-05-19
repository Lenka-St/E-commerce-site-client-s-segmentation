def desc_quali(data, variable):
    ''' Fonction qui calcule le nombre et le pourcentage de chaque modalité d'une variable qualitative
    args : data = DataFrame
           variable = le nom de variable en format 'NomDeVariable'
           
    sorties : DataFrame avec les modalités de variables, nombre et pourcentage de chaque modalité,
    ainsi que le nombre + pourcentage de  
    '''
    
    import pandas as pd
    from pandas import DataFrame    
         
    count = DataFrame(data[variable].value_counts())
    count['Pourcentage'] = count.apply(lambda row: round(row*100/sum(count[variable]),2))
    
    NA = data[variable].isna().sum()
    pourc_na=round(NA/data.shape[0],2)*100
    df = DataFrame([NA, pourc_na]).T
    df.rename(columns={0:variable, 1:'Pourcentage'}, index={0:'NaN'}, inplace=True)
    
    count = pd.concat([count, df])
    
    return count
    
    
def plot_bar_desc_quali(data, variable, titre):
    """ Fonction qui produit un bar plot d'une variable quantitative d'effectif issue de la fonction desc_quali
    
    !!! Attention : ne prend pas en compte le dernier argument (la fonction desc_quali produit l'effectif de Nan 
    à la dernière ligne de DataFrame)
    
    Entrées :
    - data : DataFrame
    - variable : le nom de variable quantitative entre ''
    - title : le titre de graphique entre ''
    
    Sortie :
    
    - barplot    
    """
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.set_style('whitegrid')
    #%matplotlib inline
    
    plt.figure()
    fig = plt.figure(figsize=(20,10))
    plt.title(titre)
    plt.bar(range(data.shape[0]-1), data[variable][:-1])
    plt.xticks(range(data.shape[0]-1), data.index[:-1])



    
def desc_quanti(data, *args):
    '''Fonction pour décrire les données quantitatives
    Arguments : DataFrame, variables en format 'NomDeVariable' 
    Sorties : DataFrame avec les statistiques descriptives, ainsi que le nombre de NaN pour chaque variable'''  
    
    from pandas import DataFrame, Series  
    
    df = DataFrame(columns=['count','mean', 'std', 'min', '25%', '50%', '75%', 'max', 'NaN'])
  
    for var in args:
    
        count = round(data[var].describe().loc['count'], 2)
        mean = round(data[var].describe().loc['mean'], 2)
        std = round(data[var].describe().loc['std'], 2)
        minimum = round(data[var].describe().loc['min'], 2)
        q1 = round(data[var].describe().loc['25%'], 2)
        med = round(data[var].describe().loc['50%'], 2)
        q3 = round(data[var].describe().loc['75%'], 2)
        maximum = round(data[var].describe().loc['max'], 2)
        NA = round(data[var].isna().sum(), 2)
    
   
        ser= Series({'count':count , 'mean':mean , 'std':std ,'min': minimum,'25%':q1 ,'50%':med ,'75%':q3 ,'max':maximum ,
                 'NaN':NA })
        ser.name=var
        df=df.append(ser)
  
    return df    
    
def transf_binaire_multiclass(data, var):
    """Fonction pour recoder des variables multiclasse en une variable binaire par classe:
    
    Entrées:
        data : DataFrame
        var : variable à recoder
    
    Sortie : 
        data : DataFrame qui contient les variables crées    
    """
    
    import numpy as np
    
    liste = data[var].value_counts().index
     
    for classe in liste:
        data['temp']=np.where(data[var]==classe,1,0)
        name = var + '_' + str(classe)
        data.rename(columns = {'temp':name}, inplace = True)
    return data
    
def sum_id(data, var, key):
    
    """Fonction va créer une nouvelle variable égale à la somme
    aggrégées par une variable clé. 
    
    La nouvelle variable est ensuite mergé à DataFrame d'origine à l'aide de la variable clé.
    
    Args :
    
    - data = DataFrame
    - var = variable à transformer en somme
    - clé = variable clé (non-unique) utilisée pour l'aggrégation (sur laquelle on fait "groupby")
    
    Sorties :
    
    - data = DataFrame avec la nouvelle variable créée  
    """
    
    group = data[var].groupby(data[key])
    temp=group.sum()
    data = data.merge(temp, on=key, how='left')
    
    name_x = var + "_x"
    name_y = var + "_y"
    new_name = var + "_sum"
    
    data.rename(columns={name_x: var, name_y: new_name}, inplace=True)
    
    return data   
    
    
def mean_id(data, var, key):
    
    """Fonction va créer une nouvelle variable égale à la somme
    aggrégées par une variable clé. 
    
    La nouvelle variable est ensuite mergé à DataFrame d'origine à l'aide de la variable clé.
    
    Args :
    
    - data = DataFrame
    - var = variable à transformer en somme
    - clé = variable clé (non-unique) utilisée pour l'aggrégation (sur laquelle on fait "groupby")
    
    Sorties :
    
    - data = DataFrame avec la nouvelle variable créée  
    """
    
    group = data[var].groupby(data[key])
    temp=group.mean()
    data = data.merge(temp, on=key, how='left')
    
    name_x = var + "_x"
    name_y = var + "_y"
    new_name = var + "_mean"
    
    data.rename(columns={name_x: var, name_y: new_name}, inplace=True)
    
    return data
    
def size_id(data, var, key):
    
    """Fonction va créer une nouvelle variable égale au nombre de lignes (~ SQL count) d'une variable clé. 
    
    La nouvelle variable est ensuite mergé à DataFrame d'origine à l'aide de la variable clé.
    
    Args :
    
    - data = DataFrame
    - var = variable à transformer en somme
    - clé = variable clé (non-unique) utilisée pour l'aggrégation (sur laquelle on fait "groupby")
    
    Sorties :
    
    - data = DataFrame avec la nouvelle variable créée  
    """
    
    group = data[var].groupby(data[key])
    temp=group.size()
    data = data.merge(temp, on=key, how='left')
    
    name_x = var + "_x"
    name_y = var + "_y"
    new_name = var + "_size"
    
    data.rename(columns={name_x: var, name_y: new_name}, inplace=True)
    
    return data
    
def max_id(data, var, key):
    
    """Fonction va créer une nouvelle variable égale au maximum
    aggrégé par une variable clé. 
    
    La nouvelle variable est ensuite mergé à DataFrame d'origine à l'aide de la variable clé.
    
    Args :
    
    - data = DataFrame
    - var = variable à transformer en somme
    - clé = variable clé (non-unique) utilisée pour l'aggrégation (sur laquelle on fait "groupby")
    
    Sorties :
    
    - data = DataFrame avec la nouvelle variable créée  
    """
    
    group = data[var].groupby(data[key])
    temp=group.max()
    data = data.merge(temp, on=key, how='left')
    
    name_x = var + "_x"
    name_y = var + "_y"
    new_name = var + "_max"
    
    data.rename(columns={name_x: var, name_y: new_name}, inplace=True)
    
    return data
    
def min_id(data, var, key):
    
    """Fonction va créer une nouvelle variable égale au minimum d'une variable clé. 
    
    La nouvelle variable est ensuite mergé à DataFrame d'origine à l'aide de la variable clé.
    
    Args :
    
    - data = DataFrame
    - var = variable à transformer en somme
    - clé = variable clé (non-unique) utilisée pour l'aggrégation (sur laquelle on fait "groupby")
    
    Sorties :
    
    - data = DataFrame avec la nouvelle variable créée  
    """
    
    group = data[var].groupby(data[key])
    temp=group.min()
    data = data.merge(temp, on=key, how='left')
    
    name_x = var + "_x"
    name_y = var + "_y"
    new_name = var + "_min"
    
    data.rename(columns={name_x: var, name_y: new_name}, inplace=True)
    
    return data
    
def transf_binaire(data,cond, nom):
    """Fonction pour transformer les variables en variables binaires.
    
    Entrées :
        data : DataFrame qui contient la variable d'origine (ex. données quanti)
        cond : condition (si vrai, variable binaire = 1)
        nom : nom de la nouvelle variable
    
    Sortie :
        data : DataFrame avec la variable recodée nommée avec sufix _bin
    """
    
    import numpy as np
       
    data[nom]=np.where(cond, 1, 0)
       
    return data 
    
def tableau_effectif(data, liste_categories, index):
    """Fonction qui a pour but de créer une table d'effectifs et de pourcentages 
    en reconstituant une variable catégorielle qui est exprimée comme matrice de variables binaires
    dans la table d'origine.

    Paramètres :

    - data : DataFrame d'origin
    - liste_categories : une liste de variables binaires à reconstituer dans une variable catégorielle
    - index : une liste contenant les noms de variables

    Sortie :

    - tableau : DataFrame avec l'effectif et pourcentage de la variable reconstituée classé par effectif. 
    L'index contient les noms de classes.

    """
    
    from pandas import DataFrame
    
    effectif = []
    for category in liste_categories:
        eff = sum(data[category])
        effectif.append(eff)

    pourc = []
    for category in liste_categories:
        pct = round(sum(data[category])*100/sum(effectif), 2)
        pourc.append(pct)

    tableau = {'Effectif': effectif, 'Pourcentage': pourc}
    tableau = DataFrame(tableau, index=index)
    tableau.sort_values('Effectif', ascending=False, inplace=True)

    return tableau
