__version__ = '1.1.6'

from .activity_task import activity_task as activity_task
from .clean_dynamic_task import clean_dynamic_task as clean_dynamic_task
from .coin_task import coin_task as coin_task
from .exchangeCoupons_task import exchangeCoupons_task as exchangeCoupons_task
from .judgement_task import judgement_task
from .lottery_task import lottery_task as lottery_task
from .manga_auto_buy_task import manga_auto_buy_task as manga_auto_buy_task
from .manga_comrade_task import manga_comrade_task as manga_comrade_task
from .manga_sign_task import manga_sign_task as manga_sign_task
from .manga_vip_reward_task import manga_vip_reward_task as manga_vip_reward_task
from .share_task import share_task as share_task
from .silver2coin_task import silver2coin_task as silver2coin_task
from .vip_task import vip_task as vip_task
from .group_sign_task import group_sign_task as group_sign_task
from .watch_task import watch_task as watch_task
from .xlive_bag_send_task import xlive_bag_send_task as xlive_bag_send_task
from .xliveSign_task import xliveSign_task as xliveSign_task
from .xlive_heartbeat_task import xlive_heartbeat_task as xlive_heartbeat_task
from .xlive_anchor_task import xlive_anchor_task as xlive_anchor_task
from .push_message_task import webhook

__all__ = (
    'activity_task',
    'clean_dynamic_task',
    'coin_task',
    'exchangeCoupons_task',
    'judgement_task',
    'lottery_task',
    'manga_vip_reward_task',
    'manga_comrade_task',
    'manga_sign_task',
    'manga_vip_reward_task',
    'share_task',
    'silver2coin_task',
    'vip_task',
    'group_sign_task',
    'watch_task',
    'xlive_bag_send_task',
    'xliveSign_task',
    'xlive_heartbeat_task',
    'xlive_anchor_task',
    'webhook'
)