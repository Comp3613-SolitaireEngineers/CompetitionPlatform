# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition import competition_views
from .competitor import competitor_views
from .rank import rank_views
from .results import results_views
from .host import host_views


views = [user_views, index_views, auth_views, competition_views, competitor_views, rank_views, results_views, host_views] 
# blueprints must be added to this list