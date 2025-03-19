from django.utils import timezone
from datetime import datetime

def demo_session_timer(request):
    '''This context processor is used to display the time remaining for the demo session.'''
    
    if request.session.get("is_demo", False):
        # Get the expiry time from the session
        expiry_time_str = request.session.get("expiry_time")
        
        if expiry_time_str:
            expiry_time = datetime.fromisoformat(expiry_time_str)

            # Calculate the time remaining for the demo session
            time_remaining_seconds = int((expiry_time - timezone.now()).total_seconds())
            
            # Calculate the minutes and seconds
            if time_remaining_seconds > 0:
                minutes = time_remaining_seconds // 60
                seconds = time_remaining_seconds % 60

                return {
                    'time_remaining_minutes': minutes,
                    'time_remaining_seconds': seconds,
                }

    return {}