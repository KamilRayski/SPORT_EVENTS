# events/urls.py
from django.urls import path
from events.views import events_views, signups_views, dashboard_views, favorites_views, auth_views

urlpatterns = [
    path('events/', events_views.events_list_create, name='events-list-create'),
    path('events/<int:event_id>/', events_views.event_detail_update_delete, name='event-detail'),
    path('events/<int:event_id>/signups/', signups_views.signup_for_event, name='event-signup'),
    path('dashboard_events/', dashboard_views.dashboard_events, name='dashboard-events'),
    path('auth/register/', auth_views.register, name='auth-register'),
    path('auth/login/', auth_views.login_view, name='auth-login'),
    path('favorites/', favorites_views.list_favorites, name='favorites-list'),
    path('favorites/add/', favorites_views.add_favorite, name='favorites-add'),
    path('favorites/<int:favorite_id>/', favorites_views.remove_favorite, name='favorites-remove'),
]
