# manage.py

if __name__ == "__main__":
    import os
    import sys
    from django.core.management import execute_from_command_line

    # Use the PORT setting if defined, otherwise default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Override default port (8000) if PORT environment variable is defined
    if "runserver" in sys.argv:
        sys.argv.append(f"--noreload")  # Disable auto-reload for production
        sys.argv.append(f"0.0.0.0:{port}")

    execute_from_command_line(sys.argv)
