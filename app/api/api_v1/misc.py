

def filter_job_group_popular(list_job_group):
    group_popular = ['dev', 'cong nghe thong tin', 'engineer', 'technology',
                     'software', 'tu van', 'analyst']
    list_job_group = list(filter(lambda x: x not in [j for i in cs.LEVEL_LIST for j in i], list_job_group))
    if 2 <= len(list_job_group) != len(set(group_popular) & set(list_job_group)):
        return list(filter(lambda x: x not in group_popular, list_job_group))

    return list_job_group


def filter_duplicate_cv(list_json):
    node_nearest = list_json["candidate"]
    node_nearest_track = []
    node_nearest_temp = []
    for item in node_nearest:
        item_temp = {k: v for k, v in item.items() if
                     k in ["match_score", "work_exp", "cv_score", "function_id"]}
        if item_temp not in node_nearest_track:
            node_nearest_track.append(item_temp)
            node_nearest_temp.append(item)
        else:
            continue
    node_nearest = node_nearest_temp
    list_json["candidate"] = node_nearest
    return list_json


