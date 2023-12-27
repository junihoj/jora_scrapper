from available_group import job_titles_by_category

def check_in_sample(title):
    for cat in job_titles_by_category.keys():
        for keywords in job_titles_by_category[cat]:
            if(title in keywords):
                return cat           
    return False
