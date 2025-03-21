from django.contrib.auth.tokens import PasswordResetTokenGenerator
from datetime import datetime, timedelta

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

    def check_token(self, user, token):
        """
        Override check_token method to include expiration time logic.
        """
        if not super().check_token(user, token):
            return False

        # Set expiration time (e.g., 24 hours)
        EXPIRATION_HOURS = 24

        try:
            # Get the time when the token was created
            token_time = datetime.utcfromtimestamp(user.date_joined.timestamp())  # Ensure it's UTC

            # Calculate expiration time
            expiration_time = token_time + timedelta(hours=EXPIRATION_HOURS)

            # Check if the token is still valid
            return datetime.utcnow() <= expiration_time

        except Exception as e:
            print("Token error:", str(e))
            return False  # Return False if there's an error

account_activation_token = AccountActivationTokenGenerator()
