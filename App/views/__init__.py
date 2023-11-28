# blue prints are imported 
# explicitly instead of using *
from .user import user_views
from .index import index_views
from .auth import auth_views
from .competition import comp_views
from .competitor import competitor_views


views = [user_views, index_views, auth_views, comp_views, competitor_views] 
# blueprints must be added to this list