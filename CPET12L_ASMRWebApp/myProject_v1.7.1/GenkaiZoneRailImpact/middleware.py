from datetime import datetime, timedelta
from django.shortcuts import redirect

class CustomSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_timeout_seconds = 10  # Timeout after 10 seconds
        now = datetime.now()

        # Exclude the login URL from session timeout checks
        if request.path == "LogIn":  # Adjust this to match your login URL
            print("Login page accessed. Skipping session timeout checks.")
            return self.get_response(request)

        # Retrieve the session last_activity timestamp
        last_activity = request.session.get('last_activity')
        if last_activity:
            try:
                # Parse last_activity timestamp
                last_activity_time = datetime.strptime(last_activity, "%Y-%m-%d %H:%M:%S")
                print(f"Last activity: {last_activity_time}, Current time: {now}")

                # Check if the session has timed out
                if now - last_activity_time > timedelta(seconds=session_timeout_seconds):
                    print("Session timed out. Flushing session and redirecting to login.")
                    request.session.flush()  # Expire the session
                    return redirect('LogIn')  # Redirect to login page (adjust URL name)

            except ValueError as e:
                # Handle parsing errors
                print(f"Error parsing last_activity timestamp: {e}. Flushing session.")
                request.session.flush()
                return redirect('LogIn')

        else:
            # If no last_activity is found, this is the first request or a new session
            print("No last_activity found. Setting it now.")

        # Update last_activity in the session
        request.session['last_activity'] = now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"Updated session last_activity: {request.session['last_activity']}")

        return self.get_response(request)
