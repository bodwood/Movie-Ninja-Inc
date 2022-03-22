import pandas as pd

##Raw-Data Table##
def table_for_vis():
    temp_name = pd.read_csv("data/raw-data.csv")
    tab_name = temp_name.head(30)
    tab_rows = tab_name
    vis_tab_og = {"columns": temp_name.columns, "rows": tab_rows}

    return vis_tab_og

##Year of release vs likes##
def title_yr_likes():
    tab_name = pd.read_csv("data/raw-data.csv")
    tab_date = tab_name["title_year"]
    tab_count = tab_name["movie_facebook_likes"]
    vis_list1 = {"title_year": tab_date, "num_critic_for_reviews": tab_count}

    return vis_list1

##Duration vs Score##
def vis_count_by_date2():
    tab_name = pd.read_csv("data/raw-data.csv")
    tab_date = tab_name["duration"]
    tab_count = tab_name["imdb_score"]
    vis_list2 = {"duration": tab_date, "imdb_score": tab_count}

    return vis_list2

##title year vs imdb score##
def vis_rel_count_temp():
    temp = pd.read_csv("data/raw-data.csv")
    vis_list = {"title_year": temp["title_year"], "imdb_score": temp["imdb_score"]}
    return vis_list

##score vs duration##
def vis_rel_count_temp2():
    temp = pd.read_csv("data/raw-data.csv")
    vis_list1 = {"imdb_score": temp["imdb_score"], "duration": temp["duration"]}
    return vis_list1


