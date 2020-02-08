from app.models.statistic_log import StatisticLog
from app.models.project import Project
from sqlalchemy import func, and_
from app.service.utils import get_days_delta_by_string


def statistic_book_read_count(date_begin, date_end):
    if date_begin and date_end:
        date_end = get_days_delta_by_string(date_end, days=1)
        book_read_count_list = Project.query. \
            outerjoin(StatisticLog, and_(StatisticLog.project_id == Project.id, StatisticLog.book_id != 0,
                                         StatisticLog.created_at >= date_begin,
                                         StatisticLog.created_at <= date_end)). \
            with_entities(Project.id, Project.title, func.count(StatisticLog.id).label('count')). \
            group_by(Project.id)
    else:
        book_read_count_list = Project.query.\
            outerjoin(StatisticLog, and_(StatisticLog.project_id == Project.id, StatisticLog.book_id != 0)). \
            with_entities(Project.id, Project.title, func.count(StatisticLog.id).label('count')). \
            group_by(Project.id)
    return book_read_count_list

def statistic_video_play_count(date_begin, date_end):
    if date_begin and date_end:
        date_end = get_days_delta_by_string(date_end, days=1)
        video_play_count_list = Project.query. \
            outerjoin(StatisticLog, and_(StatisticLog.project_id == Project.id, StatisticLog.video_id != 0,
                                         StatisticLog.created_at >= date_begin,
                                         StatisticLog.created_at <= date_end)). \
            with_entities(Project.id, Project.title, func.count(StatisticLog.id).label('count')). \
            group_by(Project.id)
    else:
        video_play_count_list = Project.query.\
            outerjoin(StatisticLog, and_(StatisticLog.project_id == Project.id, StatisticLog.video_id != 0)). \
            with_entities(Project.id, Project.title, func.count(StatisticLog.id).label('count')). \
            group_by(Project.id)
    return video_play_count_list

def statistic_all(date_begin, date_end):
    book_read_count_list = statistic_book_read_count(date_begin, date_end)
    video_play_count_list = statistic_video_play_count(date_begin, date_end)
    all_click_count = []
    for book in book_read_count_list:
        for video in video_play_count_list:
            if book.id == video.id:
                data = {
                    'count': book.count + video.count,
                    'id': book.id,
                    'title': book.title
                }
                all_click_count.append(data)
    res = {
        'book_read_count': book_read_count_list,
        'video_play_count': video_play_count_list,
        'all_click_count': all_click_count
    }
    return res