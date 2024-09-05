def get_top_closest(compared):
    max = compared[0]["p"]
    return_data = []
    for index, video in enumerate(compared):
        if video["p"] == max or index < 5:
            return_data.append(f'{video["p"]}pts - {video["v"]} - {video["d"]}' )
        else:
            break
    return return_data