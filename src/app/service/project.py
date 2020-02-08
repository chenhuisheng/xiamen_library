def bind_pictures(pictures, sort_order):
    res = []
    picture_dict = {picture.id: picture for picture in pictures}
    for picture_id in sort_order:
        if picture_dict.get(picture_id):
            data = picture_dict.get(picture_id).to_dict()
            res.append(data)
    for k in picture_dict.keys():
        if k not in sort_order:
            res.append(picture_dict[k].to_dict())
    return res